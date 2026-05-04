#!/usr/bin/env bash
set -e

echo "Starting AI Reselling Store Bot services..."

mkdir -p data logs

# Start backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &

# Start optional scheduler if present
if [ -f "app/scheduler.py" ]; then
  python -m app.scheduler > logs/scheduler.log 2>&1 &
elif [ -f "scheduler.py" ]; then
  python scheduler.py > logs/scheduler.log 2>&1 &
else
  echo "No scheduler module found; skipping scheduler." > logs/scheduler.log
fi

# Start dashboard in foreground
streamlit run dashboard/Home.py --server.address 0.0.0.0 --server.port 8501
