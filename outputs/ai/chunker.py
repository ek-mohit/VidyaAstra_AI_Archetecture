"""
chunker.py

Responsible for:

1. Smart Text Chunking
2. Overlapping Chunks
3. Metadata Generation
4. RAG Optimization
"""

import json
import os
from typing import List


class LectureChunker:

    def __init__(
        self,
        chunk_size=1000,
        overlap=200
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def load_text(
        self,
        file_path
    ):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    def chunk_text(
        self,
        text
    ):

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += (
                self.chunk_size
                - self.overlap
            )

        return chunks

    def chunk_by_paragraphs(
        self,
        text
    ):

        paragraphs = text.split("\n")

        chunks = []

        current_chunk = ""

        for para in paragraphs:

            if (
                len(current_chunk)
                + len(para)
                < self.chunk_size
            ):

                current_chunk += (
                    para + "\n"
                )

            else:

                chunks.append(
                    current_chunk
                )

                current_chunk = para

        if current_chunk:

            chunks.append(
                current_chunk
            )

        return chunks

    def create_chunk_objects(
        self,
        chunks
    ):

        chunk_objects = []

        for idx, chunk in enumerate(
            chunks
        ):

            chunk_objects.append(
                {
                    "chunk_id":
                        idx + 1,

                    "text":
                        chunk,

                    "length":
                        len(chunk)
                }
            )

        return chunk_objects

    def save_chunks(
        self,
        chunk_objects,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                chunk_objects,
                f,
                indent=4,
                ensure_ascii=False
            )

    def process_file(
        self,
        input_file,
        output_file
    ):

        text = self.load_text(
            input_file
        )

        chunks = (
            self.chunk_by_paragraphs(
                text
            )
        )

        chunk_objects = (
            self.create_chunk_objects(
                chunks
            )
        )

        self.save_chunks(
            chunk_objects,
            output_file
        )

        return chunk_objects


if __name__ == "__main__":

    chunker = LectureChunker(
        chunk_size=1200,
        overlap=200
    )

    chunks = (
        chunker.process_file(
            "outputs/fusion/knowledge.txt",
            "outputs/chunks/chunks.json"
        )
    )

    print(
        f"Generated {len(chunks)} chunks"
    )