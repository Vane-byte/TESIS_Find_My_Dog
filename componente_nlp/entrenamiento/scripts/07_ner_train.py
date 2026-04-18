#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Equivalente a: componente_nlp/entrenamiento/7NER.ipynb (entrenamiento con simpletransformers).

Parte A — exportar tokens por oración con spaCy (opcional).
Parte B — entrenar NERModel a partir de un Excel con columnas (row, words, labels) o (row, text, tag).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from _paths import DATA_DIR, ENTRENAMIENTO_DIR


def cmd_export_tokens(args):
    import spacy

    nlp = spacy.load(args.spacy_model)
    df1 = pd.read_excel(args.input_excel)
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
        "Etiquetado a nivel token requerido para NER: añade columna 'tag' (O, PLC, …) "
        "en el Excel exportado o usa un archivo ya anotado.",
        file=sys.stderr,
    )
    print(f"Tokens exportados (sin tags): {args.output}")


def cmd_train(args):
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from simpletransformers.ner import NERArgs, NERModel

    data = pd.read_excel(args.train_excel)
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

    model = NERModel(
        "bert",
        "bert-base-multilingual-cased",
        labels=label,
        args=ner_args,
        use_cuda=args.use_cuda,
    )
    model.train_model(train_data, eval_data=test_data, acc=accuracy_score)
    result, _model_outputs, preds_list = model.eval_model(test_data)
    print("Evaluación:", result)
    print(f"Modelo y logs en: {args.output_dir}")
    return preds_list


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_exp = sub.add_parser("export-tokens", help="Tokenización con spaCy → Excel (sin etiquetas NER)")
    p_exp.add_argument("--input-excel", type=Path, required=True)
    p_exp.add_argument(
        "--output",
        type=Path,
        default=DATA_DIR / "2_clean" / "ner" / "tokens_sin_tag.xlsx",
    )
    p_exp.add_argument("--spacy-model", default="es_core_news_sm")

    p_tr = sub.add_parser("train", help="Entrenar NER con simpletransformers")
    p_tr.add_argument("--train-excel", type=Path, required=True)
    p_tr.add_argument("--max-rows", type=int, default=None)
    p_tr.add_argument("--test-size", type=float, default=0.2)
    p_tr.add_argument("--seed", type=int, default=42)
    p_tr.add_argument("--epochs", type=int, default=20)
    p_tr.add_argument("--lr", type=float, default=1e-4)
    p_tr.add_argument("--batch-size", type=int, default=32)
    p_tr.add_argument("--use-cuda", action="store_true")
    p_tr.add_argument(
        "--output-dir",
        type=Path,
        default=ENTRENAMIENTO_DIR / "artifacts" / "ner_output",
        help="Solo informativo; simpletransformers usa output_dir del NERArgs por defecto",
    )

    args = parser.parse_args()
    if args.command == "export-tokens":
        cmd_export_tokens(args)
    elif args.command == "train":
        cmd_train(args)


if __name__ == "__main__":
    main()
