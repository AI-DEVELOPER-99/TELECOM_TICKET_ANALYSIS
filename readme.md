# 🎫 Telecom Ticket Analysis Assistant

An AI-powered ticket analysis system that suggests solutions for telecom support tickets using semantic search and large language models.

## 📋 Overview

This system analyzes incoming support tickets and suggests the top 3 most suitable solutions based on similar resolved tickets from a historical database. It uses:

- **Vector Embeddings** (OpenAI or HuggingFace) for semantic understanding
- **FAISS Vector Database** for efficient similarity search
- **Large Language Models** (GPT-3.5/GPT-4) for intelligent solution generation
- **Flask Backend API** for processing and analysis
- **Node.js Frontend** with both CLI and Web UI interfaces

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
│                      Backend API Layer (Flask)                   │
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
│  │  - OpenAI text-embedding-3-small (1536d)                  │  │
│  │  - or sentence-transformers (384d)                        │  │
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
│   ├── app.py                 # Flask API server
│   ├── config.py              # Configuration management
│   ├── vector_store.py        # FAISS vector store & embeddings
│   ├── ticket_agent.py        # LLM-based ticket analysis
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── vector_store/         # (Generated) FAISS index files
├── frontend/
│   ├── server.js             # Express web server
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
└── readme.md                # This file
```

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **OpenAI API Key** (or Azure OpenAI credentials)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here

# Build vector store (first time only - takes a few minutes)
python vector_store.py

# Start the backend server
python app.py
```

The backend will start on `http://localhost:5000`

### 2. Frontend Setup

#### Web UI

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start the web server
npm start
```

The web UI will be available at `http://localhost:3000`

#### CLI Interface

```bash
# In the frontend directory
npm run cli
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
    "embedding_dimension": 1536,
    "embedding_model": "text-embedding-3-small",
    "llm_model": "gpt-3.5-turbo"
  }
}
```

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `EMBEDDING_MODEL` | Embedding model to use | `text-embedding-3-small` |
| `LLM_MODEL` | LLM for solution generation | `gpt-3.5-turbo` |
| `TEMPERATURE` | LLM temperature (0-1) | `0.7` |
| `MAX_TOKENS` | Max tokens in LLM response | `1000` |
| `TOP_K_RESULTS` | Number of similar tickets to retrieve | `5` |
| `FLASK_PORT` | Backend server port | `5000` |

### Frontend Configuration (`frontend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `BACKEND_URL` | Backend API URL | `http://localhost:5000` |
| `PORT` | Frontend server port | `3000` |

## 🎯 How It Works

### 1. Corpus Preparation
- Loads `clean_data.csv` containing 16,000+ historical tickets
- Preprocesses tickets by combining subject, body, type, queue, and priority
- Creates structured text representations optimized for embedding

### 2. Embedding Generation
- Converts ticket text into dense vector embeddings (1536 dimensions for OpenAI)
- Uses state-of-the-art embedding models for semantic understanding
- Processes tickets in batches for efficiency

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
# Option 1: OpenAI (recommended for best quality)
EMBEDDING_MODEL=text-embedding-3-small

# Option 2: HuggingFace sentence-transformers (free, runs locally)
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

For HuggingFace models, modify `vector_store.py` to set `use_openai=False`.

### Using Different LLMs

```env
# GPT-3.5 (faster, cheaper)
LLM_MODEL=gpt-3.5-turbo

# GPT-4 (better quality, more expensive)
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

### Backend won't start
- Verify Python version: `python --version` (3.8+ required)
- Check API key is set in `backend/.env`
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Vector store build fails
- Ensure `data/clean_data.csv` exists
- Check available disk space (needs ~500MB)
- Verify OpenAI API key has sufficient quota

### Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check `BACKEND_URL` in `frontend/.env`
- Verify no firewall blocking localhost connections

### Slow response times
- First query is slower (cold start)
- Consider upgrading to faster embedding model
- Use GPT-3.5 instead of GPT-4 for speed

## 📈 Performance

- **Embedding Generation**: ~2-5 minutes for 16K tickets (first time only)
- **Query Response Time**: 2-5 seconds per ticket analysis
- **Vector Search**: Sub-millisecond similarity search
- **Memory Usage**: ~500MB for vector store in memory

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
