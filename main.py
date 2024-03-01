from flask import Flask, render_template, request
import os
from keras.models import load_model
import numpy as np
import cv2

app = Flask(__name__)

# Load the trained model
model = load_model('wheatDiseaseModel.h5')

# Define image size (assuming it's the same as during training)
img_size = 64

# Define the directory containing the images to be classified
klass_dir = 'test'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the uploaded file to the test directory
            file.save(os.path.join(klass_dir, file.filename))

            # Load and preprocess the uploaded image
            image = cv2.imread(os.path.join(klass_dir, file.filename))
            resized_image = cv2.resize(image, (img_size, img_size))
            resized_image = resized_image / 255.0
            resized_image = np.expand_dims(resized_image, axis=0)  # Add batch dimension

            # Make prediction
            prediction = model.predict(resized_image)
            rounded_prediction = np.argmax(prediction)

            return render_template('result.html', filename=file.filename, prediction=rounded_prediction)


if __name__ == '__main__':
    app.run(debug=True)
