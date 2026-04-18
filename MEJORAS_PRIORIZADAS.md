# Mejoras priorizadas — Find My Dog (tesis)

Contexto: tres componentes en un solo repositorio (web + NLP + visión), orientado a demostración académica y evolución incremental. Este documento distingue **lo ya hecho** de **lo pendiente** para que sirva de checklist vivo.

---

## Ya abordado (no requiere acción inmediata)

- **Secretos y configuración:** credenciales y rutas sensibles fuera del código; `config.py` lee `.env`; `.gitignore` ignora `.env`.
- **MongoDB en runtime:** `eval_from_mongodb`, scripts de import y de “hot” usan `MONGO_URI`, nombres de BD y colecciones configurables; cliente cerrado con `try`/`finally` tras evaluar.
- **Estructura por componentes:** `componente_web/`, `componente_nlp/inferencia/`, `componente_vision/inferencia/`; pipeline web importa inferencia NLP y visión de forma explícita.
- **Rutas a modelos:** definidas por variables de entorno (valores por defecto relativos al repo); inferencia NER e YOLO con **carga perezosa** (no recrear el modelo en cada llamada).
- **API web básica:** `GET /predict` responde 405; validación de archivo faltante (400); descripción vacía tratada como `""`; rutas de plantillas/estáticos y de imagen de búsqueda con `pathlib`.
- **Puntuación / imágenes:** `saveImage` escribe bajo `componente_web/static/images/` de forma portable.
- **Scripts de datos:** evitar `insert_many` cuando la lista de documentos está vacía (proceso “hot”).
- **README:** comandos de ejecución y estructura de carpetas a alto nivel.

---

## Pendiente — prioridad crítica

| # | Mejora | Estado / notas |
|---|--------|----------------|
| C1 | **Rotar credenciales** de MongoDB si el URI alguna vez quedó en historial Git público o capturas. | Acción manual en Atlas / proveedor. |
| C2 | **Archivo real para YOLO:** colocar el `.pt` en la ruta de `MODEL_YOLO_WEIGHTS_PATH` o corregir la variable. | Sin esto, el paso de detección/recorte falla. |
| C3 | **Instalar y fijar dependencias** del stack ML en un entorno (TensorFlow, transformers, simpletransformers, easyocr, ultralytics, OpenCV, etc.) y documentar versión de Python. | Hoy `requirements.txt` solo lista el mínimo web/datos. |

---

## Pendiente — prioridad alta

| # | Mejora | Estado / notas |
|---|--------|----------------|
| H1 | **Sustituir resultados vía URL** (`/search?data=...`): sesión Flask, `POST` + plantilla, o id corto en servidor / Redis. | Sigue en `main.js` + ruta `/search`; riesgo con payloads grandes. |
| H2 | **No materializar toda la colección** en cada búsqueda (`list(all_regs)` en `eval_from_mongodb`). | Filtrado en Mongo, proyecciones, índices o pre-cálculo de similitud. |
| H3 | **Checklist o pruebas mínimas** documentadas: import raw → process hot → predicción web (incluso manual). | Refuerza reproducibilidad ante tribunal. |
| H4 | **`transformDate` y texto en español:** encoding UTF-8 en fuentes; reemplazar `except:` por excepciones concretas y manejo explícito de fallos. | Archivo: `componente_web/evaluation/register_evaluation.py`. |
| H5 | **Completar README** con prerequisitos ML, tamaño aproximado de modelos y orden estricto de scripts si aplica. | El README actual es base; falta detalle de entorno. |

---

## Pendiente — prioridad media

| # | Mejora | Estado / notas |
|---|--------|----------------|
| M1 | **Poblar `componente_nlp/entrenamiento/` y `componente_vision/entrenamiento/`** (notebooks, scripts o enlaces a artefactos externos citados en la memoria). | Carpetas siguen casi vacías salvo `.gitkeep`. |
| M2 | **`requirements-ml.txt` o `environment.yml`** con versiones pinneadas una vez estable el entorno de la tesis. | Complemento a `requirements.txt`. |
| M3 | **Archivos temporales en visión:** borrar el PNG temporal tras `cv2.imread` (o usar buffer en memoria) en `image_classification.py`. | Reduce basura en disco en Windows. |
| M4 | **Corregir `calcPuntajeRaza`:** rama `else` con variable mal escrita (`mulitplicador`) y revisar que la puntuación coincida con la intención del algoritmo. | Misma lógica de negocio; impacto en el score mostrado. |
| M5 | **Decisión sobre artefactos:** mantener `Helpers/Modelos` en raíz o mover pesos a `componente_nlp/` y `componente_vision/` y actualizar `.env`. | Coherencia con el relato de “tres componentes”. |

---

## Pendiente — prioridad baja (pulido)

| # | Mejora | Estado / notas |
|---|--------|----------------|
| B1 | Sustituir `print` por **`logging`** con niveles. | Backend y scripts. |
| B2 | **Contrato JSON estable** entre front y API (nombres de campos, tipos, cuándo es string vs entero en `SePerdio`). | Mezcla actual perdido/encontrado legible vs flag numérico interno. |
| B3 | **Punto de arranque:** mover `run_web.py` dentro de `componente_web/` si se desea que no quede nada “web” en la raíz salvo `config` (opcional). | Solo organización; no cambia acoplamiento NLP/visión. |
| B4 | Modernizar front (menos CDN legacy jQuery/Bootstrap viejos) si el alcance lo permite. | Opcional para objetivos científicos. |

---

## Nota sobre arquitectura

La división en carpetas es **organizativa**: el servicio web sigue orquestando NLP y visión en un solo proceso. Separar **despliegues** (APIs distintas, contenedores por componente) sería un paso adicional no listado arriba salvo que la memoria lo exija explícitamente.
