#!/usr/bin/env bash

pip install -r requirements.txt

streamlit run dashboard/Home.py \
  --server.port $PORT \
  --server.address 0.0.0.0
