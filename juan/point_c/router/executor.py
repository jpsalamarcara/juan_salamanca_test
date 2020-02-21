from .config import logger


import os
import redis
from flask import Flask, jsonify
from flask_cors import cross_origin
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
redis_connection = redis.Redis(host=os.environ['REDIS_HOST'], port=6379, db=0)
debug = os.environ['DEBUG'] == '1'


@app.errorhandler(Exception)
def handle_generic_error(error):
    unexpected = False
    if isinstance(error, AssertionError):
        output = {'internal_status': 'EXCEPTION',
                  'payload': {'error': 'AssertionError',
                              'message': '{}'.format(error),
                              'biz_code': 2,
                              'more_info': ''}
                  }
        status = 422
    elif isinstance(error, HTTPException):
        output = {'internal_status': 'EXCEPTION',
                  'payload': {'error': 'HTTPException',
                              'message': '{}'.format(error.description),
                              'biz_code': 1,
                              'more_info': ''}
                  }
        status = error.code
    else:
        output = {'internal_status': 'EXCEPTION',
                  'payload': {'error': 'Exception',
                              'message': 'Unexpected error',
                              'biz_code': 0,
                              'more_info': 'Contact the API Admin!'}
                  }
        status = 500
        unexpected = True
    if debug or unexpected:
        logger.exception(error)
    response = jsonify(output)
    response.status_code = status
    return response


@app.route("/v1/router", methods=['GET', ])
@cross_origin()
def get_index():
    return 'It\'s working'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
