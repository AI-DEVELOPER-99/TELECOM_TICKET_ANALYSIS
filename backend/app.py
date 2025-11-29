from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
from config import Config
from vector_store import VectorStoreManager
from ticket_agent import TicketAnalysisAgent

# Initialize FastAPI app
app = FastAPI(
    title="Ticket Analysis API",
    description="AI-Powered Support Ticket Solution Finder",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for vector store and agent
vector_store = None
agent = None

# Pydantic models for request/response validation
class TicketAnalysisRequest(BaseModel):
    ticket_description: str = Field(..., min_length=10, description="The ticket description to analyze")

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    top_k: Optional[int] = Field(None, description="Number of results to return")

class HealthResponse(BaseModel):
    status: str
    service: str
    initialized: bool

def initialize_system():
    """Initialize the vector store and agent"""
    global vector_store, agent
    
    print("Initializing Ticket Analysis System...")
    
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize vector store
        print("Loading vector store...")
        use_openai = Config.EMBEDDING_MODEL == 'openai'
        vector_store = VectorStoreManager(use_openai=use_openai)
        vector_store.build_vector_store(force_rebuild=False)
        
        # Initialize agent
        print("Initializing AI agent...")
        agent = TicketAnalysisAgent(vector_store)
        
        print("System initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing system: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    if not initialize_system():
        print("\nFailed to initialize system. Please check your configuration.")
        print("Make sure to:")
        print("1. Copy .env.example to .env")
        print("2. Configure EMBEDDING_MODEL and LLM_MODE in .env")
        print("3. Install required packages: pip install -r requirements.txt")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="Ticket Analysis API",
        initialized=agent is not None
    )

@app.post("/api/analyze")
async def analyze_ticket(request: TicketAnalysisRequest):
    """
    Analyze a ticket and return top 3 solutions
    
    **Request Body:**
    - ticket_description: Description of the issue (min 10 characters)
    
    **Response:**
    - success: Boolean indicating success
    - query: The original query
    - solutions: List of 3 solutions with rank, solution text, suitability %, reasoning, and references
    - similar_tickets_count: Number of similar tickets used for analysis
    """
    try:
        # Check if system is initialized
        if agent is None:
            raise HTTPException(
                status_code=500,
                detail="System not initialized. Please check configuration."
            )
        
        # Analyze ticket
        result = agent.analyze_ticket(request.ticket_description)
        
        # Return response
        return {
            "success": True,
            **result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in analyze_ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_similar(request: SearchRequest):
    """
    Search for similar tickets without generating solutions
    
    **Request Body:**
    - query: Description to search for
    - top_k: Optional number of results (default from config)
    
    **Response:**
    - success: Boolean indicating success
    - results: List of similar tickets with metadata and similarity scores
    - count: Number of results returned
    """
    try:
        # Check if system is initialized
        if vector_store is None:
            raise HTTPException(
                status_code=500,
                detail="System not initialized."
            )
        
        # Get top_k from request or use default
        top_k = request.top_k if request.top_k else Config.TOP_K_RESULTS
        
        # Search
        results = vector_store.search_similar_tickets(request.query, top_k=top_k)
        
        return {
            "success": True,
            "results": results,
            "count": len(results)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in search_similar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rebuild-index")
async def rebuild_index():
    """
    Rebuild the vector store index
    
    **Note:** This is a time-consuming operation
    """
    try:
        if vector_store is None:
            raise HTTPException(
                status_code=500,
                detail="System not initialized."
            )
        
        # Rebuild
        vector_store.build_vector_store(force_rebuild=True)
        
        return {
            "success": True,
            "message": "Vector store rebuilt successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error rebuilding index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """
    Get system statistics
    
    **Response:**
    - success: Boolean indicating success
    - stats: Dictionary containing system statistics
    """
    try:
        if vector_store is None:
            raise HTTPException(
                status_code=500,
                detail="System not initialized."
            )
        
        return {
            "success": True,
            "stats": {
                "total_tickets": len(vector_store.tickets),
                "embedding_dimension": vector_store.embedding_dimension,
                "embedding_model": Config.EMBEDDING_MODEL,
                "llm_model": Config.LLM_MODEL
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    
    print(f"\n{'='*60}")
    print(f"  TELECOM TICKET ANALYSIS ASSISTANT - FastAPI Backend")
    print(f"{'='*60}\n")
    print(f"Starting server on {Config.SERVER_HOST}:{Config.SERVER_PORT}...")
    print(f"API Documentation:")
    print(f"  POST /api/analyze - Analyze ticket and get solutions")
    print(f"  POST /api/search - Search for similar tickets")
    print(f"  GET /api/stats - Get system statistics")
    print(f"  GET /health - Health check")
    print(f"  GET /docs - Interactive API documentation (Swagger UI)")
    print(f"  GET /redoc - Alternative API documentation (ReDoc)")
    print(f"\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "app:app",
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        reload=Config.SERVER_DEBUG
    )
