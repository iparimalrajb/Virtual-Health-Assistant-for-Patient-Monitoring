from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model 
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_knowledge_chunks():
    with open("knowledge.txt", "r") as f:
        text = f.read()

    # Split into chunks
    chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]
    return chunks


def create_vector_store():
    chunks = load_knowledge_chunks()

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index, chunks


# Initialize once
index, chunks = create_vector_store()


def retrieve_semantic(query, top_k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = [chunks[i] for i in indices[0]]
    return "\n".join(results)