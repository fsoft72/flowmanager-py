#!/bin/bash
# FlowManager Python development startup with virtual environment

echo "Starting FlowManager Python (Development - HTTP only)..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo "🐍 Activating virtual environment..."
source venv/bin/activate

echo "🔧 Starting development server on http://localhost:7183"
python -c "
import uvicorn
from main import app, cfg
uvicorn.run('main:app', host='localhost', port=cfg['port'], reload=True)
"
