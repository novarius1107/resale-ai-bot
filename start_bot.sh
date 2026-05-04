#!/usr/bin/env bash
set -e

echo "Starting AI Reselling Store Bot locally..."

if [ ! -d ".venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
fi

mkdir -p logs data

echo "Starting backend on http://127.0.0.1:8000"
uvicorn app.main:app --reload > logs/backend.log 2>&1 &

echo "Starting dashboard on http://127.0.0.1:8501"
streamlit run dashboard/Home.py
