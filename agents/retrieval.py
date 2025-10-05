import os
import pickle
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

'''To be used for improvement
'''

class ContractRAG:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None
        
    def add_documents(self, docs: List[str]):
        """Add contract documents and generate embeddings"""
        self.documents.extend(docs)
        all_embeddings = self.model.encode(self.documents)
        self.embeddings = np.array(all_embeddings)
        
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search for relevant contract sections"""
        if self.embeddings is None:
            return []
            
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(self.documents[i], similarities[i]) for i in top_indices]
        
        return results
        
    def save(self, filepath: str):
        """Save the RAG pipeline"""
        with open(filepath, 'wb') as f:
            pickle.dump({'documents': self.documents, 'embeddings': self.embeddings}, f)
            
    def load(self, filepath: str):
        """Load the RAG pipeline"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.embeddings = data['embeddings']