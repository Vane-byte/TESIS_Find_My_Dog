# Find My Dog — Proyecto de tesis

Repositorio único que agrupa **tres componentes independientes** del mismo trabajo de tesis.

## Componente 1 — Sistema web (evaluación)

Servicio que levanta una **plataforma web** para evaluar publicaciones de perros y estimar si hay **match** entre ellos. Se apoya en modelos de **NLP**, **OCR** y **visión por computador**.

## Componente 2 — Modelos NLP

Procesos y código orientados a la **creación y uso** de modelos de procesamiento de lenguaje: **clasificación de texto** y **reconocimiento de entidades (NER)**.

## Componente 3 — Modelos de visión

Procesos y código orientados a la **creación y uso** de modelos de **visión por computador** (por ejemplo detección/clasificación de razas u objetos en imágenes).

---

Los tres bloques conviven en un solo repositorio solo por **organización del proyecto**; no implican un despliegue o pipeline único obligatorio entre ellos.

## Estructura de carpetas (base)

| Carpeta | Rol |
|---------|-----|
| `componente_web/` | Flask (`app.py`), plantillas, estáticos, pipeline de evaluación (`main_pipeline.py`), puntuación (`evaluation/`), scripts Mongo (`scripts/`). |
| `componente_nlp/inferencia/` | Clasificación de texto, NER y OCR usados por el pipeline web. |
| `componente_nlp/entrenamiento/` | Notebooks de entrenamiento NLP; scripts CLI equivalentes en `entrenamiento/scripts/` (`01_test_api.py` … `08_ner_train.py`, ver `--help`). |
| `componente_vision/inferencia/` | Detección/clasificación de raza usada por el pipeline web. |
| `componente_vision/entrenamiento/` | Reservado para entrenamiento de modelos de visión. |
| `Helpers/Modelos/` | Artefactos exportados (rutas configurables en `.env`). |
| `config.py` | MongoDB, colecciones y glob de importación (solo lo que usa el web / scripts de datos). |
| `componente_nlp/settings.py` | Rutas a modelos NLP (mismas variables `MODEL_*` en `.env`). |
| `componente_vision/settings.py` | Rutas a modelos de visión (`MODEL_BREED_*`, `MODEL_YOLO_*`). |

## Ejecución por separado (entornos y configuración)

Hoy el **pipeline completo** sigue viviendo en un solo proceso Python cuando levantas la web: `main_pipeline` llama a inferencia NLP y visión **en memoria**. Para acercarte a componentes realmente independientes puedes:

1. **Tres entornos virtuales** — instala solo lo necesario en cada uno:
   - `pip install -r requirements-web.txt`
   - `pip install -r requirements-nlp.txt`
   - `pip install -r requirements-vision.txt`  
   La demo integrada en Flask **necesita** hoy las tres familias de dependencias en el mismo intérprete que ejecuta `run_web.py`, salvo que sustituyas el pipeline por llamadas HTTP (siguiente paso arquitectónico).

2. **Config partida** — `config.py` ya no define rutas de modelos; NLP y visión leen `componente_nlp/settings.py` y `componente_vision/settings.py` (siguen usando el mismo `.env` en la raíz del repo con `REPO_ROOT`).

3. **Imports perezosos** — `main_pipeline.py` importa NLP/visión solo al ejecutar `processPerritos`, no al importar el módulo del web.

4. **Siguiente paso si quieres procesos distintos** — exponer inferencia como **APIs** (p. ej. FastAPI) en `componente_nlp` y `componente_vision`, y en el web reemplazar las llamadas locales por `requests` hacia URLs en `.env` (`NLP_SERVICE_URL`, `VISION_SERVICE_URL`). Así cada servicio corre en su contenedor o máquina con su propio `requirements-*`.

## Entorno virtual válido (Python 3.12)

**No uses Python 3.14** para NLP/visión: TensorFlow no publica ruedas para 3.14 y `pip install tensorflow` fallará.

En el repo puede existir una carpeta **`.venv`** creada con el Python **3.12** de Miniconda (ajusta la ruta si tu Miniconda está en otro sitio):

```powershell
cd ruta\al\TESIS_Find_My_Dog
# Crear (o recrear) el venv con 3.12
& "$env:USERPROFILE\miniconda3\python.exe" -m venv .venv --clear
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-nlp.txt
```

Si tienes **varias versiones** instaladas con el launcher de Windows:

```powershell
py -3.12 -m venv .venv
```

**Activar** antes de trabajar:

```powershell
.\.venv\Scripts\Activate.ps1
python --version   # debe mostrar 3.12.x
```

Si `pip install` devuelve **WinError 32** (“archivo en uso”), cierra otras terminales o procesos que estén usando `.venv` (otro `pip`, Jupyter, etc.), vuelve a activar el venv y ejecuta `pip install -r requirements-nlp.txt` otra vez.

## Configuración y ejecución (desde la raíz del repo)

1. Copiar o editar `.env` (ver claves en el archivo; no versionar secretos reales en Git).
2. Web: `python run_web.py` o `python -m componente_web.app`
3. Importar imágenes a `Raw_dogs`: `python -m componente_web.scripts.import_mongodb`
4. Refrescar colecciones calientes: `python -m componente_web.scripts.process_raw_mongodb`

Requisito: ejecutar comandos con el **directorio de trabajo en la raíz del repositorio** para que `import config` y los paquetes `componente_*` resuelvan correctamente.
