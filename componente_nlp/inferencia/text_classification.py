import tensorflow as tf
from transformers import BertTokenizer

import config

# Clasificación de texto (perdido / encontrado)
model_text_classy = tf.keras.models.load_model(str(config.MODEL_TEXT_CLASSIFICATION_DIR))

tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")


def prep_data(text):
    tokens = tokenizer.encode_plus(
        text,
        max_length=512,
        truncation=True,
        padding="max_length",
        add_special_tokens=True,
        return_token_type_ids=False,
        return_tensors="tf",
    )
    return {
        "input_ids": tf.cast(tokens["input_ids"], tf.float64),
        "attention_mask": tf.cast(tokens["attention_mask"], tf.float64),
    }


def DogStateClasification(registro):
    probs = model_text_classy.predict(prep_data(registro["descripcion"]))[0][0]
    if round(probs) == 1:
        print("El post es de perro perdido.")
    else:
        print("El post es de perro encontrado.")
    registro["SePerdio"] = round(probs)
    return registro
