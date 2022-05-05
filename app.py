from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from os import environ



app = Flask(__name__)
app.config["MONGO_URI"] = environ.get("MONGO_URI")
mongo = PyMongo(app)
db = mongo.db


@app.route('/api/busqueda/<busqueda_id>', methods=['GET'])
def getbusqueda(busqueda_id):
    _busqueda = db.busqueda.find_one({"_id": ObjectId(busqueda_id)})
    item = {
        'id': str(_busqueda['_id']),
        'idUser': _busqueda['idUser'],
        'idComic': _busqueda['idComic'],
        'cont': _busqueda['cont']


    }

    return jsonify(data=item), 200


@app.route('/api/busqueda', methods=['GET'])
def getbusquedas():
    _busquedas = db.busqueda.find()
    bd = environ.get("MONGO_URI")
    item = {}
    data = []
    for busqueda in _busquedas:
        item = {
            'id': str(busqueda['_id']),
            'idUser': busqueda['idUser'],
            'idComic': busqueda['idComic'],
            'cont': busqueda['cont']
        }
        data.append(item)

    return jsonify(data=data), 200


@app.route('/api/busqueda', methods=['POST'])
def createbusqueda():
    data = request.get_json(force=True)
    item = {
        'idUser': data['idUser'],
        'idComic': data['idComic'],
        'cont': data['cont']
    }
    db.busqueda.insert_one(item)

    return jsonify(data=data), 201


@app.route('/api/busqueda/<busqueda_id>', methods=['PATCH'])
def updatebusqueda(busqueda_id):
    data = request.get_json(force=True)
    db.busqueda.update_one({"_id": ObjectId(busqueda_id)}, {"$set": data})

    return jsonify(data=data), 204


@app.route('/api/busqueda/<busqueda_id>', methods=['DELETE'])
def deletebusqueda(busqueda_id):
    db.busqueda.delete_one({"_id": ObjectId(busqueda_id)})

    return jsonify(), 204


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)