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
| `componente_nlp/entrenamiento/` | Reservado para notebooks/scripts de entrenamiento NLP. |
| `componente_vision/inferencia/` | Detección/clasificación de raza usada por el pipeline web. |
| `componente_vision/entrenamiento/` | Reservado para entrenamiento de modelos de visión. |
| `Helpers/Modelos/` | Artefactos exportados (rutas configurables en `.env`). |
| `config.py` | Carga `.env` y expone URI MongoDB, colecciones y rutas a modelos. |

## Configuración y ejecución (desde la raíz del repo)

1. Copiar o editar `.env` (ver claves en el archivo; no versionar secretos reales en Git).
2. Web: `python run_web.py` o `python -m componente_web.app`
3. Importar imágenes a `Raw_dogs`: `python -m componente_web.scripts.import_mongodb`
4. Refrescar colecciones calientes: `python -m componente_web.scripts.process_raw_mongodb`

Requisito: ejecutar comandos con el **directorio de trabajo en la raíz del repositorio** para que `import config` y los paquetes `componente_*` resuelvan correctamente.
