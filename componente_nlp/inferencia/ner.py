from __future__ import annotations

import config

_ner_model = None


def _get_ner_model():
    global _ner_model
    if _ner_model is None:
        from simpletransformers.ner import NERModel

        _ner_model = NERModel("bert", str(config.MODEL_NER_DIR), use_cuda=False)
    return _ner_model


def PredictNER(registro):
    model_saved = _get_ner_model()
    predictions, _raw = model_saved.predict([registro["descripcion"]])
    predictions = predictions[0]
    resultado = [reg for reg in predictions if not any(valor == "O" for valor in reg.values())]
    ner_dict = {}
    for ner in resultado:
        ner_val = [ner[key] for key in ner][0]
        if ner_val in ner_dict:
            ner_dict[ner_val] = ner_dict[ner_val] + " " + list(ner)[0]
        else:
            ner_dict[ner_val] = list(ner)[0]
    registro["NER"] = ner_dict
    return registro
