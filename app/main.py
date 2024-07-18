# app/main.py
import sys
import os

# Add the project's root directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from app.api.endpoints import FastAPIHandler

if __name__ == "__main__":
    handler = FastAPIHandler()
    handler.start()
