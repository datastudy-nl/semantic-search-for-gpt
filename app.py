from flask import Flask, request, jsonify
import faiss
import sqlite3
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Initialize Sentence Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create SQLite database
conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

# Create table to store text and embeddings
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    embedding BLOB
)
""")
conn.commit()

# Initialize FAISS index
embedding_dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(embedding_dimension)

# Maintain a mapping of SQLite IDs to FAISS indices
sqlite_to_faiss_map = {}

# Function to load existing embeddings into FAISS index at startup
def load_embeddings_to_faiss():
    cursor.execute("SELECT id, embedding FROM memory")
    rows = cursor.fetchall()
    if rows:
        embeddings = []
        for row in rows:
            sqlite_id = row[0]
            embedding = np.frombuffer(row[1], dtype=np.float32)
            embeddings.append(embedding)
            sqlite_to_faiss_map[len(embeddings) - 1] = sqlite_id
        index.add(np.array(embeddings, dtype=np.float32))

# Load existing embeddings into FAISS index at startup
load_embeddings_to_faiss()

# Function to add text to memory
def add_to_memory(text):
    # Generate embedding
    embedding = model.encode([text])[0]

    # Insert text and embedding into database
    cursor.execute("INSERT INTO memory (text, embedding) VALUES (?, ?)", (text, embedding.tobytes()))
    conn.commit()

    # Map the new SQLite ID to FAISS index
    sqlite_id = cursor.lastrowid
    sqlite_to_faiss_map[index.ntotal] = sqlite_id

    # Add embedding to FAISS index
    index.add(embedding.reshape(1, -1))

# Function to search memory
def search_memory(query, top_k=10, distance_threshold=None):
    # Generate embedding for query
    query_embedding = model.encode([query])[0]

    # Perform search in FAISS index
    distances, indices = index.search(query_embedding.reshape(1, -1), top_k)

    # Normalize distances to relevance percentages (higher % = more relevant)
    max_distance = max(distances[0]) if distances[0].size > 0 else 1.0
    relevance_scores = [(1 - (distance / max_distance)) * 100 for distance in distances[0]]

    # Fetch the corresponding texts from the database
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            if distance_threshold is None or distances[0][i] <= distance_threshold:
                sqlite_id = sqlite_to_faiss_map[idx]
                cursor.execute("SELECT text FROM memory WHERE id = ?", (sqlite_id,))
                result = cursor.fetchone()
                if result:
                    # Add text and its relevance score to the results
                    results.append({"text": result[0], "relevance": relevance_scores[i]})

    return results

# API endpoint to add text to memory
@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.json
        text = data.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400

        add_to_memory(text)
        print(text)
        return jsonify({"message": "Text added to memory."}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to add memory"}), 400

# API endpoint to search memory
@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query")
    top_k = data.get("top_k", 5)
    if not query:
        return jsonify({"error": "Query is required"}), 400

    results = [a.get('text') for a in search_memory(query, top_k=top_k)]
    return jsonify({"results": results}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)