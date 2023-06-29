from flask import Flask, request, render_template,jsonify
from werkzeug.utils import secure_filename
from Steps.Step_ImageClasification import predimage,recognitionDog

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

        f = request.files['file']
        file_contents = f.read()
        registro={
            "descripcion":'',
            "imagen": file_contents
        }
        finalEvaluation(registro)
        registro.pop('imagen')
        json_str = jsonify(registro)
    
        return json_str
    return None

if __name__ == '__main__':
    from evalFromMongoDB import finalEvaluation
    app.run(debug=False, threaded=False)

