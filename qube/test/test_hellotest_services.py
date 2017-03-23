#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['HELLOTEST_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['HELLOTEST_MONGOALCHEMY_SERVER'] = ''
    os.environ['HELLOTEST_MONGOALCHEMY_PORT'] = ''
    os.environ['HELLOTEST_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.hellotest import HelloTest
    from qube.src.services.hellotestservice import HelloTestService
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, HelloTestServiceError


class TestHelloTestService(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.hellotestService = HelloTestService(context)
        self.hellotest_api_model = self.createTestModelData()
        self.hellotest_data = self.setupDatabaseRecords(self.hellotest_api_model)
        self.hellotest_someoneelses = \
            self.setupDatabaseRecords(self.hellotest_api_model)
        self.hellotest_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.hellotest_someoneelses.save()
        self.hellotest_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.hellotest_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.hellotest_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, hellotest_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            hellotest_data = HelloTest(name='test_record')
            for key in hellotest_api_model:
                hellotest_data.__setattr__(key, hellotest_api_model[key])

            hellotest_data.description = 'my short description'
            hellotest_data.tenantId = "23432523452345"
            hellotest_data.orgId = "987656789765670"
            hellotest_data.createdBy = "1009009009988"
            hellotest_data.modifiedBy = "1009009009988"
            hellotest_data.createDate = str(int(time.time()))
            hellotest_data.modifiedDate = str(int(time.time()))
            hellotest_data.save()
            return hellotest_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_hellotest(self, *args, **kwargs):
        result = self.hellotestService.save(self.hellotest_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.hellotest_api_model['name'])
        HelloTest.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_hellotest(self, *args, **kwargs):
        self.hellotest_api_model['name'] = 'modified for put'
        id_to_find = str(self.hellotest_data.mongo_id)
        result = self.hellotestService.update(
            self.hellotest_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.hellotest_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_hellotest_description(self, *args, **kwargs):
        self.hellotest_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.hellotest_data.mongo_id)
        result = self.hellotestService.update(
            self.hellotest_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.hellotest_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_hellotest_item(self, *args, **kwargs):
        id_to_find = str(self.hellotest_data.mongo_id)
        result = self.hellotestService.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_hellotest_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(HelloTestServiceError):
            self.hellotestService.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_hellotest_list(self, *args, **kwargs):
        result_collection = self.hellotestService.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.hellotest_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.hellotest_data.mongo_id)
        with self.assertRaises(HelloTestServiceError) as ex:
            self.hellotestService.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.hellotest_data.mongo_id)
        self.hellotestService.auth_context.is_system_user = True
        self.hellotestService.delete(id_to_delete)
        with self.assertRaises(HelloTestServiceError) as ex:
            self.hellotestService.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.hellotestService.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.hellotest_someoneelses.mongo_id)
        with self.assertRaises(HelloTestServiceError):
            self.hellotestService.delete(id_to_delete)
