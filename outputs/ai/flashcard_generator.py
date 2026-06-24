"""
flashcard_generator.py

Generates:

1. Basic Flashcards
2. Definition Cards
3. Formula Cards
4. Concept Cards

Output:
JSON + TXT

Input:
outputs/fusion/knowledge.txt
"""

import os
import json

from ai.llm_service import (
    LLMService
)


class FlashcardGenerator:

    def __init__(self):

        self.llm = LLMService()

    def load_knowledge(
        self,
        file_path
    ):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    def generate_flashcards(
        self,
        content
    ):

        prompt = f"""
Generate educational flashcards.

Return ONLY valid JSON.

Format:

[
    {{
        "front": "Question",
        "back": "Answer",
        "type": "concept"
    }}
]

Generate 30 flashcards.

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            2500
        )

    def parse_flashcards(
        self,
        llm_response
    ):

        try:

            start = llm_response.find("[")

            end = llm_response.rfind("]")

            json_part = (
                llm_response[
                    start:end+1
                ]
            )

            cards = json.loads(
                json_part
            )

            return cards

        except Exception:

            return []

    def save_json(
        self,
        flashcards,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                flashcards,
                f,
                indent=4,
                ensure_ascii=False
            )

    def save_text(
        self,
        flashcards,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            for i, card in enumerate(
                flashcards,
                start=1
            ):

                f.write(
                    f"Flashcard {i}\n"
                )

                f.write(
                    f"Front: "
                    f"{card['front']}\n"
                )

                f.write(
                    f"Back: "
                    f"{card['back']}\n"
                )

                f.write(
                    f"Type: "
                    f"{card['type']}\n"
                )

                f.write(
                    "-" * 50
                    + "\n"
                )


def run_flashcard_pipeline():

    generator = (
        FlashcardGenerator()
    )

    knowledge = (
        generator.load_knowledge(
            "outputs/fusion/knowledge.txt"
        )
    )

    response = (
        generator.generate_flashcards(
            knowledge
        )
    )

    flashcards = (
        generator.parse_flashcards(
            response
        )
    )

    os.makedirs(
        "outputs/flashcards",
        exist_ok=True
    )

    generator.save_json(
        flashcards,
        "outputs/flashcards/cards.json"
    )

    generator.save_text(
        flashcards,
        "outputs/flashcards/cards.txt"
    )

    print(
        f"Generated "
        f"{len(flashcards)} "
        f"flashcards"
    )


if __name__ == "__main__":

    run_flashcard_pipeline()