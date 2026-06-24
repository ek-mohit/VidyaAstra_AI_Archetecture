"""
notes_generator.py

Generates:

1. Detailed Notes
2. Revision Notes
3. Key Concepts
4. Important Questions

Input:
outputs/fusion/knowledge.txt
"""

import os

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline
)


class NotesGenerator:

    def __init__(self):

        model_name = (
            "Qwen/Qwen2.5-3B-Instruct"
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                model_name
            )
        )

        self.model = (
            AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto"
            )
        )

        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )

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

    def generate(
        self,
        prompt
    ):

        result = self.pipe(
            prompt,
            max_new_tokens=1500,
            do_sample=True,
            temperature=0.4
        )

        return result[0][
            "generated_text"
        ]

    def generate_detailed_notes(
        self,
        content
    ):

        prompt = f"""
You are an expert professor.

Create detailed academic notes.

Content:

{content}

Include:

1. Topics
2. Concepts
3. Definitions
4. Examples
5. Explanations
"""

        return self.generate(
            prompt
        )

    def generate_revision_notes(
        self,
        content
    ):

        prompt = f"""
Create concise revision notes.

Content:

{content}

Include:

- Important points
- Key formulas
- Exam facts
"""

        return self.generate(
            prompt
        )

    def generate_key_concepts(
        self,
        content
    ):

        prompt = f"""
Extract important concepts.

Content:

{content}

Format:

Concept:
Explanation:
"""

        return self.generate(
            prompt
        )

    def generate_important_questions(
        self,
        content
    ):

        prompt = f"""
Generate 15 exam-oriented questions.

Content:

{content}
"""

        return self.generate(
            prompt
        )

    def save_output(
        self,
        text,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)


def run_notes_pipeline():

    generator = NotesGenerator()

    knowledge = (
        generator.load_knowledge(
            "outputs/fusion/knowledge.txt"
        )
    )

    os.makedirs(
        "outputs/notes",
        exist_ok=True
    )

    detailed = (
        generator.generate_detailed_notes(
            knowledge
        )
    )

    revision = (
        generator.generate_revision_notes(
            knowledge
        )
    )

    concepts = (
        generator.generate_key_concepts(
            knowledge
        )
    )

    questions = (
        generator.generate_important_questions(
            knowledge
        )
    )

    generator.save_output(
        detailed,
        "outputs/notes/detailed_notes.txt"
    )

    generator.save_output(
        revision,
        "outputs/notes/revision_notes.txt"
    )

    generator.save_output(
        concepts,
        "outputs/notes/key_concepts.txt"
    )

    generator.save_output(
        questions,
        "outputs/notes/important_questions.txt"
    )

    print(
        "Notes Generation Complete"
    )


if __name__ == "__main__":
    run_notes_pipeline()