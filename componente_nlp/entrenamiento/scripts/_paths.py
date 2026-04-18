"""Rutas base para scripts de entrenamiento NLP."""
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
ENTRENAMIENTO_DIR = SCRIPTS_DIR.parent
DATA_DIR = ENTRENAMIENTO_DIR / "data"
# componente_nlp/entrenamiento -> repo raíz = parent.parent
REPO_ROOT = ENTRENAMIENTO_DIR.parent.parent
