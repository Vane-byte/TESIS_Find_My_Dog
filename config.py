"""
Configuración compartida: carga `.env` en la raíz del repositorio y expone URI de MongoDB,
nombres de colección y rutas a artefactos de modelos (relativas al proyecto).
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


def _require_env(key: str) -> str:
    value = os.getenv(key)
    if value is None or not str(value).strip():
        raise RuntimeError(f"Variable de entorno obligatoria no definida: {key}")
    return str(value).strip()


MONGO_URI = _require_env("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Tesis").strip()
MONGO_COLLECTION_RAW = os.getenv("MONGO_COLLECTION_RAW", "Raw_dogs").strip()
MONGO_COLLECTION_HOT_LOST = os.getenv("MONGO_COLLECTION_HOT_LOST", "Hot_Dogs_Lost").strip()
MONGO_COLLECTION_HOT_FOUND = os.getenv("MONGO_COLLECTION_HOT_FOUND", "Hot_Dogs_Found").strip()

RAW_DOGS_GLOB = os.getenv("RAW_DOGS_GLOB", "uploads/*").strip()


def _model_path(env_key: str, default_relative: str) -> Path:
    rel = os.getenv(env_key, default_relative).strip()
    return (PROJECT_ROOT / rel).resolve()


MODEL_TEXT_CLASSIFICATION_DIR = _model_path(
    "MODEL_TEXT_CLASSIFICATION_DIR", "Helpers/Modelos/lost_dogs_model2"
)
MODEL_NER_DIR = _model_path("MODEL_NER_DIR", "Helpers/Modelos/NEROutputs/outputs")
MODEL_BREED_KERAS_PATH = _model_path("MODEL_BREED_KERAS_PATH", "Helpers/Modelos/RESENTV2.h5")
MODEL_YOLO_WEIGHTS_PATH = _model_path("MODEL_YOLO_WEIGHTS_PATH", "Helpers/Modelos/yolov8n.pt")
