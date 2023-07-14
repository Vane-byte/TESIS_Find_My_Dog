import base64
from flask import Flask, request, render_template,jsonify

import json
import os


# Definimos una instancia de Flask
app = Flask(__name__, root_path=os.getcwd())

app.root_path = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        desc = request.form.get('desc')
        file = request.files['file']
        file_contents = file.read()
        with open('static\images\photo_search.png', 'wb') as newFile:
            newFile.write(file_contents)
        
        registro={
            "descripcion":desc,
            "imagen": file_contents
        }
        det, res=finalEvaluation(registro)
    
        return jsonify(
            objects=res, 
            SePerdio=det['SePerdio'], 
            NER=det['NER'], 
            Razas=det['imagen_razas'],
            Desc=det['descripcion'])
    return None


@app.route('/search', methods=['GET'])
def result():
    # Retrieve the processed data from the query parameters
    # Render the result HTML template and pass the processed data to it
    processed_data = json.loads(request.args.get('data'))
    print("PPPPPPPPPPPPPPPP: " ,processed_data)
    res=processed_data["objects"]
    SePerdio=processed_data["SePerdio"]
    NER=processed_data["NER"]
    Razas=processed_data["Razas"]
    Desc=processed_data["Desc"]

    return render_template('search.html',
            objects=res, 
            SePerdio=SePerdio, 
            NER=NER, 
            Razas=Razas,
            Desc=Desc)

if __name__ == '__main__':
    from evalFromMongoDB import finalEvaluation
    app.run(debug=False, threaded=False)

