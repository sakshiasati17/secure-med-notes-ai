#!/bin/bash

echo "🏥 Starting Secure Medical Notes AI..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mednotes
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-this-in-production-$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Application Settings
DEBUG=True
ENVIRONMENT=development
EOF
    echo "✅ .env file created. Please update with your actual values."
fi

# Start Docker services
echo "🐳 Starting Docker services (PostgreSQL + Redis)..."
docker compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations and seed data
echo "🗄️  Setting up database..."
python api/seed_more_data.py

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "1. Start API: uvicorn api.main:app --reload"
echo "2. Start UI: streamlit run ui/app.py"
echo ""
echo "📱 Access points:"
echo "- API: http://localhost:8000"
echo "- UI: http://localhost:8501"
echo "- API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 Test credentials:"
echo "- Doctor: dr.smith@hospital.com / password123"
echo "- Nurse: nurse.johnson@hospital.com / password123"
echo "- Admin: admin@hospital.com / password123"
