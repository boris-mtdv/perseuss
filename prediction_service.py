import pickle
import xgboost
import pandas as pd

cabins = ["A","B","C","D","E","F","G","T"]

class PredictionService:
    """
    Processes passenger features and uses loaded xgboost model to return probability of survical.
    """

    def __init__(self):
        # depending on the nature of the project, this model file could be retrieved from
        # blob storage, which could be accessed using credentials stored in a config file,
        # but for the sake of brevity the model file was included in the resources directory.
        model_file_path = "resources/xgboost_regressor.pickle"
        self.xgb_model = pickle.load(open(model_file_path, "rb"))

    def predict(self, passenger):
        processed_passenger = PredictionService.process_features(passenger)

        df = pd.DataFrame({'Pclass': [processed_passenger["Pclass"]], 'sex': [processed_passenger["sex"]],
                 'Age': [processed_passenger["Age"]], 'SibSp': [processed_passenger["SibSp"]],
                 'Parch': [processed_passenger["Parch"]], 'embarked': [processed_passenger["embarked"]],
                 'deck':[processed_passenger["deck"]]})

        # imputing None values as 0's. Could be imputed with mean depending on distribution in the dataset.
        df["Age"] = df["Age"].fillna(0)
        df["deck"] = df["deck"].fillna(8)

        prediction = self.xgb_model.predict(df)

        response = {"id": passenger["id"], "probability": str(prediction[0])}
        return response

    @staticmethod
    def process_features(passenger):
        passenger = PredictionService.process_null_age_and_cabin(passenger)
        passenger = PredictionService.process_sex(passenger)
        passenger = PredictionService.process_embark(passenger)

        return PredictionService.process_cabin(passenger)

    @staticmethod
    def process_null_age_and_cabin(passenger):
        if "Age" not in passenger:
            passenger["Age"] = None
        if "Cabin" not in passenger:
            passenger["Cabin"] = None
        return passenger

    @staticmethod
    def process_sex(passenger):
        if passenger["Sex"] != "male" and passenger["Sex"] != "female":
            raise ValueError("incorrect sex")
        if passenger["Sex"] == "male":
            passenger["sex"] = 1
        elif passenger["Sex"] == "female":
            passenger["sex"] = 0
        return passenger

    @staticmethod
    def process_embark(passenger):
        if passenger["Embark"] != "C" and passenger["Embark"] != "S" and passenger["Embark"] != "Q":
            raise ValueError("incorrect Embark value")
        if passenger["Embark"] == "C":
            passenger["embarked"] = 0
        elif passenger["Embark"] == "S":
            passenger["embarked"] = 1
        elif passenger["Embark"] == "Q":
            passenger["embarked"] = 2
        return passenger

    @staticmethod
    def process_cabin(passenger):
        if passenger["Cabin"] is not None and passenger["Cabin"][0] not in cabins:
            raise ValueError("incorrect Cabin value")
        if not passenger["Cabin"]:
            passenger["deck"] = passenger["Cabin"]
        elif passenger["Cabin"][0] == 'A':
            passenger["deck"] = 1
        elif passenger["Cabin"][0] == "B":
            passenger["deck"] = 2
        elif passenger["Cabin"][0] == "C":
            passenger["deck"] = 3
        elif passenger["Cabin"][0] == "D":
            passenger["deck"] = 4
        elif passenger["Cabin"][0] == "E":
            passenger["deck"] = 5
        elif passenger["Cabin"][0] == "F":
            passenger["deck"] = 6
        elif passenger["Cabin"][0] == "G":
            passenger["deck"] = 7
        elif passenger["Cabin"][0] == "T":
            passenger["deck"] = 8

        return passenger