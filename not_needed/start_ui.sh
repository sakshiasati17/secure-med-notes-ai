#!/bin/bash
cd /Users/sukritisehgal/secure-med-notes-ai
source venv/bin/activate
echo "🎨 Starting UI Server on http://localhost:8501"
streamlit run ui/app.py --server.port 8501
