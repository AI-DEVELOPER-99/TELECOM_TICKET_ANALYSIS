import pandas as pd
import numpy as np
import faiss
import pickle
import os
from typing import List, Dict, Tuple
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from config import Config

class VectorStoreManager:
    """Manages embeddings and FAISS vector store for ticket data"""
    
    def __init__(self, use_openai: bool = True):
        """
        Initialize the vector store manager
        
        Args:
            use_openai: If True, use OpenAI embeddings, else use sentence-transformers
        """
        self.use_openai = use_openai
        self.config = Config()
        
        if self.use_openai:
            self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
            self.embedding_dimension = 1536  # text-embedding-3-small dimension
        else:
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.embedding_dimension = 384
        
        self.index = None
        self.tickets = []
        self.metadata = []
    
    def load_data(self) -> pd.DataFrame:
        """Load and prepare ticket data from CSV"""
        print(f"Loading data from {self.config.DATA_PATH}...")
        df = pd.read_csv(self.config.DATA_PATH)
        print(f"Loaded {len(df)} tickets")
        return df
    
    def preprocess_ticket(self, row: pd.Series) -> str:
        """
        Preprocess a single ticket into a text chunk for embedding
        
        Args:
            row: Pandas series containing ticket information
            
        Returns:
            Preprocessed text string
        """
        subject = str(row.get('subject', ''))
        body = str(row.get('body', ''))
        ticket_type = str(row.get('type', ''))
        queue = str(row.get('queue', ''))
        priority = str(row.get('priority', ''))
        
        # Combine relevant fields
        text = f"Subject: {subject}\n\nDescription: {body}\n\nType: {ticket_type}\nQueue: {queue}\nPriority: {priority}"
        
        return text
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a given text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        if self.use_openai:
            response = self.client.embeddings.create(
                input=text,
                model=self.config.EMBEDDING_MODEL
            )
            return np.array(response.data[0].embedding, dtype=np.float32)
        else:
            return self.model.encode(text, convert_to_numpy=True).astype(np.float32)
    
    def get_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> np.ndarray:
        """
        Generate embeddings for multiple texts in batches
        
        Args:
            texts: List of input texts
            batch_size: Number of texts to process at once
            
        Returns:
            Array of embeddings
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
            
            if self.use_openai:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.config.EMBEDDING_MODEL
                )
                batch_embeddings = [np.array(item.embedding, dtype=np.float32) for item in response.data]
            else:
                batch_embeddings = self.model.encode(batch, convert_to_numpy=True, show_progress_bar=True).astype(np.float32)
            
            embeddings.extend(batch_embeddings)
        
        return np.array(embeddings)
    
    def build_vector_store(self, force_rebuild: bool = False):
        """
        Build FAISS vector store from ticket data
        
        Args:
            force_rebuild: If True, rebuild even if store exists
        """
        os.makedirs(self.config.VECTOR_STORE_PATH, exist_ok=True)
        
        index_path = os.path.join(self.config.VECTOR_STORE_PATH, 'faiss_index.bin')
        metadata_path = os.path.join(self.config.VECTOR_STORE_PATH, 'metadata.pkl')
        
        # Load existing store if available
        if not force_rebuild and os.path.exists(index_path) and os.path.exists(metadata_path):
            print("Loading existing vector store...")
            self.index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                data = pickle.load(f)
                self.tickets = data['tickets']
                self.metadata = data['metadata']
            print(f"Loaded vector store with {len(self.tickets)} tickets")
            return
        
        # Build new store
        print("Building new vector store...")
        df = self.load_data()
        
        # Preprocess tickets
        self.tickets = []
        self.metadata = []
        
        for idx, row in df.iterrows():
            ticket_text = self.preprocess_ticket(row)
            self.tickets.append(ticket_text)
            
            # Store metadata
            metadata = {
                'id': idx,
                'subject': row.get('subject', ''),
                'body': row.get('body', ''),
                'answer': row.get('answer', ''),
                'type': row.get('type', ''),
                'queue': row.get('queue', ''),
                'priority': row.get('priority', ''),
                'tags': [row.get(f'tag_{i}', '') for i in range(1, 9) if pd.notna(row.get(f'tag_{i}', ''))]
            }
            self.metadata.append(metadata)
        
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.get_embeddings_batch(self.tickets)
        
        # Create FAISS index
        print("Creating FAISS index...")
        self.index = faiss.IndexFlatL2(self.embedding_dimension)
        self.index.add(embeddings)
        
        # Save to disk
        print("Saving vector store...")
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump({'tickets': self.tickets, 'metadata': self.metadata}, f)
        
        print(f"Vector store built successfully with {len(self.tickets)} tickets!")
    
    def search_similar_tickets(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for similar tickets using the query
        
        Args:
            query: Query text (new ticket description)
            top_k: Number of results to return
            
        Returns:
            List of similar tickets with metadata and similarity scores
        """
        if self.index is None:
            raise ValueError("Vector store not initialized. Call build_vector_store() first.")
        
        if top_k is None:
            top_k = self.config.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.get_embedding(query).reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['similarity_score'] = float(1 / (1 + distances[0][i]))  # Convert distance to similarity
                result['ticket_text'] = self.tickets[idx]
                results.append(result)
        
        return results

if __name__ == "__main__":
    # Test the vector store
    print("Initializing VectorStoreManager...")
    manager = VectorStoreManager(use_openai=True)
    
    print("\nBuilding vector store...")
    manager.build_vector_store(force_rebuild=False)
    
    # Test search
    test_query = "Internet connection is not working properly and keeps disconnecting"
    print(f"\n\nTest Query: {test_query}")
    results = manager.search_similar_tickets(test_query, top_k=3)
    
    print("\n\nTop 3 Similar Tickets:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Subject: {result['subject']}")
        print(f"   Similarity: {result['similarity_score']:.2%}")
        print(f"   Type: {result['type']} | Queue: {result['queue']}")
