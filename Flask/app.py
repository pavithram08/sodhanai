from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json
import preprocess_text
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
import pickle


app = Flask(__name__)
cors = CORS(app, resources={r"/predict": {"origins": "https://sodhanai.onrender.com//predict"}})


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
# @cross_origin()
def predict():
    print(request.method)
    try:
        tf_idf = pickle.load(open('./Models/tfidf_tokenizer.pkl', 'rb'))
        rf_model = pickle.load(open('./Models/random_forest.pkl', 'rb'))
        tokenizer = pickle.load(open('./Models/tf_tokenizer.pkl', 'rb'))
        model = load_model('./Models/lstm.h5', compile=False)
        text = request.form['text']
        new_text = preprocess_text.clean_text(text)
        vec = tf_idf.transform([new_text])
        ml_pred = rf_model.predict(vec)
        ml_pred = int(ml_pred[0])
        print(f"ML Prediction: {ml_pred}")
        print("Data type of ml_pred:", type(ml_pred))

       
        return jsonify({"status": 200,"ml_pred": json.dumps(ml_pred)})
    except:
        pass

    return jsonify({"status": 422, "message": "Internal Server Error"})


if __name__ == '__main__':
    app.run(debug=True)

