# SpearPhish App - Backend

A FastAPI-based backend application for the SpearPhish phishing detection system using NLP and machine learning models.

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Step-by-Step Installation

**Step 1: Navigate to the backend directory**
```bash
cd backend
```

**Step 2: Create a virtual environment**

On Windows (PowerShell):
```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 3: Upgrade pip**
```bash
pip install --upgrade pip
```

**Step 4: Install required dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Run the application**

Start the FastAPI server:
```bash
python main.py
```

Or run with Uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── main.py                    - FastAPI application entry point
├── text_classification.py     - NLP text classification models
├── link_analysis.py           - Link analysis utilities
├── requirements.txt           - Python dependencies
├── L1 App.ipynb              - L1 model notebook
├── L2 App.ipynb              - L2 model notebook
├── backend_notebook.ipynb    - Backend experiment notebook
└── *.pkl                      - Trained model files
```

## Required Dependencies

- **fastapi** - Web framework for building APIs
- **uvicorn[standard]** - ASGI server
- **scikit-learn** - Machine learning library
- **xgboost** - Gradient boosting framework
- **nltk** - Natural Language Toolkit
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scipy** - Scientific computing
- **beautifulsoup4** - HTML/XML parsing
- **requests** - HTTP library
- **python-whois** - WHOIS lookup
- **joblib** - Serialization

## Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:
```bash
deactivate
```

## Troubleshooting

- **ModuleNotFoundError**: Ensure your virtual environment is activated and all dependencies are installed
- **Port already in use**: Change the port with `uvicorn main:app --reload --port 8001`
- **Permission denied** (on macOS/Linux): Run `chmod +x .venv/bin/activate` before activating
- **Model files missing**: Ensure `.pkl` files are in the backend directory before running

## API Endpoints

Once the server is running, you can access the API documentation at `http://localhost:8000/docs` to view and test available endpoints.
