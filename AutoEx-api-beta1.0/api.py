from flask import Flask, request, abort, jsonify
from waitress import serve
from time import sleep, time
import threading
import main
import queue as queue_module
import json
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)
obj={}
task_queue=queue_module.Queue(maxsize=0)

def worker():
    while True:
        try:
            uuid=task_queue.get()
            print(uuid)
            obj[uuid][0].start()
        except Exception as e:
            print(e)

def janitor():
    while True:
        sleep(2700)
        keys_to_delete = [uuid for uuid in obj if time() - obj[uuid][1] > 2700]
        for uuid in keys_to_delete:
            del obj[uuid]

class Project:
    @app.route('/')
    def index():
        return "Hello, World!"

    @app.route('/requests', methods=['POST'])
    def requests():
        #request = (request.json['maxroll'],)
        uuid = main.randomString()
        obj[uuid] = [main.resultProcessor(int(request.json['department']), int(request.json['semester']), int(request.json['maxroll']), request.json['rollPrefix']), time()]
        task_queue.put(uuid)
        response = app.response_class(
        response=json.dumps({'uuid':uuid}),
        status=200,
        mimetype='application/json'
        )
        #response.headers['Access-Control-Allow-Origin'] = '*'
        return(response)

    @app.route('/progress')
    def progress():
        uuid = request.args.get('uuid')
        try:
            return jsonify({"progress":obj[uuid][0].progress.progress, "max":obj[uuid][0].maxroll,"status":"200"})
        except:
            return jsonify({"progress":"0", "max":"0","status":"901"})
    @app.route('/getfile')
    def getfile():
        uuid = request.args.get('uuid')
        try:
            file = obj[uuid][0].package()
        except Exception as e:
            print(e)
            return("901 Resoruce Not Found/Deleted" + str(e)) #File Destoryed
        # if file != 601:
        #     del obj[uuid]

        if file in [500,701,601]:
            status = file
            file = ""
        else:
            status = 200
        #601: In progress
        #701: No result
        #500: Internal error

        return jsonify({"status":status,"file":str(file)})


if __name__ == '__main__':
    workerThread = threading.Thread(target=worker, name="Worker", daemon=True)
    janitorThread = threading.Thread(target=janitor, name="Janitor", daemon=True)
    workerThread.start()
    janitorThread.start()
    serve(app, port=int(sys.argv[1]))
