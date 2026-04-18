#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Equivalente a: componente_nlp/entrenamiento/2dataCleaning_main.ipynb

Limpieza de texto: URLs, saltos de línea, emojis (clean-text), menciones, etc.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
from cleantext import clean

from _paths import DATA_DIR


def clean_text_cell(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\n", ". ", text)
    text = clean(
        text,
        to_ascii=False,
        no_emoji=True,
        normalize_whitespace=True,
        lower=False,
        lang="es",
    )
    text = re.sub(r"#", "", text)
    text = re.sub(r"@\S+", "USER_ID", text)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=DATA_DIR / "1_raw" / "extracc_twitter_4.csv",
        help="CSV con columna 'text' (sep ;)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DATA_DIR / "2_clean" / "data_cleaning.xlsx",
        help="Excel de salida",
    )
    args = parser.parse_args()

    pd.set_option("display.max_colwidth", None)
    df = pd.read_csv(args.input, sep=";", encoding="utf-8", on_bad_lines="skip")
    if "text" not in df.columns:
        raise SystemExit(f"El CSV debe tener columna 'text'. Columnas: {list(df.columns)}")

    df = pd.DataFrame(df["text"].copy())
    for row in df.itertuples():
        df.at[row.Index, "text"] = clean_text_cell(df.at[row.Index, "text"])
    df = df.drop_duplicates()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(args.output, index=False)
    print(f"Guardado: {args.output} ({len(df)} filas)")


if __name__ == "__main__":
    main()
