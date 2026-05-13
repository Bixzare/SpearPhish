# SpearPhish App

A comprehensive phishing detection system combining machine learning and link analysis to identify and classify phishing emails and URLs.

## Project Overview

SpearPhish is a full-stack application consisting of:
- **Backend**: FastAPI-based REST API with NLP models for phishing detection
- **Frontend**: React + Vite web interface for interacting with the detection system

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js v16+
- npm v7+

### One-Command Setup

Run both backend and frontend servers with a single command:

**Windows (PowerShell):**
```bash
.\run.ps1
```

**macOS/Linux:**
```bash
./run.sh
```

This will:
1. Activate the Python virtual environment
2. Start the FastAPI backend server on `http://localhost:8000`
3. Start the React frontend development server on `http://localhost:5173`

Both servers will run in separate terminal windows.

## Manual Installation

For detailed installation instructions, see:
- [Backend Installation](backend/README.md)
- [Frontend Installation](frontend/project-spearphish/README.md)

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend/project-spearphish
npm install
npm run dev
```

## Accessing the Application

Once both servers are running:

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

## Project Structure

```
SpearPhish App/
├── backend/
│   ├── main.py
│   ├── text_classification.py
│   ├── link_analysis.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   └── project-spearphish/
│       ├── src/
│       ├── package.json
│       └── README.md
├── .gitignore
└── README.md
```

## Technologies

### Backend
- **FastAPI** - Modern web framework for building APIs
- **scikit-learn** - Machine learning
- **XGBoost** - Gradient boosting
- **NLTK** - Natural Language Processing
- **BeautifulSoup4** - Web scraping
- **python-whois** - WHOIS lookups

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **JavaScript** - Client-side logic

## Stopping the Servers

To stop the servers:
1. In the backend terminal: Press `Ctrl+C`
2. In the frontend terminal: Press `Ctrl+C`

## Troubleshooting

- **Port conflicts**: If ports 8000 or 5173 are in use, see the README files for alternative port configurations
- **Virtual environment issues**: Ensure `.venv` is properly activated before running
- **Node modules missing**: Run `npm install` in the frontend directory
- **Missing Python dependencies**: Run `pip install -r requirements.txt` in the backend directory

## License

[Add your license information here]

## Contact

[Add contact information here]
