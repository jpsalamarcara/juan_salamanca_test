from werkzeug.exceptions import HTTPException
from flask import jsonify


def handle_generic_error(error, logger, debug=False):
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
