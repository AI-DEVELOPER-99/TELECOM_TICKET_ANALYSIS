# 🎫 Telecom Ticket Analysis Assistant

An AI-powered ticket analysis system that suggests solutions for telecom support tickets using semantic search and large language models.

## 📋 Overview

This system analyzes incoming support tickets and suggests the top 3 most suitable solutions based on similar resolved tickets from a historical database. It uses:

- **Vector Embeddings** (OpenAI or HuggingFace) for semantic understanding
- **FAISS Vector Database** for efficient similarity search
- **Large Language Models** (GPT-3.5/GPT-4) for intelligent solution generation
- **FastAPI Backend** for high-performance API processing
- **Node.js Frontend** with both CLI and Web UI interfaces

## 🛠️ Tech Stack

### Backend Technologies
- **FastAPI** (0.109.0) - Modern, high-performance Python web framework for building APIs
- **Uvicorn** (0.27.0) - Lightning-fast ASGI server
- **OpenAI** (2.8.1) - GPT models for solution generation & embeddings
- **FAISS-CPU** (1.7.4) - Facebook AI Similarity Search for vector operations
- **Pandas** (2.1.4) - Data manipulation and analysis
- **NumPy** (1.26.2) - Numerical computing
- **Tiktoken** (0.5.2) - Token counting for OpenAI models
- **Python-dotenv** (1.0.0) - Environment variable management
- **Sentence Transformers** (5.1.0+) - Local embedding models

### Frontend Technologies
- **Node.js** - JavaScript runtime environment
- **Express.js** (4.18.2) - Fast, minimalist web framework
- **Axios** (1.6.2) - Promise-based HTTP client
- **Inquirer.js** (8.2.5) - Interactive CLI prompts
- **Chalk** (4.1.2) - Terminal string styling
- **Ora** (5.4.1) - Elegant terminal spinners
- **Vanilla JavaScript** - Modern ES6+ for web UI
- **HTML5 & CSS3** - Responsive web interface

### AI/ML Technologies
- **OpenAI GPT-4o-mini** - Lightweight, cost-effective language model for solution generation
- **OpenAI GPT-3.5/GPT-4** - Alternative large language models (optional)
- **Sentence Transformers** - all-MiniLM-L6-v2 (384 dimensions) - Default embedding model
- **OpenAI Embeddings** - text-embedding-3-small (1536 dimensions) - Alternative option
- **FAISS** - Efficient similarity search and clustering of dense vectors
- **Semantic Search** - Vector-based similarity matching

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │   Web UI (Express)   │      │   CLI (Node.js)      │        │
│  │  - Modern Interface  │      │  - Interactive Menu  │        │
│  │  - Real-time Results │      │  - Color Output      │        │
│  └──────────────────────┘      └──────────────────────┘        │
└────────────────────┬────────────────────┬───────────────────────┘
                     │                    │
                     └─────────┬──────────┘
                               │ HTTP/REST
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend API Layer (FastAPI)                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints: /api/analyze, /api/search, /api/stats    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────┬──────────────────┬────────────────────────┘
                     │                  │
         ┌───────────▼──────────┐      │
         │  Ticket Agent (LLM)  │      │
         │  - Solution Gen      │      │
         │  - Ranking Logic     │      │
         └───────────┬──────────┘      │
                     │                  │
                     └──────────┬───────┘
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vector Store Layer                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    FAISS Index                             │  │
│  │  - 16,000+ ticket embeddings                              │  │
│  │  - Fast similarity search                                 │  │
│  │  - L2 distance metric                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Embedding Model                              │  │
│  │  - sentence-transformers/all-MiniLM-L6-v2 (384d)         │  │
│  │  - or OpenAI text-embedding-3-small (1536d) [optional]   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Data Layer                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │             Cleaned Ticket Dataset (CSV)                  │  │
│  │  - Subject, Body, Answer, Type, Priority                 │  │
│  │  - 16,000+ historical tickets                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
Telecom Ticket Analysis/
├── backend/
│   ├── app.py                 # FastAPI server with REST endpoints
│   ├── config.py              # Configuration management
│   ├── vector_store.py        # FAISS vector store & embeddings
│   ├── ticket_agent.py        # LLM-based ticket analysis
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── .env                  # Environment configuration (not in git)
│   ├── venv/                 # Python virtual environment
│   └── vector_store/         # (Generated) FAISS index files
├── frontend/
│   ├── server.js             # Express web server with proxy
│   ├── cli.js                # Interactive CLI application
│   ├── package.json          # Node.js dependencies
│   ├── .env.example         # Frontend environment template
│   └── public/
│       ├── index.html       # Web UI structure
│       ├── styles.css       # Web UI styling
│       └── app.js           # Web UI JavaScript
├── data/
│   └── clean_data.csv       # Cleaned ticket dataset
├── scripts/
│   └── cleanData.py         # Data cleaning script
├── GENERATE_SOLUTION_FEATURE.md  # Generate Solution feature docs
└── readme.md                # This file
```

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+** - [Download Node.js](https://nodejs.org/)
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **Git** - For cloning the repository

### Quick Start

#### 1. Clone the Repository
```bash
git clone https://github.com/AI-DEVELOPER-99/TELECOM_TICKET_ANALYSIS.git
cd "TELECOM_TICKET_ANALYSIS"
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create environment configuration file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your_api_key_here
# You can use nano, vim, or any text editor:
nano .env

