import sqlite3
import json
import numpy as np
from embeddings import generate_embedding

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_documents(query, threshold=0.4):
    query_embedding = generate_embedding(query)
    
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chunk, embedding FROM documents")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for chunk, emb_json in rows:
        doc_emb = json.loads(emb_json)
        score = cosine_similarity(query_embedding, doc_emb)
        
        # Mandatory Requirement: Apply similarity threshold
        if score >= threshold:
            results.append((chunk, score))

    # Sort by highest similarity
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 2 chunks for better context, or empty list if none match
    
    conn.close()
    return [r[0] for r in results[:2]]

    