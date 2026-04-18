#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Equivalente a: componente_nlp/entrenamiento/3dataPreProcessing.ipynb

Lee Excel etiquetado, tokeniza con BERT multilingual y guarda .npy (ids, mask, labels one-hot).
"""
from __future__ import annotations

import argparse
import builtins
from pathlib import Path

import numpy as np
import pandas as pd
from transformers import BertTokenizer

from _paths import DATA_DIR


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_DIR / "2_clean" / "complete_clean_data.xlsx",
        help="Excel con columnas de texto y etiqueta (ver --text-col / --label-col)",
    )
    parser.add_argument(
        "--text-col",
        default="text",
        help="Nombre columna texto (si no existe, se intenta 'post_description')",
    )
    parser.add_argument(
        "--label-col",
        default="tipoPost",
        help="Nombre columna etiqueta (si no existe, se intenta 'label')",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DATA_DIR / "3_preprocessed",
        help="Directorio donde guardar posts-xids.npy, posts-xmask.npy, posts-labels.npy",
    )
    parser.add_argument("--seq-len", type=int, default=512)
    args = parser.parse_args()

    seq_len = args.seq_len
    df = pd.read_excel(args.input)

    text_col = args.text_col if args.text_col in df.columns else "post_description"
    label_col = args.label_col if args.label_col in df.columns else "label"
    if text_col not in df.columns:
        raise SystemExit(f"No se encontró columna de texto. Columnas: {list(df.columns)}")
    if label_col not in df.columns:
        raise SystemExit(f"No se encontró columna de etiqueta. Columnas: {list(df.columns)}")

    initial_df = df[[text_col, label_col]].copy()
    initial_df.rename(columns={text_col: "post_description", label_col: "label"}, inplace=True)
    initial_df = initial_df.loc[initial_df["label"] != "no"]

    if initial_df["label"].dtype == object:
        initial_df["label"] = initial_df["label"].replace(
            {"encontró": "found", "Busca": "searching", "encontro": "found", "busca": "searching"}
        )

    tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
    tokens = tokenizer(
        initial_df["post_description"].tolist(),
        max_length=seq_len,
        truncation=True,
        padding="max_length",
        add_special_tokens=True,
        return_tensors="np",
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with builtins.open(args.out_dir / "posts-xids.npy", "wb") as f:
        np.save(f, tokens["input_ids"])
    with builtins.open(args.out_dir / "posts-xmask.npy", "wb") as f:
        np.save(f, tokens["attention_mask"])

    if initial_df["label"].dtype == object:
        initial_df.loc[initial_df["label"] == "found", "label"] = 1
        initial_df.loc[initial_df["label"] == "searching", "label"] = 0
    arr = initial_df["label"].values.astype("int64")
    labels = np.zeros((arr.size, int(arr.max()) + 1))
    labels[np.arange(arr.size), arr] = 1

    with builtins.open(args.out_dir / "posts-labels.npy", "wb") as f:
        np.save(f, labels)

    print(f"Guardado en {args.out_dir} — muestras: {len(initial_df)}")


if __name__ == "__main__":
    main()
