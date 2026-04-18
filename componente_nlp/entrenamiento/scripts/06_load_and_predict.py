#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Equivalente a: componente_nlp/entrenamiento/6Load_and_predict.ipynb

Carga el SavedModel de clasificación, define prep_data y predice (texto suelto o CSV).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer

from _paths import DATA_DIR, REPO_ROOT


def prep_data(text: str, tokenizer: BertTokenizer):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        type=Path,
        default=REPO_ROOT / "Helpers" / "Modelos" / "lost_dogs_model2",
        help="Ruta al SavedModel entrenado",
    )
    parser.add_argument(
        "--text",
        default="",
        help="Si se indica, una sola predicción y se imprime el vector de probabilidades",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="CSV con columna de texto para etiquetar en lote (sep ;)",
    )
    parser.add_argument(
        "--csv-text-col",
        default="text",
        help="Nombre de la columna de texto en el CSV",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="CSV de salida si se usa --csv",
    )
    args = parser.parse_args()

    model = tf.keras.models.load_model(str(args.model))
    tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")

    if args.text:
        probs = model.predict(prep_data(args.text, tokenizer), verbose=0)[0]
        print(probs)
        return

    if args.csv is None:
        print("Usa --text \"...\" o --csv ruta.csv")
        return

    pd.set_option("display.max_colwidth", None)
    df = pd.read_csv(args.csv, sep=";", encoding="utf-8", on_bad_lines="skip")
    if args.csv_text_col not in df.columns:
        raise SystemExit(f"Falta columna {args.csv_text_col}. Columnas: {list(df.columns)}")

    df["tipoPost"] = None
    for i, row in df.iterrows():
        tokens = prep_data(str(row[args.csv_text_col]), tokenizer)
        probs = model.predict(tokens, verbose=0)
        pred = int(np.argmax(probs))
        df.at[i, "tipoPost"] = pred

    out = args.out or (args.csv.with_name(args.csv.stem + "_predicted.csv"))
    df.to_csv(out, sep=";", index=False)
    print(f"Guardado: {out}")


if __name__ == "__main__":
    main()
