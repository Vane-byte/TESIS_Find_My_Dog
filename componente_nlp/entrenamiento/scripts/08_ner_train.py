#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrena el modelo NER (BERT multilingual + simpletransformers) con un Excel ya etiquetado.

Columnas esperadas: (row, words, labels) o (row, text, tag).

Equivalente a la parte de entrenamiento del notebook 7NER.ipynb.

El otro modelo NLP del repo es la clasificación de texto; se entrena con
`05_text_classification_train.py` (pipeline de scripts 01–06).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from _paths import DATA_DIR, REPO_ROOT

DEFAULT_TRAIN_EXCEL = DATA_DIR / "2_clean" / "ner" / "tagged_data.xlsx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "Helpers" / "Modelos" / "NEROutputs" / "outputs"


def main():
    parser = argparse.ArgumentParser(
        description="Entrena NER (simpletransformers). Clasificación de texto: 05_text_classification_train.py."
    )
    parser.add_argument(
        "--train-excel",
        type=Path,
        default=DEFAULT_TRAIN_EXCEL,
        help=f"Excel con tags. Por defecto: {DEFAULT_TRAIN_EXCEL}",
    )
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--use-cuda", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Salida del modelo (NERArgs.output_dir). Por defecto: {DEFAULT_OUTPUT_DIR}",
    )
    args = parser.parse_args()

    train_path = Path(args.train_excel)
    if not train_path.is_file():
        raise SystemExit(
            f"No existe el Excel: {train_path.resolve()}\n"
            f"Usa --train-excel o coloca datos en: {DEFAULT_TRAIN_EXCEL}"
        )

    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from simpletransformers.ner import NERArgs, NERModel

    print(f"[08_ner_train] Leyendo: {train_path.resolve()}")
    data = pd.read_excel(train_path)
    if "words" in data.columns and "labels" in data.columns:
        work = data.rename(columns={"words": "text"})
    elif "text" in data.columns and "tag" in data.columns:
        work = data.rename(columns={"tag": "labels"})
    else:
        raise SystemExit(
            "El Excel debe tener ('row','words','labels') o ('row','text','tag'). "
            f"Columnas actuales: {list(data.columns)}"
        )

    if "row" not in work.columns:
        raise SystemExit("Falta columna 'row' (id de frase).")

    if args.max_rows:
        work = work.iloc[: args.max_rows].copy()

    x_train, x_test, y_train, y_test = train_test_split(
        work[["row", "text"]],
        work["labels"],
        test_size=args.test_size,
        random_state=args.seed,
    )
    train_data = pd.DataFrame(
        {"sentence_id": x_train["row"], "words": x_train["text"], "labels": y_train}
    )
    test_data = pd.DataFrame(
        {"sentence_id": x_test["row"], "words": x_test["text"], "labels": y_test}
    )

    label = work["labels"].unique().tolist()
    ner_args = NERArgs()
    ner_args.num_train_epochs = args.epochs
    ner_args.learning_rate = args.lr
    ner_args.overwrite_output_dir = True
    ner_args.train_batch_size = args.batch_size
    ner_args.eval_batch_size = args.batch_size
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ner_args.output_dir = str(args.output_dir)

    print(f"[08_ner_train] output_dir={args.output_dir.resolve()}")
    model = NERModel(
        "bert",
        "bert-base-multilingual-cased",
        labels=label,
        args=ner_args,
        use_cuda=args.use_cuda,
    )
    model.train_model(train_data, eval_data=test_data, acc=accuracy_score)
    result, _model_outputs, _preds_list = model.eval_model(test_data)
    print("Evaluación:", result)
    print(f"[08_ner_train] Modelo y logs en: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
