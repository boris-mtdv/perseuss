from app import app
from flask import json
from prediction_service import PredictionService


def test_add():
    app.testing = True

    prediction_service = PredictionService()

    response = app.test_client().post(
        '/classify',
        data=json.dumps({
            "jsonrpc": "2.0",
            "method": "classify",
            "params": {"Pclass": 1, "Sex": "female", "Age": 34, "SibSp": 1, "Parch": 0, "Embark": "S"},
            "id": "1"
        }),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert "id" in data
    assert "probability" in data
    assert response.status_code == 200

def test_feature_processing1():
    passenger = {"Pclass" : 1,
                 "Sex" : "male",
                 "Age" : 15,
                 "SibSp" : 2,
                 "Parch" : 2,
                 "Embark" : "C",
                 "Cabin" : "C105"}

    processed_passenger = PredictionService.process_features(passenger)

    assert processed_passenger["sex"] == 1
    assert processed_passenger["deck"] == 3
    assert processed_passenger["embarked"] == 0

def test_feature_processing2():
    passenger = {"Pclass" : 1,
                 "Sex" : "female",
                 "Age" : 15,
                 "SibSp" : 2,
                 "Parch" : 2,
                 "Embark" : "S",
                 "Cabin" : "B105"}

    processed_passenger = PredictionService.process_features(passenger)

    assert processed_passenger["sex"] == 0
    assert processed_passenger["deck"] == 2
    assert processed_passenger["embarked"] == 1

def test_feature_processing3():
    passenger = {"Pclass" : 1,
                 "Sex" : "female",
                 "SibSp" : 2,
                 "Parch" : 2,
                 "Embark" : "Q"}

    processed_passenger = PredictionService.process_features(passenger)

    assert processed_passenger["Age"] == None
    assert processed_passenger["sex"] == 0
    assert processed_passenger["deck"] == None
    assert processed_passenger["embarked"] == 2
