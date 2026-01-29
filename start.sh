#!/bin/bash

echo "=================================="
echo "ArXiv Similarity Search - Startup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create frontend directory if it doesn't exist
if [ ! -d "frontend" ]; then
    echo ""
    echo "📁 Creating frontend directory..."
    mkdir -p frontend/static/css frontend/static/js
fi

# Check if frontend/index.html exists
if [ ! -f "frontend/index.html" ]; then
    echo ""
    echo "⚠️  WARNING: frontend/index.html not found!"
    echo "Please create this file before starting the server."
    echo ""
fi

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p data/temp_pdfs data/sample_pdfs data/local_database data/faiss_indices outputs logs

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Starting FastAPI server..."
echo ""
echo "Access the application at:"
echo "  🌐 http://localhost:8000"
echo ""
echo "API Documentation:"
echo "  📚 http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="
echo ""

# Start the server
python3 main.py