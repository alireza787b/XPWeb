# config/config.py
import os
import sys
import json

def setup_xpc_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xpc_path = os.path.join(current_dir, '../resources/XPlaneConnect/Python3/src')
    if xpc_path not in sys.path:
        sys.path.append(xpc_path)

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config