# Build the vector store (first time only - takes 2-5 minutes)
python vector_store.py

# Start the FastAPI backend server
python app.py
```

**Expected Output:**
```
Initializing Ticket Analysis System...
✓ Configuration validated
✓ Vector store loaded successfully
✓ Ticket agent initialized
Using OpenAI for solution generation
INFO:     Uvicorn running on http://0.0.0.0:5001
```

The backend API will be available at `http://localhost:5001`

#### 3. Frontend Setup

Open a **new terminal window** and run:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Create environment configuration file
cp .env.example .env

# (Optional) Edit .env if backend is on different host/port
# BACKEND_URL=http://localhost:5000
# PORT=3000

# Start the Express web server
npm start
```

**Expected Output:**
```
════════════════════════════════════════════════════════════
  TELECOM TICKET ANALYSIS ASSISTANT - WEB UI
════════════════════════════════════════════════════════════

  🌐 Server running at: http://localhost:3000
  🔗 Backend URL: http://localhost:5001

  Press Ctrl+C to stop the server
```

The web UI will be available at `http://localhost:3000`

### Alternative: Run CLI Interface

Instead of the web UI, you can use the interactive CLI:

```bash
# In the frontend directory
npm run cli
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════════╗
║   TELECOM TICKET ANALYSIS ASSISTANT - CLI MODE       ║
╚═══════════════════════════════════════════════════════╝

? What would you like to do? (Use arrow keys)
❯ Analyze New Ticket
  Search Similar Tickets
  View System Stats
  Exit
```

### Verification

To verify everything is working correctly:

1. **Check Backend Health:**
   ```bash
   curl http://localhost:5001/health
   ```
   Expected response: `{"status":"healthy","service":"Ticket Analysis API","initialized":true}`

2. **Check Frontend:**
   Open browser to `http://localhost:3000` and you should see the web interface

3. **Test Analysis:**
   - Go to "Analyze Ticket" tab
   - Enter a test ticket
   - Click "Analyze Ticket"
   - You should receive 3 solution recommendations

4. **Test Generate Solution (NEW):**
   - Go to "✨ Generate Solution" tab
   - Enter ticket details
   - Click "Generate Solution"
   - You should receive an AI-generated comprehensive solution

### Troubleshooting Setup

#### Backend Issues

**Error: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Error: `OpenAI API key not found`**
```bash
# Check .env file exists and has correct format
cat backend/.env
# Should contain: OPENAI_API_KEY=sk-...
```

**Error: `File not found: clean_data.csv`**
```bash
# Ensure you're in the backend directory and data file exists
ls ../data/clean_data.csv
```

**Error: Port 5000 already in use**
```bash
# Change port in backend/.env
echo "SERVER_PORT=5001" >> .env
# Or kill the process using port 5001
lsof -ti:5001 | xargs kill -9
```

#### Frontend Issues

**Error: `Cannot connect to backend`**
- Ensure backend is running on port 5001
- Check `BACKEND_URL` in `frontend/.env` (should be `http://localhost:5001`)
- Verify firewall isn't blocking localhost connections

**Error: `npm: command not found`**
```bash
# Install Node.js from https://nodejs.org/
node --version  # Should show v14 or higher
npm --version
```

**Error: Port 3000 already in use**
```bash
# Change port in frontend/.env
echo "PORT=3001" >> .env
```

### Environment Variables Reference

#### Backend `.env` Configuration
```env
# Optional - Only required if using OpenAI models
OPENAI_API_KEY=sk-your_actual_api_key_here

# Optional - Model Configuration
EMBEDDING_MODEL=sentence-transformers
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
LLM_MODE=local
LLM_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000

# Optional - Search Configuration
TOP_K_RESULTS=5

# Optional - Server Configuration
SERVER_PORT=5001
SERVER_HOST=0.0.0.0
SERVER_DEBUG=True
```

