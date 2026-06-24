"""
embeddings.py

Creates embeddings
for lecture knowledge.
"""

from sentence_transformers import (
    SentenceTransformer
)


class EmbeddingService:

    def __init__(self):

        self.model = (
            SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )
        )

    def embed_text(
        self,
        text
    ):

        return self.model.encode(
            text
        )

    def embed_batch(
        self,
        texts
    ):

        return self.model.encode(
            texts
        )


if __name__ == "__main__":

    service = EmbeddingService()

    emb = service.embed_text(
        "Normalization reduces redundancy."
    )

    print(emb.shape)