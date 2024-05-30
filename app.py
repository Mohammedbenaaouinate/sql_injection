from flask import Flask,request,jsonify
from tensorflow.keras.models import load_model 
import numpy as np
import string
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Load the model
model =load_model('sql_detectionVF.h5')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the request
    data = request.get_json()
    # Assuming the query is sent in JSON format with a key 'query'
    query = data.get('query')
    # Return the prediction as JSON
    return jsonify({'prediction': predict_sql_injection(query)})

def predict_sql_injection(query):
    length=len(query)
    ponctuation_chars=set(string.punctuation)
    punctuation_count=0
    number_of_key=0
    key_words=["select", "update", "insert", "create", "drop", "alter", "rename", "exec", "order", "group", "sleep","count","where"]

    for char in query:
        if char in ponctuation_chars:
            punctuation_count+=1
    for char in query:
        if char in key_words:
            number_of_key+=1
    features=np.array([length,punctuation_count,number_of_key]).reshape(1,1,3)
    prediction=model.predict(features)
    if(prediction>=0.5):
            return 1
    else:
            return 0
    

if __name__ == '__main__':
    app.run(debug=True)
