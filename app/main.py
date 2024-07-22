import sys
import os
import uvicorn

# Ensure the path for X-Plane Connect is set up correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from config.config import setup_xpc_path, load_config
setup_xpc_path()  # Call this early to ensure the path is set

from core.fastapi_app import create_app

def print_welcome_message(host, port):
    welcome_message = f"""
    ********************************************
    *         Welcome to XPWeb API Server      *
    ********************************************
    XPWeb is a REST API for interfacing with X-Plane via X-Plane Connect.
    
    Server is running on:
    Host: {host}
    Port: {port}

    API Documentation: http://{host}:{port}/docs
    GitHub Repository: https://github.com/alireza787b/XPWeb

    Press CTRL+C to quit.
    """
    print(welcome_message)

if __name__ == "__main__":
    print("Starting XPWeb API Server...")
    try:
        print("Loading configuration...")
        config = load_config()
        print("Configuration loaded successfully.")
        
        app = create_app()
        host = config['server']['host']
        port = config['server']['port']

        print_welcome_message(host, port)
        print("Starting Uvicorn server...")
        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")

    input("Press Enter to exit...")  # Keeps the console open
