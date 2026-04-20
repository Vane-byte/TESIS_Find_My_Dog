# Componente NLP — Find My Dog

Aquí vive el **NLP de la tesis**: inferencia usada por el sistema web y **entrenamiento** (notebooks + scripts CLI).

## Estructura

| Ruta | Contenido |
|------|-----------|
| `inferencia/` | Clasificación de texto (BERT), NER, OCR (EasyOCR). Lo importa el componente web cuando corres la app completa. |
| `settings.py` | Rutas a modelos (`MODEL_TEXT_CLASSIFICATION_DIR`, `MODEL_NER_DIR`). Lee el `.env` en la **raíz del repositorio**. |
| `entrenamiento/` | Notebooks, carpeta `data/` y scripts en `entrenamiento/scripts/`. |

## Entorno e instalación

Desde la **raíz del repo** (`TESIS_Find_My_Dog/`):

```bash
pip install -r requirements-nlp.txt
```

Si además vas a correr la web en el mismo entorno, puedes usar el meta-fichero de la raíz: `pip install -r requirements.txt`.

## Variables de entorno (`.env` en la raíz del repo)

El componente NLP usa principalmente:

| Variable | Uso |
|----------|-----|
| `MODEL_TEXT_CLASSIFICATION_DIR` | Ruta relativa al repo del SavedModel de clasificación (por defecto `Helpers/Modelos/lost_dogs_model2`). |
| `MODEL_NER_DIR` | Carpeta del modelo NER (simpletransformers), por defecto `Helpers/Modelos/NEROutputs/outputs`. |

Para el script de Twitter:

| Variable | Uso |
|----------|-----|
| `TWITTER_BEARER_TOKEN` | Obligatoria para `01_test_api.py` (no pongas el token en el código). |

## Cómo ejecutar los scripts de entrenamiento

Trabaja siempre con el **directorio de trabajo en la raíz del repositorio** y llama al script con ruta relativa (así `import _paths` dentro de `scripts/` resuelve bien).

**Regla general:** casi todos los parámetros son **opcionales**; cada script trae valores por defecto bajo `entrenamiento/data/`. Si tus archivos están en otra ruta, pásalos con las flags que indica `--help`.

```bash
cd ruta/al/TESIS_Find_My_Dog
python componente_nlp/entrenamiento/scripts/NOMBRE_SCRIPT.py --help
```

### Dos modelos NLP (scripts distintos)

| Modelo | Scripts |
|--------|---------|
| **Clasificación de texto** (BERT + Keras, SavedModel) | `01` → `06` en la tabla siguiente; el entrenamiento es `05_text_classification_train.py`. |
| **NER** (BERT + simpletransformers) | `07_ner_export_tokens.py` (tokens sin tag) → anotar → `08_ner_train.py`. |

### Orden típico del pipeline (clasificación de texto)

1. `01_test_api.py` — descarga tweets (opcional).  
2. `02_data_cleaning_main.py` — limpia CSV.  
3. `03_data_preprocessing.py` — Excel etiquetado → `.npy`.  
4. `04_dataset_creation.py` — `.npy` → `tf.data` train/val.  
5. `05_text_classification_train.py` — entrena y guarda SavedModel.  
6. `06_load_and_predict.py` — prueba el modelo de clasificación (texto o CSV).

Ejecuta **uno a la vez**; cuando termine, el siguiente.

---

### `01_test_api.py`

| Parámetro | ¿Obligatorio? | Default / notas |
|-----------|----------------|-----------------|
| `--query` | No | Query de búsqueda en X API. |
| `--out` | No | `entrenamiento/data/1_raw/extracc_twitter.csv` |
| Entorno `TWITTER_BEARER_TOKEN` | **Sí** | Bearer de la API v2. |

```bash
python componente_nlp/entrenamiento/scripts/01_test_api.py
python componente_nlp/entrenamiento/scripts/01_test_api.py --out entrenamiento/data/1_raw/mi_muestra.csv
```

---

### `02_data_cleaning_main.py`

| Parámetro | ¿Obligatorio? | Default |
|-----------|----------------|---------|
| `--input` | No | `entrenamiento/data/1_raw/extracc_twitter_4.csv` |
| `--output` | No | `entrenamiento/data/2_clean/data_cleaning.xlsx` |

El CSV debe tener columna **`text`**.

```bash
python componente_nlp/entrenamiento/scripts/02_data_cleaning_main.py --input entrenamiento/data/1_raw/mi.csv --output entrenamiento/data/2_clean/salida.xlsx
```

---

### `03_data_preprocessing.py`

| Parámetro | ¿Obligatorio? | Default |
|-----------|----------------|---------|
| `--input` | No | `entrenamiento/data/2_clean/complete_clean_data.xlsx` |
| `--text-col` | No | `text` (si no existe, intenta `post_description`) |
| `--label-col` | No | `tipoPost` (si no existe, intenta `label`) |
| `--out-dir` | No | `entrenamiento/data/3_preprocessed` |
| `--seq-len` | No | `512` |

