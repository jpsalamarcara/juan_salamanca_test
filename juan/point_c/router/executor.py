from juan.point_c.common import handle_generic_error
from juan.point_c.router.config import logger

import os
import redis
from flask import Flask, Response, request, jsonify
from flask_cors import cross_origin

app = Flask(__name__)
redis_connection = redis.Redis(host=os.environ['REDIS_HOST'], port=6379, db=0)
debug = os.environ['DEBUG'] == '1'
routes_key = 'routes'


@app.errorhandler(Exception)
def error_handler(error):
    return handle_generic_error(error, logger, debug=debug)


def bytes_dict_to_str_dict(data):
    #
    # help function taken from :
    # https://stackoverflow.com/questions/33137741/fastest-way-to-convert-a-dicts-keys-values-from-bytes-to-str-in-python3
    #

    if isinstance(data, bytes):
        return data.decode('ascii')
    if isinstance(data, dict):
        return dict(map(bytes_dict_to_str_dict, data.items()))
    if isinstance(data, tuple):
        return map(bytes_dict_to_str_dict, data)
    return data


@app.route("/v1/routes", methods=['GET', ])
@cross_origin()
def query_cache_regions():
    lat = request.args.get('lat')
    long = request.args.get('long')
    radius = request.args.get('radius', '500')
    unit = request.args.get('unit', 'km')
    assert lat is not None, 'lat must have a value'
    assert long is not None, 'long must have a value'
    results = redis_connection.georadius(routes_key, long, lat, radius, unit=unit, sort='ASC')
    if len(results) > 0:
        output = redis_connection.hgetall(results[0])
        return jsonify(bytes_dict_to_str_dict(output))

    else:
        return Response(status=404, response='Try with a wide radius')


@app.route("/v1/routes", methods=['POST', ])
@cross_origin()
def add_cache_region():
    data = request.json
    assert data is not None, 'There is no json header'
    fields = ['region', 'lat', 'long', 'url']
    row = {}
    for field in fields:
        assert field in data.keys(), '{} must have a value'.format(field)
        row[field] = data[field]
    redis_connection.geoadd(routes_key, row['long'], row['lat'], row['region'])
    redis_connection.hmset(row['region'], row)
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
