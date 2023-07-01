from flask import Flask, request, render_template,jsonify

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
        registro={
            "descripcion":desc,
            "imagen": file_contents
        }
        det, res=finalEvaluation(registro)
        data={
            'SePerdio': det['SePerdio'],
            'NER':det['NER'],
            'Razas': det['imagen_razas'],
            'Resultados': list(res)
        }
     
        return render_template('search.html', objects=res, SePerdio=det['SePerdio'], NER=det['NER'], Razas=det['imagen_razas'])
    return None


@app.route('/search')
def result():
    # Retrieve the processed data from the query parameters
    processed_data = request.args.get('data')
    # Render the result HTML template and pass the processed data to it
    return processed_data

if __name__ == '__main__':
    from evalFromMongoDB import finalEvaluation
    app.run(debug=False, threaded=False)

