#!/bin/bash

# Mechelen Train Station Kiosk Startup Script

echo "Starting Mechelen Train Station Kiosk..."
echo "========================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv .venv
    echo "Installing dependencies..."
    .venv/bin/pip install -r requirements.txt
fi

# Activate virtual environment and start the application
echo "Starting Flask application..."
echo "Open your browser to http://localhost:5000"
echo "Press Ctrl+C to stop the application"
echo ""

.venv/bin/python app.py
