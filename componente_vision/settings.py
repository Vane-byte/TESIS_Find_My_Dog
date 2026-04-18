"""
Configuración del componente visión (rutas a modelos).
Carga `.env` desde la raíz del repositorio para poder ejecutar solo este componente.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")


def _model_path(env_key: str, default_relative: str) -> Path:
    rel = os.getenv(env_key, default_relative).strip()
    return (REPO_ROOT / rel).resolve()


MODEL_BREED_KERAS_PATH = _model_path("MODEL_BREED_KERAS_PATH", "Helpers/Modelos/RESENTV2.h5")
MODEL_YOLO_WEIGHTS_PATH = _model_path("MODEL_YOLO_WEIGHTS_PATH", "Helpers/Modelos/yolov8n.pt")
