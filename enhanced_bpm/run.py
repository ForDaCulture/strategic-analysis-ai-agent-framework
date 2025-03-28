#!/usr/bin/env python3
"""
Run script for the BPM Principles Explorer application.
This script starts the Flask web server.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the Flask app
from web.app import app

if __name__ == '__main__':
    print("Starting BPM Principles Explorer...")
    print("Open your browser and navigate to http://127.0.0.1:5000/")
    app.run(debug=True)