#!/bin/bash

# Start FastAPI backend on port 8000 (internal)
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to be ready
sleep 5

# Start Streamlit dashboard on port 7860 (exposed by HF Spaces)
streamlit run dashboard/app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false
