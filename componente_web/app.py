import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from componente_web.evaluation.eval_from_mongodb import finalEvaluation

_WEB_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(_WEB_DIR / "templates"),
    static_folder=str(_WEB_DIR / "static"),
    static_url_path="/static",
)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def upload():
    if request.method != "POST":
        return jsonify({"error": "Use POST con formulario multipart"}), 405

    desc = request.form.get("desc") or ""
    file = request.files.get("file")
    if file is None or file.filename == "":
        return jsonify({"error": "Falta archivo de imagen"}), 400

    file_contents = file.read()
    images_dir = _WEB_DIR / "static" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    photo_path = images_dir / "photo_search.png"
    photo_path.write_bytes(file_contents)

    registro = {"descripcion": desc, "imagen": file_contents}
    det, res = finalEvaluation(registro)

    return jsonify(
        objects=res,
        SePerdio=det["SePerdio"],
        NER=det["NER"],
        Razas=det["imagen_razas"],
        Desc=det["descripcion"],
    )


@app.route("/search", methods=["GET"])
def result():
    raw = request.args.get("data")
    if not raw:
        return jsonify({"error": "Parámetro data requerido"}), 400
    processed_data = json.loads(raw)
    res = processed_data["objects"]
    se_perdio = processed_data["SePerdio"]
    ner = processed_data["NER"]
    razas = processed_data["Razas"]
    desc = processed_data["Desc"]

    return render_template(
        "search.html",
        objects=res,
        SePerdio=se_perdio,
        NER=ner,
        Razas=razas,
        Desc=desc,
    )


if __name__ == "__main__":
    app.run(debug=False, threaded=False)
