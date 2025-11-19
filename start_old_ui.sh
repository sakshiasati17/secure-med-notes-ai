#!/bin/bash

# Start Old Streamlit UI
echo "🏥 Starting Streamlit UI (Old)"
echo "================================"
echo ""

# Start Docker
echo "Starting Docker services..."
docker compose up -d
echo "✅ Docker running"
echo ""

# Start FastAPI
echo "Starting FastAPI backend..."
source .venv/bin/activate && python -m uvicorn api.main:app --reload --port 8000 &
echo "✅ FastAPI running on port 8000"
echo ""

# Start Streamlit
echo "Starting Streamlit UI..."
streamlit run old_ui/app.py --server.port 8501
