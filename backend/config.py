import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the ticket analysis system"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Azure OpenAI Configuration (optional)
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY', '')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', '')
    
    # Embedding Model Configuration
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers')
    EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'all-MiniLM-L6-v2')
    
    # LLM Configuration
    LLM_MODE = os.getenv('LLM_MODE', 'local')  # 'openai' or 'local'
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    
    # Vector Store Configuration
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', '5'))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '500'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '50'))
    
    # Paths
    DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'clean_data.csv')
    VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), 'vector_store')
    
    # Server Configuration
    SERVER_PORT = int(os.getenv('SERVER_PORT', '5001'))
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_DEBUG = os.getenv('SERVER_DEBUG', 'True') == 'True'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if cls.LLM_MODE == 'openai' and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set when LLM_MODE is 'openai'")
        return True
