import base64

from werkzeug.exceptions import abort

from juan.point_c.common import handle_generic_error
from juan.point_c.cache.config import logger


import os
import redis
from flask import Flask, jsonify, request, Response
from flask_cors import cross_origin


app = Flask(__name__)
redis_connection = redis.Redis(host=os.environ['REDIS_HOST'], port=6379, db=0)
debug = os.environ['DEBUG'] == '1'
app_version = '0.1'
region = os.environ['REGION']
lat_long = os.environ['LAT_LONG']
expire_time = int(os.environ['EXPIRE_TIME'])


def get_db_status():
    status = None
    try:
        if redis_connection.ping():
            status = 'connected'
    except redis.ConnectionError:
        status = 'not_connected'
    return status


@app.errorhandler(Exception)
def handle_errors(error):
    return handle_generic_error(error, logger, debug=debug)


@app.route("/v1/cache/status", methods=['GET', ])
@cross_origin()
def get_index():
    status = get_db_status()
    output = {'db': status, 'version': app_version, 'region': region, 'lat_long': lat_long}
    return jsonify(output)


@app.route("/v1/cache/<key>", methods=['GET', ])
@cross_origin()
def get_object(key):
    row = redis_connection.hgetall(key)
    if row is None:
        abort(404)
    else:
        redis_connection.expire(key, expire_time)
        response = Response(
            response=base64.b64decode(row[b'content']),
            status=200, mimetype=row[b'content-type'].decode('ascii'))
        return response


@app.route("/v1/cache", methods=['POST', ])
@cross_origin()
def put_object():
    data = request.data
    key = request.headers.get('X-Key')
    content_type = request.headers.get('Content-Type')
    assert data is not None, 'body must have a value'
    assert key is not None, 'Header X-Key must have a value'
    assert content_type is not None, 'Header Content-Type must have a value'
    row = {'content': base64.b64encode(data), 'content-type': content_type.encode('ascii')}
    if redis_connection.exists(key):
        redis_connection.delete(key)
    redis_connection.hmset(key, row)
    redis_connection.expire(key, expire_time)
    return Response(status=201)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181)
