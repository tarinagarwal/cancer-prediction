# util.py
import json
import pickle
import numpy as np
from flask import render_template
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt

__data_columns = None
__model = None

def load_saved_artifacts():
    """Loads the sklearn model, converts to ONNX, and loads column info."""
    global __data_columns, __model
    if __model is not None:
        return

    # load sklearn model
    with open('artifacts/log_model.pkl', 'rb') as f:
        sklearn_model = pickle.load(f)

    # convert to ONNX
    initial_type = [('float_input', FloatTensorType([None, 9]))]
    onnx_model = convert_sklearn(sklearn_model, initial_types=initial_type)
    __model = onnx_model.SerializeToString()

    # load data columns (if you ever need them)
    with open('artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']

def predict_risk(age, sex, weight, height,
                 alcohol_consumption, smoking,
                 genetic_risk, physical_activity,
                 diabetes, hypertension):
    """
    Runs the ONNX model to predict cancer risk.
    Returns a float between 0 and 100.
    """
    load_saved_artifacts()

    # compute BMI
    bmi = weight / (height**2)

    # assemble feature vector
    features = np.array(
        [[age, sex, bmi, alcohol_consumption,
          smoking, genetic_risk, physical_activity,
          diabetes, hypertension]],
        dtype=np.float32
    )

    # run inference
    sess = rt.InferenceSession(__model)
    input_name = sess.get_inputs()[0].name
    probs = sess.run(None, {input_name: features})

    # binary classifier: probs[1] is the output for class 1
    risk = float(probs[1][0][1] * 100.0)
    return round(risk, 2)

def apology(message, code=400):
    """Renders a simple apology page."""
    return render_template("apology.html",
                           top=code,
                           bottom=message), code