#### Frontend `.env` Configuration
```env
# Backend API endpoint
BACKEND_URL=http://localhost:5001

# Frontend server port
PORT=3000
```

## 💻 Usage

### Web UI

1. Open your browser to `http://localhost:3000`
2. Navigate to the "Analyze Ticket" tab
3. Enter a ticket subject and description
4. Click "Analyze Ticket"
5. View the top 3 recommended solutions with suitability percentages

**Features:**
- 📝 Analyze new tickets with AI-powered solutions
- ✨ Generate comprehensive solutions using LLM and retrieved context
- 🔍 Search for similar resolved tickets
- 📊 View system statistics
- 🎨 Modern, responsive interface

### CLI

1. Run `npm run cli` in the frontend directory
2. Select from the menu:
   - **Analyze New Ticket**: Enter ticket details to get solutions
   - **Search Similar Tickets**: Find similar resolved tickets
   - **View System Stats**: See database statistics
   - **Exit**: Close the application

**Features:**
- 🎨 Colored, interactive terminal interface
- ⚡ Fast and lightweight
- 📋 Easy copy-paste of results

### API Endpoints

#### POST `/api/analyze`
Analyze a ticket and get top 3 solutions

**Request:**
```json
{
  "ticket_description": "Subject: VPN Issues\n\nDescription: Cannot connect to VPN..."
}
```

**Response:**
```json
{
  "success": true,
  "query": "Subject: VPN Issues...",
  "solutions": [
    {
      "rank": 1,
      "solution": "Check firewall settings...",
      "suitability_percentage": 85,
      "reasoning": "Based on similar VPN connectivity issues...",
      "reference_tickets": [1, 3]
    }
  ],
  "similar_tickets_count": 5
}
```

#### POST `/api/generate-solution` (NEW)
Generate a comprehensive solution using LLM and retrieved ticket chunks

**Request:**
```json
{
  "ticket_description": "Subject: Email Server Issues\n\nDescription: Email server not responding..."
}
```

**Response:**
```json
{
  "success": true,
  "query": "Subject: Email Server Issues...",
  "generated_solution": "Based on similar resolved tickets, here's a comprehensive solution:\n\n1. Check server status...",
  "retrieved_chunks": [
    {
      "id": 456,
      "subject": "Email Server Down",
      "similarity_score": 0.87,
      "answer": "Restart email services...",
      ...
    }
  ],
  "chunks_count": 5,
  "llm_model": "gpt-4o-mini"
}
```

#### POST `/api/search`
Search for similar tickets

**Request:**
```json
{
  "query": "internet connection problems",
  "top_k": 5
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "id": 123,
      "subject": "Internet Connection Issues",
      "similarity_score": 0.89,
      "type": "Incident",
      "priority": "high",
      ...
    }
  ]
}
```

#### GET `/api/stats`
Get system statistics

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_tickets": 16339,
    "embedding_dimension": 384,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "llm_mode": "local"
  }
}
```

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key from platform.openai.com | - | Only if using OpenAI |
| `EMBEDDING_MODEL` | Embedding provider (`sentence-transformers` or `openai`) | `sentence-transformers` | No |
| `EMBEDDING_MODEL_NAME` | Specific model name | `all-MiniLM-L6-v2` | No |
| `LLM_MODE` | LLM mode (`local` or `openai`) | `openai` | No |
| `LLM_MODEL` | LLM for solution generation | `gpt-4o-mini` | No |
| `TEMPERATURE` | LLM temperature (0-1) | `0.7` | No |
| `MAX_TOKENS` | Max tokens in LLM response | `1000` | No |
| `TOP_K_RESULTS` | Number of similar tickets to retrieve | `5` | No |
| `SERVER_PORT` | Backend server port | `5001` | No |
| `SERVER_HOST` | Server host address | `0.0.0.0` | No |
| `SERVER_DEBUG` | Enable debug mode | `True` | No |

### Frontend Configuration (`frontend/.env`)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BACKEND_URL` | Backend API URL | `http://localhost:5001` | No |
| `PORT` | Frontend server port | `3000` | No |

## 🎯 How It Works

### 1. Corpus Preparation
- Loads `clean_data.csv` containing 16,000+ historical tickets
- Preprocesses tickets by combining subject, body, type, queue, and priority
- Creates structured text representations optimized for embedding

