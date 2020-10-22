from flask import Flask, request, jsonify
from marshmallow import ValidationError
from passenger import PassengerSchema
from prediction_service import PredictionService

app = Flask(__name__)
prediction_service = PredictionService()

@app.route('/classify', methods=["POST"])
def classify():
    data = request.get_json()
    # initial vaalidation of request fields
    try:
        passenger = PassengerSchema().load(data["params"])
        passenger["id"] = data["id"]

    except ValidationError as err:
        return (err.messages)

    response_object = prediction_service.predict(passenger)

    return jsonify(response_object)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)