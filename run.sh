#!/bin/bash

# Lease Abstraction Tool - Startup Script

echo "=========================================="
echo "  Lease Abstraction Tool for Yardi"
echo "=========================================="
echo ""

# Check if running in the correct directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the lease_abstraction_tool directory."
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Create necessary directories
echo "Setting up directories..."
mkdir -p uploads exports

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY environment variable not set."
    echo "The application may not work correctly without it."
    echo ""
fi

echo ""
echo "Starting Lease Abstraction Tool..."
echo "The application will open in your default browser."
echo ""
echo "Press Ctrl+C to stop the application."
echo "=========================================="
echo ""

# Start Streamlit
streamlit run app.py
