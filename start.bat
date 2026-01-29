@echo off
echo ==================================
echo ArXiv Similarity Search - Startup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create frontend directory if it doesn't exist
if not exist "frontend" (
    echo.
    echo 📁 Creating frontend directory...
    mkdir frontend\static\css
    mkdir frontend\static\js
)

REM Check if frontend/index.html exists
if not exist "frontend\index.html" (
    echo.
    echo ⚠️  WARNING: frontend\index.html not found!
    echo Please create this file before starting the server.
    echo.
)

REM Create necessary directories
echo.
echo 📁 Creating necessary directories...
if not exist "data\temp_pdfs" mkdir data\temp_pdfs
if not exist "data\sample_pdfs" mkdir data\sample_pdfs
if not exist "data\local_database" mkdir data\local_database
if not exist "data\faiss_indices" mkdir data\faiss_indices
if not exist "outputs" mkdir outputs
if not exist "logs" mkdir logs

echo.
echo ==================================
echo ✅ Setup Complete!
echo ==================================
echo.
echo Starting FastAPI server...
echo.
echo Access the application at:
echo   🌐 http://localhost:8000
echo.
echo API Documentation:
echo   📚 http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ==================================
echo.

REM Start the server
python main.py

pause