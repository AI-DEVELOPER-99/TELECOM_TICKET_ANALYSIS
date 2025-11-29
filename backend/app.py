from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from config import Config
from vector_store import VectorStoreManager
from ticket_agent import TicketAnalysisAgent

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for vector store and agent
vector_store = None
agent = None

def initialize_system():
    """Initialize the vector store and agent"""
    global vector_store, agent
    
    print("Initializing Ticket Analysis System...")
    
    try:
        # Validate configuration
        Config.validate()
        
        # Initialize vector store
        print("Loading vector store...")
        vector_store = VectorStoreManager(use_openai=True)
        vector_store.build_vector_store(force_rebuild=False)
        
        # Initialize agent
        print("Initializing AI agent...")
        agent = TicketAnalysisAgent(vector_store)
        
        print("System initialized successfully!")
        return True
        
    except Exception as e:
        print(f"Error initializing system: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Ticket Analysis API',
        'initialized': agent is not None
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_ticket():
    """
    Analyze a ticket and return top 3 solutions
    
    Request Body:
    {
        "ticket_description": "Description of the issue..."
    }
    
    Response:
    {
        "success": true,
        "query": "...",
        "solutions": [
            {
                "rank": 1,
                "solution": "...",
                "suitability_percentage": 85,
                "reasoning": "...",
                "reference_tickets": [1, 2]
            },
            ...
        ],
        "similar_tickets_count": 5
    }
    """
    try:
        # Check if system is initialized
        if agent is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized. Please check configuration.'
            }), 500
        
        # Get request data
        data = request.get_json()
        
        if not data or 'ticket_description' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: ticket_description'
            }), 400
        
        ticket_description = data['ticket_description']
        
        if not ticket_description or len(ticket_description.strip()) < 10:
            return jsonify({
                'success': False,
                'error': 'Ticket description must be at least 10 characters'
            }), 400
        
        # Analyze ticket
        result = agent.analyze_ticket(ticket_description)
        
        # Return response
        return jsonify({
            'success': True,
            **result
        })
        
    except Exception as e:
        print(f"Error in analyze_ticket: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['POST'])
def search_similar():
    """
    Search for similar tickets without generating solutions
    
    Request Body:
    {
        "query": "Description to search...",
        "top_k": 5  // optional
    }
    
    Response:
    {
        "success": true,
        "results": [
            {
                "id": 123,
                "subject": "...",
                "body": "...",
                "answer": "...",
                "similarity_score": 0.85,
                ...
            },
            ...
        ]
    }
    """
    try:
        # Check if system is initialized
        if vector_store is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized.'
            }), 500
        
        # Get request data
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: query'
            }), 400
        
        query = data['query']
        top_k = data.get('top_k', Config.TOP_K_RESULTS)
        
        # Search
        results = vector_store.search_similar_tickets(query, top_k=top_k)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        print(f"Error in search_similar: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rebuild-index', methods=['POST'])
def rebuild_index():
    """
    Rebuild the vector store index
    
    Note: This is a time-consuming operation
    """
    try:
        if vector_store is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized.'
            }), 500
        
        # Rebuild
        vector_store.build_vector_store(force_rebuild=True)
        
        return jsonify({
            'success': True,
            'message': 'Vector store rebuilt successfully'
        })
        
    except Exception as e:
        print(f"Error rebuilding index: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        if vector_store is None:
            return jsonify({
                'success': False,
                'error': 'System not initialized.'
            }), 500
        
        return jsonify({
            'success': True,
            'stats': {
                'total_tickets': len(vector_store.tickets),
                'embedding_dimension': vector_store.embedding_dimension,
                'embedding_model': Config.EMBEDDING_MODEL,
                'llm_model': Config.LLM_MODEL
            }
        })
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Initialize system on startup
    if initialize_system():
        print(f"\nStarting Flask server on {Config.FLASK_HOST}:{Config.FLASK_PORT}...")
        print(f"API Documentation:")
        print(f"  POST /api/analyze - Analyze ticket and get solutions")
        print(f"  POST /api/search - Search for similar tickets")
        print(f"  GET /api/stats - Get system statistics")
        print(f"  GET /health - Health check")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        app.run(
            host=Config.FLASK_HOST,
            port=Config.FLASK_PORT,
            debug=Config.FLASK_DEBUG
        )
    else:
        print("\nFailed to initialize system. Please check your configuration.")
        print("Make sure to:")
        print("1. Copy .env.example to .env")
        print("2. Set your OPENAI_API_KEY in .env")
        print("3. Install required packages: pip install -r requirements.txt")