### 2. Embedding Generation
- Converts ticket text into dense vector embeddings (384 dimensions for sentence-transformers, 1536 for OpenAI)
- Uses state-of-the-art embedding models for semantic understanding
- Processes tickets in batches for efficiency
- Default: sentence-transformers/all-MiniLM-L6-v2 (local, free)

### 3. Vector Store Creation
- Stores embeddings in FAISS (Facebook AI Similarity Search) index
- Uses L2 distance metric for similarity calculations
- Enables sub-millisecond similarity search across thousands of tickets

### 4. Query Processing
When a new ticket arrives:
1. **Embedding**: Convert ticket description to vector embedding
2. **Search**: Find top K most similar resolved tickets using FAISS
3. **Context Building**: Prepare relevant context from similar tickets
4. **LLM Generation**: Use GPT to analyze context and generate 3 ranked solutions
5. **Response**: Return solutions with suitability percentages and reasoning

### 5. Solution Ranking
The LLM considers:
- Similarity scores from vector search
- Ticket type and priority alignment
- Historical resolution effectiveness
- Technical context and specificity

## 📊 Dataset

The system uses `data/clean_data.csv` with the following schema:

| Column | Description |
|--------|-------------|
| `subject` | Brief ticket title |
| `body` | Detailed issue description |
| `answer` | Resolution provided |
| `type` | Incident, Request, Problem, etc. |
| `queue` | Support queue (Technical, Billing, etc.) |
| `priority` | low, medium, high |
| `language` | Language code |
| `tag_1` to `tag_8` | Categorization tags |

**Stats:**
- 16,339 tickets
- Multiple ticket types and priorities
- Comprehensive resolution history

## 🔍 Example Usage

### Example 1: VPN Connection Issue

**Input:**
```
Subject: Cannot connect to company VPN

Description: I'm trying to connect to the company VPN from home but 
keep getting connection timeout errors. I've tried restarting my 
router and computer, but the issue persists. Error code 800.
```

**Output:**
```
Solution #1 (85% Suitable)
Check your firewall settings and ensure VPN ports are open. 
Verify that UDP ports 500 and 4500 are not blocked...

Solution #2 (72% Suitable)
Update your VPN client to the latest version and ensure your 
network drivers are current...

Solution #3 (65% Suitable)
Try using an alternative internet connection to rule out 
ISP-level blocking...
```

### Example 2: Billing Query

**Input:**
```
Subject: Unexpected charges on invoice

Description: I noticed additional charges on my latest bill that 
I don't recognize. Can you explain what these are for?
```

**Output:**
```
Solution #1 (88% Suitable)
Review your recent service changes and usage patterns. Additional 
charges may be from premium features activated last month...

Solution #2 (75% Suitable)
Check if you've exceeded your data plan limits, which can result 
in overage charges...

Solution #3 (68% Suitable)
Contact billing department directly for a detailed breakdown of 
all charges on your account...
```

## 🛠️ Customization

### Using Different Embedding Models

Edit `backend/.env`:

```env
# Option 1: Sentence Transformers (default, free, runs locally)
EMBEDDING_MODEL=sentence-transformers
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Option 2: OpenAI (better quality, requires API key and costs money)
# EMBEDDING_MODEL=openai
# OPENAI_API_KEY=sk-your_api_key_here

# Other sentence-transformers models you can try:
# EMBEDDING_MODEL_NAME=all-mpnet-base-v2  # Higher quality, slower
# EMBEDDING_MODEL_NAME=paraphrase-MiniLM-L6-v2  # Similar performance
```

### Using Different LLMs

```env
# Local mode (default, rule-based generation)
LLM_MODE=local

# OpenAI mode (requires API key, uses GPT models)
LLM_MODE=openai
OPENAI_API_KEY=sk-your_api_key_here

# GPT-4o-mini (recommended: lightweight, fast, cost-effective)
LLM_MODEL=gpt-4o-mini

# GPT-3.5 (faster, cheaper, good quality)
LLM_MODEL=gpt-3.5-turbo

# GPT-4 (best quality, more expensive)
LLM_MODEL=gpt-4

# GPT-4 Turbo
LLM_MODEL=gpt-4-turbo-preview
```

### Azure OpenAI

In `backend/.env`:

```env
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
```

Update `vector_store.py` and `ticket_agent.py` to use Azure OpenAI client.

## 🚧 Troubleshooting

### Backend Issues

