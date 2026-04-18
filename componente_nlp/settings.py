"""
Configuración del componente NLP (rutas a modelos).
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


MODEL_TEXT_CLASSIFICATION_DIR = _model_path(
    "MODEL_TEXT_CLASSIFICATION_DIR", "Helpers/Modelos/lost_dogs_model2"
)
MODEL_NER_DIR = _model_path("MODEL_NER_DIR", "Helpers/Modelos/NEROutputs/outputs")
