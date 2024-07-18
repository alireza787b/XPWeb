# config/config.py
import os
import sys

def setup_xpc_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xpc_path = os.path.join(current_dir, '../resources/XPlaneConnect/Python3/src')
    if xpc_path not in sys.path:
        sys.path.append(xpc_path)
