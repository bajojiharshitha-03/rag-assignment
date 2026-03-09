import sqlite3
import json
from embeddings import generate_embedding

documents = [
    "Users can reset their password from Settings > Security.",
    "To update your email address go to Profile Settings.",
    "You can delete your account from the Account Management page.",
    "Two factor authentication can be enabled in Security settings."
]

conn = sqlite3.connect("rag.db")
cursor = conn.cursor()

for doc in documents:
    embedding = generate_embedding(doc)

    cursor.execute(
        "INSERT INTO documents (chunk, embedding) VALUES (?, ?)",
        (doc, json.dumps(embedding))
    )

conn.commit()
conn.close()

print("Documents inserted successfully")