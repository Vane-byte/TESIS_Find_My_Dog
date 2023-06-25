

from flask import Flask, request, render_template,jsonify
from werkzeug.utils import secure_filename
from Steps.Step_ImageClasification import predimage,recognitionDog
from Steps.Step_NER import PredictNER
from Steps.Step_TextClasification import DogStateClasification
from Steps.Step_TextExtraction import ExtractTextFromImage

import os
import numpy as np
import cv2
import json
import base64


# Definimos una instancia de Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        f = request.files['file']
        file_contents = f.read()
        registro={
            "descripcion":'',
            "imagen": file_contents
        }
        if  registro['descripcion']== '':
            registro= ExtractTextFromImage(registro)

        registro=DogStateClasification(registro)
        registro=PredictNER(registro)
        registro=recognitionDog(registro)
        registro.pop('imagen')
        json_str = jsonify(registro)

    
        return json_str
    return None

if __name__ == '__main__':
    app.run(debug=False, threaded=False)

