"""
retriever.py

Retrieves relevant chunks
from ChromaDB.
"""

from ai.vector_store import (
    LectureVectorStore
)


class LectureRetriever:

    def __init__(self):

        self.vector_store = (
            LectureVectorStore()
        )

    def retrieve(
        self,
        query,
        top_k=5
    ):

        result = (
            self.vector_store.search(
                query=query,
                top_k=top_k
            )
        )

        documents = result.get(
            "documents",
            [[]]
        )[0]

        distances = result.get(
            "distances",
            [[]]
        )[0]

        ids = result.get(
            "ids",
            [[]]
        )[0]

        chunks = []

        for i in range(
            len(documents)
        ):

            chunks.append(
                {
                    "id":
                        ids[i],

                    "text":
                        documents[i],

                    "distance":
                        distances[i]
                }
            )

        return chunks

    def retrieve_context(
        self,
        query,
        top_k=5
    ):

        chunks = self.retrieve(
            query,
            top_k
        )

        context = []

        for chunk in chunks:

            context.append(
                chunk["text"]
            )

        return "\n\n".join(
            context
        )


if __name__ == "__main__":

    retriever = (
        LectureRetriever()
    )

    query = (
        "What is normalization?"
    )

    results = (
        retriever.retrieve(
            query,
            top_k=3
        )
    )

    print(
        "\nTop Chunks:\n"
    )

    for chunk in results:

        print(
            f"\nID: "
            f"{chunk['id']}"
        )

        print(
            f"Distance: "
            f"{chunk['distance']}"
        )

        print(
            chunk["text"][:300]
        )

        print(
            "\n----------------"
        )