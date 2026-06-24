"""
vector_store.py

Stores lecture chunks.
"""

import chromadb

from ai.chunker import LectureChunker

from ai.embeddings import (
    EmbeddingService
)


class LectureVectorStore:

    def __init__(self):

        self.client = (
            chromadb.PersistentClient(
                path="vectordb"
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                "lecture_knowledge"
            )
        )

        self.embedding_service = (
            EmbeddingService()
        )

    def add_chunks(
        self,
        chunks
    ):

        embeddings = (
            self.embedding_service
            .embed_batch(chunks)
        )

        ids = [
            f"chunk_{i}"
            for i in range(
                len(chunks)
            )
        ]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=ids
        )

    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = (
            self.embedding_service
            .embed_text(query)
        )

        result = (
            self.collection.query(
                query_embeddings=[
                    query_embedding.tolist()
                ],
                n_results=top_k
            )
        )

        return result


if __name__ == "__main__":

    store = LectureVectorStore()

    chunker = LectureChunker()

    chunk_objects = chunker.process_file(
        "outputs/fusion/knowledge.txt",
        "outputs/chunks/chunks.json"
    )

    texts = [
        c["text"]
        for c in chunk_objects
    ]

    store.add_chunks(texts)

    result = store.search(
        "What is 1NF?"
    )

    print(result)