"""
Configuración del componente web y datos: MongoDB, colecciones, rutas de importación.
Las rutas de modelos NLP y visión están en `componente_nlp/settings.py` y
`componente_vision/settings.py`.
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

# Rutas a modelos NLP y visión: ver `componente_nlp/settings.py` y `componente_vision/settings.py`
# (así cada componente puede ejecutarse con su propio entorno sin importar `config`).
