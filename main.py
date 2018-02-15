from flask import Flask, request, Response
import json
import uuid
from random import randrange, choice
import datetime
from flask_socketio import SocketIO, emit, send
from time import sleep
from random import uniform

app = Flask(__name__)
socketio = SocketIO(app)
users = {}


@app.route("/<username>/vista_parcial")
def handle_message(username):
    return json.dumps([{"x": i, "y": uniform(0, 1)} for i in xrange((2**10)*8)])


@app.route("/login", methods=['GET', 'POST', 'PUT'])
def login():

    print users.keys()

    if request.method == 'POST':
        content = request.get_json()
        username = content["username"]
        users[username] = {"access": True, "user": username, "publickey": 1234, "logued": True}
        return json.dumps(users[username])

    if request.method == 'GET':
        content = request.get_json()
        username = content["username"]
        return json.dumps(users[username])

    if request.method == 'PUT':
        content = request.get_json()
        username = content["username"]
        users[username] = {"access": True, "user": username, "publickey": 1234, "logued": False}
        return json.dumps(users[username])


def random_date(start,l):
   current = start
   while l >= 0:
      curr = current + datetime.timedelta(minutes=randrange(60))
      yield curr
      l-=1


@app.route("/<username>/experiments", methods=['GET', 'POST', 'PUT', 'UPDATE', 'DELETE', 'PATCH'])
@app.route("/<username>/experiments/<int:idexp>", methods=['GET', 'POST', 'PUT', 'UPDATE', 'DELETE', 'PATCH'])
def experiments_lists(username, idexp=None):

    if request.method == 'GET' and not idexp and username == "jperez":
        d = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False}
        return Response(json.dumps(d), status=200, mimetype='application/json')

    if request.method == 'GET' and not idexp and username == "pbovina":
        n_users = 10
        startDate = datetime.datetime(2013, 9, 20, 13, 00)
        authors = ["pbovina", "lmessi", "jreno", "jpmorgan", "dtrump", "cfk"]
        descr = ["atado con alambre", "el mejor experiemento", "casi lo termino", "ni Albert lo podia hacer mejor", "no salio bien"]
        states = ["en edicion", "en ejcucion", "finalizado", "cancelado"]
        d = []
        for i in range(n_users):
            d.append({"id": str(uuid.uuid4()),
                      "created": [x for x in random_date(startDate, 1)][0].strftime("%c"),
                      "author": choice(authors),
                      "resume": choice(descr),
                      "state": choice(states)})
        dd = {"error": False, "msg": "tu consulta no esta permitida", "username": "jperez", "authError": False, "datas": d}
        return json.dumps(dd)

    # endpoint para errores
    if idexp == 1:
        d = {"error": True, "msg": "este experimento no esta disponible", "username": "jperez"}
        return Response(json.dumps(d), status=404, mimetype='application/json')

    # endpoint para exitos
    if idexp == 2:
        d = {"error": False, "msg": "operacion realizada con exito", "data": "este es el experimentto"}
        return Response(json.dumps(d), status=200, mimetype='application/json')

    #endpoint para crear experimento

    if request.method == "PATCH":
        print request.json
        d = {"error": False, "msg": "operacion realizada con exito", "data": "este es el experimentto"}
        return Response(json.dumps(d), status=200, mimetype='application/json')


if __name__ == "__main__":
    socketio.run(app, debug=True)
