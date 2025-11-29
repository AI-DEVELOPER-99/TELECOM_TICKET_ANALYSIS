#!/bin/bash

# Telecom Ticket Analysis - Quick Setup Script
# This script automates the setup process for both backend and frontend

set -e  # Exit on error

echo "════════════════════════════════════════════════════════════"
echo "  Telecom Ticket Analysis Assistant - Setup Script"
echo "════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 14 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and Node.js are installed${NC}"
echo ""

# Backend Setup
echo "────────────────────────────────────────────────────────────"
echo "Setting up Backend..."
echo "────────────────────────────────────────────────────────────"

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Setup .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env and add your OPENAI_API_KEY${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

cd ..

# Frontend Setup
echo ""
echo "────────────────────────────────────────────────────────────"
echo "Setting up Frontend..."
echo "────────────────────────────────────────────────────────────"

cd frontend

# Install Node dependencies
echo "Installing Node.js dependencies..."
npm install
echo -e "${GREEN}✓ Node.js dependencies installed${NC}"

# Setup .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓ Frontend .env created${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

cd ..

# Final instructions
echo ""
echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Add your OpenAI API key to backend/.env:"
echo "   ${YELLOW}OPENAI_API_KEY=your_key_here${NC}"
echo ""
echo "2. Build the vector store (first time only, takes a few minutes):"
echo "   ${YELLOW}cd backend && source venv/bin/activate && python vector_store.py${NC}"
echo ""
echo "3. Start the backend server:"
echo "   ${YELLOW}cd backend && source venv/bin/activate && python app.py${NC}"
echo ""
echo "4. In a new terminal, start the frontend:"
echo "   ${YELLOW}cd frontend && npm start${NC}"
echo ""
echo "5. Or use the CLI interface:"
echo "   ${YELLOW}cd frontend && npm run cli${NC}"
echo ""
echo "Web UI: http://localhost:3000"
echo "Backend API: http://localhost:5000"
echo ""
