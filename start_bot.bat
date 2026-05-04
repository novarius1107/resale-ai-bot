@echo off
echo Starting AI Reselling Store Bot locally...

IF NOT EXIST .venv (
  echo Creating Python virtual environment...
  python -m venv .venv
)

call .venv\Scripts\activate

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

IF NOT EXIST .env (
  echo Creating .env from .env.example...
  copy .env.example .env
)

IF NOT EXIST logs mkdir logs
IF NOT EXIST data mkdir data

echo Starting backend on http://127.0.0.1:8000
start "Resale Bot Backend" cmd /k "call .venv\Scripts\activate && uvicorn app.main:app --reload"

echo Starting dashboard on http://127.0.0.1:8501
streamlit run dashboard/Home.py