**Problem: Backend won't start**
- Verify Python version: `python --version` (3.8+ required)
- Check API key is set in `backend/.env`
- Ensure virtual environment is activated: `source venv/bin/activate`
- Install all dependencies: `pip install -r requirements.txt`

**Problem: Vector store build fails**
- Ensure `data/clean_data.csv` exists
- Check available disk space (needs ~500MB)
- If using OpenAI: Verify API key has sufficient quota and billing status
- If using sentence-transformers: Ensure model can download (needs internet connection first time)
- For sentence-transformers errors: `pip install sentence-transformers`

**Problem: Import errors**
```bash
# Reinstall dependencies in virtual environment
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

**Problem: FAISS installation fails on Apple Silicon (M1/M2)**
```bash
# Use conda instead
conda install -c conda-forge faiss-cpu
```

### Frontend Issues

**Problem: Frontend can't connect to backend**
- Ensure backend is running on port 5001: `curl http://localhost:5001/health`
- Check `BACKEND_URL` in `frontend/.env` matches backend address (should be `http://localhost:5001`)
- Verify no firewall blocking localhost connections
- Check CORS is enabled in backend (it is by default)
- Ensure frontend proxy routes include `/api/generate-solution`

**Problem: `npm install` fails**
- Update Node.js to version 14+: `node --version`
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and try again: `rm -rf node_modules && npm install`

**Problem: Port already in use**
```bash
# Find and kill process using the port
# For port 3000 (frontend):
lsof -ti:3000 | xargs kill -9

# For port 5001 (backend):
lsof -ti:5001 | xargs kill -9
```

### Performance Issues

**Problem: Slow response times**
- First query is slower (cold start) - this is normal
- Consider using `gpt-4o-mini` (recommended) or `gpt-3.5-turbo` for faster responses
- Reduce `TOP_K_RESULTS` in `.env` to retrieve fewer similar tickets
- Ensure adequate RAM (minimum 4GB free)

**Problem: High memory usage**
- Vector store requires ~500MB in memory
- Sentence-transformers model requires ~400MB
- Close other applications if running low on RAM
- Consider using smaller embedding model for lower memory footprint

**Problem: OpenAI errors (`proxies` argument error)**
```bash
# Upgrade to compatible OpenAI version
cd backend
source venv/bin/activate
pip install --upgrade openai
# Should install openai>=2.8.1
```
- Check OpenAI usage dashboard for quota limits
- Reduce `MAX_TOKENS` to use fewer tokens per request
- Add delays between requests in high-volume scenarios
- Consider upgrading OpenAI plan for higher limits

## 📈 Performance

- **Embedding Generation**: 
  - Sentence-transformers: ~5-10 minutes for 16K tickets (first time only, runs locally)
  - OpenAI: ~2-3 minutes (requires API calls and costs ~$0.50)
- **Query Response Time**: 1-3 seconds per ticket analysis (local mode)
- **Vector Search**: Sub-millisecond similarity search
- **Memory Usage**: ~500MB for vector store + ~400MB for embedding model in memory

## 🔐 Security Considerations

- Store API keys in `.env` files (never commit to git)
- `.env` files are gitignored by default
- Use environment-specific configurations
- Consider implementing rate limiting for production
- Add authentication for API endpoints in production

## 🤝 Contributing

To extend this project:

1. **Add new ticket sources**: Modify `vector_store.py` to load from databases
2. **Improve preprocessing**: Enhance `preprocess_ticket()` for better context
3. **Custom ranking**: Modify LLM prompts in `ticket_agent.py`
4. **Additional features**: Add feedback loops, solution tracking, etc.
5. **New endpoints**: Add to both `backend/app.py` and `frontend/server.js` proxy

## 🆕 Recent Updates

### Generate Solution Feature
- Added new `/api/generate-solution` endpoint
- Uses LLM to generate comprehensive solutions from retrieved ticket chunks
- New "✨ Generate Solution" tab in web UI
- Displays retrieved context tickets with similarity scores
- See `GENERATE_SOLUTION_FEATURE.md` for detailed documentation

### Technical Improvements
- Upgraded OpenAI library to v2.8.1 for better compatibility
- Fixed proxy server routing for all API endpoints
- Enhanced error handling in frontend
- Improved null safety in response processing

## 📝 License

MIT License - feel free to use and modify for your needs.

## 🙏 Acknowledgments

- OpenAI for GPT and embedding models
- Facebook Research for FAISS
- The open-source community for amazing tools

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review configuration files
3. Ensure all dependencies are installed
4. Verify API keys are valid and have quota

---

**Built with ❤️ using AI & Vector Search Technology**