Genera `posts-xids.npy`, `posts-xmask.npy`, `posts-labels.npy` en `--out-dir`.

```bash
python componente_nlp/entrenamiento/scripts/03_data_preprocessing.py --input entrenamiento/data/2_clean/mi_etiquetado.xlsx
```

---

### `04_dataset_creation.py`

| Parámetro | ¿Obligatorio? | Default |
|-----------|----------------|---------|
| `--npy-dir` | No | `entrenamiento/data/3_preprocessed` |
| `--out-dir` | No | `entrenamiento/data/4_dataset` (crea `train/` y `val/`) |
| `--batch-size` | No | `16` |
| `--shuffle-buffer` | No | `100` |
| `--train-fraction` | No | `0.9` |
| `--no-clean` | No | Si **no** lo pasas, se borran `train/` y `val/` antes de guardar (evita mezclar shards viejos de TensorFlow con correlativos nuevos). |

```bash
python componente_nlp/entrenamiento/scripts/04_dataset_creation.py
```

---

### `05_text_classification_train.py`

Entrena el **modelo de clasificación de texto** (no NER; para NER usa `08_ner_train.py`).

| Parámetro | ¿Obligatorio? | Default |
|-----------|----------------|---------|
| `--dataset-dir` | No | `entrenamiento/data/4_dataset` (debe existir `train/` y `val/`) |
| `--output` | No | `Helpers/Modelos/lost_dogs_model_trained` (raíz del repo) |
| `--batch-size`, `--epochs`, `--learning-rate`, `--seq-len` | No | Ver `--help` |

```bash
python componente_nlp/entrenamiento/scripts/05_text_classification_train.py --epochs 6
```

---

### `06_load_and_predict.py`

| Parámetro | ¿Obligatorio? | Default / notas |
|-----------|----------------|-----------------|
| `--model` | No | `Helpers/Modelos/lost_dogs_model2` |
| `--text` | Uno de los dos | Si lo pasas, una sola predicción por consola. |
| `--csv` | Uno de los dos | CSV con columna de texto (por defecto `text`). |
| `--csv-text-col` | No | `text` |
| `--out` | No | Si usas `--csv`, por defecto guarda `*_predicted.csv` junto al entrada. |

```bash
python componente_nlp/entrenamiento/scripts/06_load_and_predict.py --text "Se perdió mi perro en Lima"
python componente_nlp/entrenamiento/scripts/06_load_and_predict.py --csv entrenamiento/data/2_clean/mi.csv --csv-text-col text
```

---

### `07_ner_export_tokens.py`

Tokeniza textos con spaCy y genera un Excel **sin** etiquetas NER (`row`, `text`). Útil como base antes de anotar `tag`.

| Parámetro | ¿Obligatorio? | Default |
|-----------|----------------|---------|
| `--input-excel` | No | `entrenamiento/data/2_clean/complete_clean_data.xlsx` |
| `--output` | No | `entrenamiento/data/2_clean/ner/tokens_sin_tag.xlsx` |
| `--spacy-model` | No | `es_core_news_sm` |

```bash
python componente_nlp/entrenamiento/scripts/07_ner_export_tokens.py
```

---

### `08_ner_train.py`

Entrena NER con simpletransformers a partir de un Excel **ya etiquetado** (columnas `(row, words, labels)` o `(row, text, tag)`).

| Parámetro | ¿Obligatorio? | Default / notas |
|-----------|----------------|-----------------|
| `--train-excel` | No | `entrenamiento/data/2_clean/ner/tagged_data.xlsx` |
| `--max-rows` | No | Limita filas (útil para pruebas). |
| `--test-size`, `--seed`, `--epochs`, `--lr`, `--batch-size` | No | Ver `--help`. |
| `--use-cuda` | No | Flag; sin él usa CPU. |
| `--output-dir` | No | `Helpers/Modelos/NEROutputs/outputs` (raíz del repo; alineado con inferencia). |

```bash
python componente_nlp/entrenamiento/scripts/08_ner_train.py
python componente_nlp/entrenamiento/scripts/08_ner_train.py --train-excel ruta/al/archivo_etiquetado.xlsx
```

---

## Inferencia (sin scripts aparte)

La app web importa `componente_nlp.inferencia.*` al procesar un registro. No hay un servidor NLP independiente en este repo; para ejecutar “solo inferencia” sueles usar **la web** o un notebook / REPL importando esas funciones.

## Notas

- Los scripts asumen rutas bajo `entrenamiento/data/` coherentes con los defaults; si cambias nombres de carpetas, usa siempre `--input`, `--out-dir`, etc.
- Si un script falla por dependencia faltante, revisa `requirements-nlp.txt` y tu versión de Python (3.9–3.11 suele ser lo más compatible con TensorFlow 2.x).
