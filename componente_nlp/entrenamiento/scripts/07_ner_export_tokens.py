#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset preliminar para NER: tokeniza frases con spaCy y genera un Excel (row, text)
sin columna tag — hay que etiquetar después o usar otro flujo.

Equivalente a la parte de exportación del notebook 7NER.ipynb.

Tras anotar `tag`, el entrenamiento NER es `08_ner_train.py`. El modelo de
clasificación de texto es independiente (`05_text_classification_train.py`).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from _paths import DATA_DIR

DEFAULT_INPUT = DATA_DIR / "2_clean" / "complete_clean_data.xlsx"
DEFAULT_OUTPUT = DATA_DIR / "2_clean" / "ner" / "tokens_sin_tag.xlsx"


def main():
    parser = argparse.ArgumentParser(
        description="Exporta tokens por fila de texto (spaCy). Salida sin columna tag."
    )
    parser.add_argument(
        "--input-excel",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Excel con columna 'text'. Por defecto: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Excel de salida (row, text). Por defecto: {DEFAULT_OUTPUT}",
    )
    parser.add_argument("--spacy-model", default="es_core_news_sm")
    args = parser.parse_args()

    in_path = Path(args.input_excel)
    if not in_path.is_file():
        raise SystemExit(
            f"No existe el Excel de entrada: {in_path.resolve()}\n"
            f"Usa --input-excel o coloca el archivo en: {DEFAULT_INPUT}"
        )

    import spacy

    print(f"[07_ner_export_tokens] Entrada: {in_path.resolve()}")
    nlp = spacy.load(args.spacy_model)
    df1 = pd.read_excel(in_path)
    if "text" not in df1.columns:
        raise SystemExit(f"Se espera columna 'text'. Columnas: {list(df1.columns)}")

    rows_out = []
    for row in df1.itertuples():
        doc = nlp(df1.at[row.Index, "text"])
        for token in doc:
            rows_out.append([row.Index, token.text])

    out = pd.DataFrame(rows_out, columns=["row", "text"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_excel(args.output, index=False)
    print(
        "Siguiente paso: añade columna 'tag' (O, PLC, …) en el Excel o copia a tu archivo de entrenamiento.",
        file=sys.stderr,
    )
    print(f"[07_ner_export_tokens] Guardado: {args.output.resolve()}")


if __name__ == "__main__":
    main()
