#!/bin/bash

echo "🏥 Secure Medical Notes AI - Startup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Creating .env file..."
    cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mednotes
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-this-in-production-changeme123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Application Settings
DEBUG=True
ENVIRONMENT=development
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
fi

# Check Docker
echo ""
echo "1️⃣  Checking Docker..."
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running!${NC}"
    echo -e "${YELLOW}Please start Docker Desktop and run this script again.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Docker is running${NC}"
fi

# Start Docker services
echo ""
echo "2️⃣  Starting PostgreSQL and Redis..."
docker compose up -d
sleep 5

# Check if containers are running
if docker ps | grep -q postgres; then
    echo -e "${GREEN}✅ PostgreSQL is running${NC}"
else
    echo -e "${RED}❌ PostgreSQL failed to start${NC}"
fi

if docker ps | grep -q redis; then
    echo -e "${GREEN}✅ Redis is running${NC}"
else
    echo -e "${RED}❌ Redis failed to start${NC}"
fi

# Check Python packages
echo ""
echo "3️⃣  Checking Python dependencies..."
if python3 -c "import fastapi, streamlit, sqlalchemy" 2>/dev/null; then
    echo -e "${GREEN}✅ Core dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

# Seed database
echo ""
echo "4️⃣  Setting up database..."
python3 api/seed_more_data.py

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "🚀 To start the application, open TWO terminals:"
echo ""
echo "Terminal 1 - API Server:"
echo -e "${YELLOW}  uvicorn api.main:app --reload --port 8000${NC}"
echo ""
echo "Terminal 2 - UI Server:"
echo -e "${YELLOW}  streamlit run ui/app.py --server.port 8501${NC}"
echo ""
echo "📱 Then access:"
echo "  - UI: http://localhost:8501"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "👤 Default login:"
echo "  Doctor - Email: doctor@hospital.com | Password: doctor123"
echo "  Nurse - Email: nurse@hospital.com | Password: nurse123"
echo ""
