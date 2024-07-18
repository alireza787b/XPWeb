# app/main.py
import sys
import os

# Add the project's root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from config.config import load_config
from core.fastapi_app import create_app

if __name__ == "__main__":
    import uvicorn

    config = load_config()
    app = create_app()
    host = config['server']['host']
    port = config['server']['port']

    uvicorn.run(app, host=host, port=port)
