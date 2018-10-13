from flask import Flask, jsonify, request
import json
from slogansvc.category import Category
from slogansvc.slogangw import get as get_s, listall as listall_s, upsert as upsert_s, delete as delete_s
from slogansvc.categorygw import get as get_c, listall as listall_c, upsert as upsert_c, delete as delete_c
from slogansvc.sourcegw import get as get_src, listall as listall_src, upsert as upsert_src, delete as delete_src
from slogansvc.source import Source

app = Flask(__name__)


def not_found():
    message = {
        'status': 404,
        'message': f'Not Found: {request.url}',
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


# ######## slogans #########

@app.route("/slogans/<s_id>")
def get_slogan(s_id):
    slogan = get_s(s_id)
    if slogan:
        return jsonify(slogan.__dict__)
    return not_found()


@app.route("/slogans", methods=['GET', 'POST', 'PUT'])
def save_slogan():
    if request.method == 'GET':
        return jsonify([slogan.__dict__ for slogan in listall_s()])
    slogan = json.loads(request.get_json())
    response = upsert_s(slogan)
    return jsonify(response)


@app.route("/slogans/<s_id>", methods=['DELETE'])
def delete_slogan(s_id):
    delete_s(s_id)
    return jsonify(200)


# ######## slogans #########

# ######## category #########

@app.route("/categories/<c_id>")
def get_category(c_id):
    category = get_c(c_id)
    if category:
        return jsonify(category.__dict__)
    return not_found()


@app.route("/categories", methods=['GET', 'POST', 'PUT'])
def save_category():
    if request.method == 'GET':
        return jsonify([c.__dict__ for c in listall_c()])

    category = json.loads(request.data, object_hook=lambda d: Category(**d))
    c_id = upsert_c(category)
    return jsonify({'category_id': c_id})


@app.route("/categories/<c_id>", methods=['DELETE'])
def delete_category(c_id):
    delete_c(c_id)


# ######## category #########

# ######## source #########

@app.route("/sources/<src_id>")
def get_source(src_id):
    source = get_src(src_id)
    if source:
        return jsonify(source.__dict__)
    return not_found()


@app.route("/sources", methods=['GET', 'POST', 'PUT'])
def save_sources():
    if request.method == 'GET':
        return jsonify([s.__dict__ for s in listall_src()])

    src = json.loads(request.data, object_hook=lambda d: Source(**d))
    upsert_src(src)


@app.route("/sources/<src_id>", methods=['DELETE'])
def delete_source(src_id):
    delete_src(src_id)


# ######## source #########


if __name__ == "__main__":
    app.run(host='0.0.0.0')
