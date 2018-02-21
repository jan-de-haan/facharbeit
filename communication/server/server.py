from pathlib import Path
from threading import Thread

from flask import Flask, Response, request
from flask_restful import Resource, Api, reqparse
from flask_jsonpify import jsonify
from sensor import new_measurement, time_left

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument("duration")

class StartMeasurement(Resource):
    def post(self):
        if time_left > 0:
            return Response("Already measuring for the next "
                + str(time_left) + " ms", status=503)

        args = parser.parse_args()
        duration = int(args["duration"])
        thread = Thread(target = new_measurement, args = (duration, ))
        thread.start()
        return Response("", status=200)

class AvailableDataSets(Resource):
    def get(self):
        datasets_dir = Path("./datasets/")
        datasets = list(map(lambda p: p.name, list(datasets_dir.glob("*.csv"))))
        print(datasets)
        return jsonify(datasets)

class DownloadDataSet(Resource):
    def get(self, dataset_name):
        try:
            with open("./datasets/" + dataset_name, "r") as dataset_file:
                return Response(dataset_file.read()
                    , mimetype="text/comma-separated-values")
        except IOError:
            return Response("The requested dataset does not exist\n"
                , status=404, mimetype="text/plain")

api.add_resource(StartMeasurement, "/accelerometer/start-measurement")
api.add_resource(AvailableDataSets, "/accelerometer/datasets")
api.add_resource(DownloadDataSet, "/accelerometer/datasets/<string:dataset_name>")

if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
