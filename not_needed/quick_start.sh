#!/bin/bash

echo "🚀 QUICK START - Running WITHOUT Docker (SQLite mode)"
echo "======================================================"

# Update .env for SQLite
cat > .env << 'EOF'
# Database Configuration (SQLite - no Docker needed)
DATABASE_URL=sqlite:///./mednotes.db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=quick-start-secret-key-for-development-12345678
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration (optional for now)
OPENAI_API_KEY=sk-test-key

# Application Settings
DEBUG=True
ENVIRONMENT=development
EOF

echo "✅ Configuration updated for SQLite"
echo ""
echo "📦 Installing dependencies..."
pip3 install fastapi uvicorn streamlit sqlalchemy pydantic python-jose passlib python-multipart bcrypt 2>&1 | grep -E "(Successfully|already satisfied)" | tail -5

echo ""
echo "✅ Ready to start!"
echo ""
echo "Now run these commands in 2 separate terminals:"
echo ""
echo "Terminal 1: uvicorn api.main:app --reload"
echo "Terminal 2: streamlit run ui/app.py"
echo ""
