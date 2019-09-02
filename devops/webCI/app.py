from flask import Flask, escape, request, json
import auto_docker
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def push():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            auto_docker.activate_docker()
            return json.dumps(request.json)
    elif request.method == 'GET':
        return "This is WebCI"


#@app.route('/commit', methods=['POST', 'GET'])
#def commitLog():
    