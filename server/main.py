from flask import Flask, request, send_file, Response, make_response
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

import database
db = database.Database()

import analysis

import ml
predictor = ml.Predictor()

import json
import os
import threading

ROOT_DIR = "/tf/HackDuke2019"
FRONTEND_DIR = os.path.join(ROOT_DIR, "transcend")


@app.route("/")
def main():
    return send_file(os.path.join(FRONTEND_DIR, "index.html"))


@app.route("/<path:frontend_resource>", methods=["GET"])
def thing(frontend_resource):

    if request.method == "GET":
        resource_path = os.path.join(FRONTEND_DIR, frontend_resource)
        if os.path.exists(resource_path):
            return send_file(resource_path)


phone_data_queue = []
phone_data_queue_lock = threading.Lock()
phone_data_queue_condition = threading.Condition(phone_data_queue_lock)
def process_phone_data_thread():

    while True:

        # Condition is triggered whenever the queue has new data
        with phone_data_queue_condition:

            # Wait for new data
            phone_data_queue_condition.wait()

            phone_data_queue_lock.release()
            while len(phone_data_queue) > 0:

                phone_data_queue_lock.acquire()
                username, data = phone_data_queue.pop(0)
                phone_data_queue_lock.release()

                data["score"] = predictor.predict(data["message"])
                db.addText(username, data)

            phone_data_queue_lock.acquire()


@app.route("/phone_data/<string:username>", methods=["GET", "POST"])
def post_phone_data(username):
    if request.method == "POST":
        data = request.json
        
        with phone_data_queue_condition:
            phone_data_queue.append((username, data))
            phone_data_queue_condition.notify_all()

        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

    elif request.method == "GET":
        output = db.getTexts(username)
        output = analysis.filter24hours(output)
        return json.dumps(output), 200, {"ContentType": "application/json"}
    

@app.route("/add_user", methods=["POST"])
def post_add_user():
    if request.method == "POST":
        data = request.json
        db.addUser(data["username"], "randomsalt", 2834792835)
        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/user_stats/<string:username>", methods=["GET"])
def get_user_stats(username):
    if request.method == "GET":
        texts = db.getTexts(username)
        filtered = analysis.filter24hours(texts)
        if len(filtered) > 0:
            output = analysis.messageStats(filtered)
        else:
            output = {}
        return json.dumps(output), 200, {"ContentType": "application/json"}


graph_funcs = {
    "24hours": analysis.graph24hours,
    "ratio": analysis.graphRatio,
    "30days": analysis.graph30days
}

@app.route("/graph/24hours/<string:size>/<string:username>")
def get_graph_24hours(size, username):
    return get_graph(size, username, "24hours")

@app.route("/graph/ratio/<string:size>/<string:username>")
def get_graph_ratio(size, username):
    return get_graph(size, username, "ratio")

@app.route("/graph/30days/<string:size>/<string:username>")
def get_graph_30days(size, username):
    return get_graph(size, username, "30days")

def get_graph(size, username, graph):
    if request.method == "GET":
        texts = db.getTexts(username)
        if graph in graph_funcs.keys():
            if graph == "24hours" or graph == "ratio":
                texts = analysis.filter24hours(texts)
            else:
                texts = analysis.filter30days(texts)

            stats = analysis.messageStats(texts)
            print(texts[:4])

            if len(texts) > 0:
                output = analysis.generateGraph(graph_funcs[graph], texts, stats, size == "small")
                return send_file(output, mimetype="image/png")

            else:
                print("NO TEXTS")


if __name__ == "__main__":
    threading.Thread(name="phone_data_queue", target=process_phone_data_thread).start()
    app.run(host="0.0.0.0", port="5000")
