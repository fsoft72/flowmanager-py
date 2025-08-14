#!/bin/bash
# FlowManager Python startup script

echo "Starting FlowManager Python..."

# Check dependencies
echo "Checking dependencies..."
python3 test_install.py

if [ $? -eq 0 ]; then
    echo "Starting production server..."
    ./run_production.py
else
    echo "Dependencies check failed."
    exit 1
fi
