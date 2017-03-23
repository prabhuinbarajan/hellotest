#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class TestHelloTestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_hellotest_model(self):
        from qube.src.models.hellotest import HelloTest
        hellotest_data = HelloTest(name='testname')
        hellotest_data.tenantId = "23432523452345"
        hellotest_data.orgId = "987656789765670"
        hellotest_data.createdBy = "1009009009988"
        hellotest_data.modifiedBy = "1009009009988"
        hellotest_data.createDate = str(int(time.time()))
        hellotest_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            hellotest_data.save()
            self.assertIsNotNone(hellotest_data.mongo_id)
            hellotest_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
