#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrena el modelo de clasificación de texto (BERT + cabeza densa, Keras SavedModel).

Equivalente a: componente_nlp/entrenamiento/5ModelCreation.ipynb

El otro modelo NLP del repo es el NER; para entrenarlo usa `08_ner_train.py`
(después de preparar datos con `07_ner_export_tokens.py` y anotar).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import tensorflow as tf
from transformers import TFAutoModel

from _paths import DATA_DIR, REPO_ROOT


def build_model(seq_len: int = 512):
    bert = TFAutoModel.from_pretrained("bert-base-multilingual-cased", use_safetensors=False)
    input_ids = tf.keras.layers.Input(shape=(seq_len,), name="input_ids", dtype="int64")
    mask = tf.keras.layers.Input(shape=(seq_len,), name="attention_mask", dtype="int64")
    embeddings = bert.bert(input_ids, attention_mask=mask)[1]
    x = tf.keras.layers.Dense(1024, activation="relu")(embeddings)
    y = tf.keras.layers.Dense(2, activation="softmax", name="outputs")(x)
    model = tf.keras.Model(inputs=[input_ids, mask], outputs=y)
    model.layers[2].trainable = False
    return model


def main():
    parser = argparse.ArgumentParser(
        description="Entrena clasificación de texto (SavedModel). Ver también 08_ner_train.py para NER."
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=DATA_DIR / "4_dataset",
        help="Carpeta con subcarpetas train/ y val/ (salida de 04_dataset_creation)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "Helpers" / "Modelos" / "lost_dogs_model_trained",
        help="Ruta de salida del SavedModel",
    )
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--learning-rate", type=float, default=5e-5)
    parser.add_argument("--seq-len", type=int, default=512)
    args = parser.parse_args()

    bs = args.batch_size
    sl = args.seq_len

    element_spec = (
        {
            "input_ids": tf.TensorSpec(shape=(bs, sl), dtype=tf.int64, name=None),
            "attention_mask": tf.TensorSpec(shape=(bs, sl), dtype=tf.int64, name=None),
        },
        tf.TensorSpec(shape=(bs, 2), dtype=tf.float32, name=None),
    )

    train_path = args.dataset_dir / "train"
    val_path = args.dataset_dir / "val"
    train_ds = tf.data.Dataset.load(str(train_path), element_spec=element_spec)
    val_ds = tf.data.Dataset.load(str(val_path), element_spec=element_spec)

    model = build_model(sl)
    optimizer = tf.keras.optimizers.Adam(learning_rate=args.learning_rate)
    loss = tf.keras.losses.CategoricalCrossentropy()
    acc = tf.keras.metrics.CategoricalAccuracy("accuracy")
    model.compile(optimizer=optimizer, loss=loss, metrics=[acc])

    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(args.output))
    print(f"Modelo de clasificación guardado en: {args.output}")


if __name__ == "__main__":
    main()
