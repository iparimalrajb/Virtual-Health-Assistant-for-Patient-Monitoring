def load_knowledge():
    with open("knowledge.txt", "r") as f:
        return f.read()


def retrieve_context(user_query, knowledge):
    # Simple keyword matching (v1 RAG)
    relevant_chunks = []

    for line in knowledge.split("\n"):
        if any(word.lower() in line.lower() for word in user_query.split()):
            relevant_chunks.append(line)

    return "\n".join(relevant_chunks[:5])