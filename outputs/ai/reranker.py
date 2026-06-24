"""
reranker.py

Re-ranks retrieved chunks
using a Cross Encoder.
"""

from sentence_transformers import (
    CrossEncoder
)


class LectureReranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query,
        retrieved_chunks,
        top_k=5
    ):

        if not retrieved_chunks:
            return []

        pairs = []

        for chunk in retrieved_chunks:

            pairs.append(
                (
                    query,
                    chunk["text"]
                )
            )

        scores = self.model.predict(
            pairs
        )

        ranked_results = []

        for chunk, score in zip(
            retrieved_chunks,
            scores
        ):

            ranked_results.append(
                {
                    **chunk,
                    "rerank_score":
                        float(score)
                }
            )

        ranked_results.sort(
            key=lambda x:
                x["rerank_score"],
            reverse=True
        )

        return ranked_results[:top_k]

    def build_context(
        self,
        ranked_chunks
    ):

        context = []

        for chunk in ranked_chunks:

            context.append(
                chunk["text"]
            )

        return "\n\n".join(
            context
        )


if __name__ == "__main__":

    query = (
        "Explain Third Normal Form"
    )

    retrieved_chunks = [

        {
            "id": "chunk_1",
            "text":
                "Third Normal Form removes "
                "transitive dependency."
        },

        {
            "id": "chunk_2",
            "text":
                "Binary Trees are hierarchical "
                "data structures."
        },

        {
            "id": "chunk_3",
            "text":
                "A relation is in 3NF if "
                "there are no transitive "
                "dependencies."
        }
    ]

    reranker = (
        LectureReranker()
    )

    ranked = reranker.rerank(
        query,
        retrieved_chunks,
        top_k=2
    )

    print("\nRanked Results:\n")

    for item in ranked:

        print(
            f"Score: "
            f"{item['rerank_score']:.4f}"
        )

        print(
            item["text"]
        )

        print(
            "-" * 50
        )