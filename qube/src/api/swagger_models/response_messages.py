from flask_restful_swagger_2 import Schema

from qube.src.api.swagger_models.hellotest import HelloTestErrorModel
from qube.src.api.swagger_models.hellotest import HelloTestModel
from qube.src.api.swagger_models.hellotest import HelloTestModelPostResponse

"""
the common response messages printed in swagger UI
"""

post_response_msgs = {
    '201': {
        'description': 'CREATED',
        'schema': HelloTestModelPostResponse
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': HelloTestErrorModel
    }
}

get_response_msgs = {
    '200': {
        'description': 'OK',
        'schema': HelloTestModel
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': HelloTestErrorModel
    }
}

put_response_msgs = {
    '204': {
        'description': 'No Content'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': HelloTestErrorModel
    }
}

del_response_msgs = {
    '204': {
        'description': 'No Content'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error',
        'schema': HelloTestErrorModel
    }
}

response_msgs = {
    '200': {
        'description': 'OK'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error'
    }
}


class ErrorModel(Schema):
    type = 'object'
    properties = {
        'error_code': {
            'type': 'string'
        },
        'error_message': {
            'type': 'string'
        }
    }
