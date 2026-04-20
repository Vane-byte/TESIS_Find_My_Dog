#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Equivalente a: componente_nlp/entrenamiento/4DatasetCreation.ipynb

Construye tf.data.Dataset desde los .npy, shuffle/batch y guarda train/val en disco.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
import tensorflow as tf

from _paths import DATA_DIR


def map_func(input_ids, masks, labels):
    return (
        {"input_ids": input_ids, "attention_mask": masks},
        labels,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--npy-dir",
        type=Path,
        default=DATA_DIR / "3_preprocessed",
        help="Directorio con posts-xids.npy, posts-xmask.npy, posts-labels.npy",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DATA_DIR / "4_dataset",
        help="Directorio base; se crean subcarpetas train/ y val/",
    )
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--shuffle-buffer", type=int, default=100)
    parser.add_argument("--train-fraction", type=float, default=0.9)
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="No borrar train/ y val/ antes de guardar (por defecto se vacían para evitar shards viejos).",
    )
    args = parser.parse_args()

    d = args.npy_dir
    with open(d / "posts-xids.npy", "rb") as f:
        xids = np.load(f, allow_pickle=True)
    with open(d / "posts-xmask.npy", "rb") as f:
        xmask = np.load(f, allow_pickle=True)
    with open(d / "posts-labels.npy", "rb") as f:
        labels = np.load(f, allow_pickle=True)
    labels = labels.tolist()

    dataset = tf.data.Dataset.from_tensor_slices((xids, xmask, labels))
    dataset = dataset.map(map_func)
    dataset = dataset.shuffle(args.shuffle_buffer).batch(args.batch_size, drop_remainder=True)

    batch_size = args.batch_size
    split = args.train_fraction
    size = int(xids.shape[0] / batch_size * split)

    train_ds = dataset.take(size)
    val_ds = dataset.skip(size)

    train_path = args.out_dir / "train"
    val_path = args.out_dir / "val"
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if not args.no_clean:
        for p in (train_path, val_path):
            if p.exists():
                print(f"[04] Eliminando salida anterior: {p}")
                shutil.rmtree(p)

    train_ds.save(str(train_path))
    val_ds.save(str(val_path))

    print(f"Train: {train_path}")
    print(f"Val:   {val_path}")


if __name__ == "__main__":
    main()
