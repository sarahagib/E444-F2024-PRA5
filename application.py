from flask import Flask, request, jsonify
import pickle
import os

# Initialize the Flask application
application = Flask(__name__)

# Load the pre-trained model and vectorizer
model_path = os.path.join(os.path.dirname(__file__), 'basic_classifier.pkl')
with open(model_path, 'rb') as fid:
    loaded_model = pickle.load(fid)


vectorizer_path = os.path.join(os.path.dirname(__file__), 'count_vectorizer.pkl')
with open(vectorizer_path, 'rb') as vd:
    vectorizer = pickle.load(vd)


@application.route('/')
def home():
    return "Fake News Detection API is running."


@application.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return "Please use POST to send data"

    try:
        # get text from the request
        print(request)
        input_text = request.form.get('text')
        
        if not input_text:
            return jsonify({'error': 'No input'}), 400
        
        print(f"Input: {input_text}")
        
        # predict using provided model
        predictions = []
        
        vectorized_input = vectorizer.transform([input_text])
        prediction = loaded_model.predict(vectorized_input)[0]
    
        if prediction == 'FAKE':
            predictions.append(1)
        elif prediction == 'REAL':
            predictions.append(0)
        else:
            raise ValueError(f"Unexpected prediction value: {prediction}")
        
        print("Prediction:", predictions)
        
        return jsonify({'input': input_text, 'prediction': predictions}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': "An error occurred during prediction"}), 500


if __name__ == "__main__":
    application.run()