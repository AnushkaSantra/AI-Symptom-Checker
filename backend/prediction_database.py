import json
import os
from datetime import datetime


# =====================================================
# DATABASE FILE
# =====================================================

DATABASE_FILE = os.path.join(
    os.path.dirname(__file__),
    "prediction_history.json"
)


# =====================================================
# LOAD PREDICTIONS
# =====================================================

def _load_predictions():

    if not os.path.exists(DATABASE_FILE):
        return []

    try:

        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception as error:

        print(
            "Prediction database load error:",
            error
        )

        return []


# =====================================================
# SAVE PREDICTIONS
# =====================================================

def _save_predictions(predictions):

    try:

        with open(
            DATABASE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                predictions,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:

        print(
            "Prediction database save error:",
            error
        )

        return False


# =====================================================
# ADD PREDICTION
# =====================================================

def add_prediction(prediction):

    predictions = _load_predictions()


    # Generate a unique numeric ID
    existing_ids = []

    for item in predictions:

        try:

            existing_ids.append(
                int(item.get("id", 0))
            )

        except (ValueError, TypeError):

            pass


    new_id = (
        max(existing_ids) + 1
        if existing_ids
        else 1
    )


    now = datetime.now()


    record = {

        "id":
            new_id,

        "patientName":
            prediction.get(
                "patientName",
                "Unknown"
            ),

        "patientAge":
            prediction.get(
                "patientAge",
                "Unknown"
            ),

        "patientGender":
            prediction.get(
                "patientGender",
                "Unknown"
            ),

        "disease":
            prediction.get(
                "disease",
                "Unknown"
            ),

        "confidence":
            prediction.get(
                "confidence",
                0
            ),

        "severity":
            prediction.get(
                "severity",
                "Unknown"
            ),

        "doctor":
            prediction.get(
                "doctor",
                "General Physician"
            ),

        "date":
            now.strftime(
                "%Y-%m-%d"
            ),

        "time":
            now.strftime(
                "%H:%M:%S"
            )

    }


    predictions.append(record)


    if not _save_predictions(
        predictions
    ):

        return None


    print(
        "Prediction history saved:",
        record
    )


    return record


# =====================================================
# GET ALL PREDICTIONS
# =====================================================

def get_predictions():

    return _load_predictions()


# =====================================================
# GET PREDICTION BY ID
# =====================================================

def get_prediction_by_id(
    prediction_id
):

    predictions = _load_predictions()


    for prediction in predictions:

        if str(
            prediction.get("id")
        ) == str(prediction_id):

            return prediction


    return None


# =====================================================
# UPDATE PREDICTION
# =====================================================

def update_prediction(
    prediction_id,
    updated_data
):

    predictions = _load_predictions()


    for index, prediction in enumerate(
        predictions
    ):

        if str(
            prediction.get("id")
        ) == str(prediction_id):

            # Make sure updated_data is a dictionary
            if not isinstance(
                updated_data,
                dict
            ):

                return None


            # Update only supplied fields
            for key, value in updated_data.items():

                # Do not allow the ID to be changed
                if key == "id":
                    continue

                prediction[key] = value


            predictions[index] = prediction


            if not _save_predictions(
                predictions
            ):

                return None


            print(
                "Prediction updated:",
                prediction
            )


            return prediction


    return None


# =====================================================
# DELETE PREDICTION BY ID
# =====================================================

def delete_prediction(
    prediction_id
):

    predictions = _load_predictions()


    for index, prediction in enumerate(
        predictions
    ):

        if str(
            prediction.get("id")
        ) == str(prediction_id):

            deleted_prediction = predictions.pop(
                index
            )


            if not _save_predictions(
                predictions
            ):

                return None


            print(
                "Prediction deleted:",
                deleted_prediction
            )


            return deleted_prediction


    return None


# =====================================================
# DELETE ALL PREDICTIONS
# =====================================================

def clear_predictions():

    if _save_predictions([]):

        print(
            "All prediction history cleared."
        )

        return True


    return False