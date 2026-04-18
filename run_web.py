"""
Arranque rápido del componente web. Desde la raíz del repositorio:

    python run_web.py
"""
from componente_web.app import app

if __name__ == "__main__":
    app.run(debug=False, threaded=False)
