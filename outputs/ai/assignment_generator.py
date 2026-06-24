"""
assignment_generator.py

Generates:

1. Easy Assignment
2. Medium Assignment
3. Advanced Assignment
4. Practical Assignment
5. Viva Questions

Input:
outputs/fusion/knowledge.txt
"""

import os

from ai.llm_service import (
    LLMService
)


class AssignmentGenerator:

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

    def generate_easy_assignment(
        self,
        content
    ):

        prompt = f"""
Create an EASY academic assignment.

Requirements:

- 10 questions
- Beginner level
- Concept understanding

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            1500
        )

    def generate_medium_assignment(
        self,
        content
    ):

        prompt = f"""
Create a MEDIUM difficulty assignment.

Requirements:

- 10 questions
- Application based
- Real world examples

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            1500
        )

    def generate_advanced_assignment(
        self,
        content
    ):

        prompt = f"""
Create an ADVANCED assignment.

Requirements:

- Critical thinking
- Analysis questions
- Design questions
- Research questions

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            2000
        )

    def generate_practical_assignment(
        self,
        content
    ):

        prompt = f"""
Create practical/lab based tasks.

Requirements:

- Hands-on exercises
- Mini project ideas
- Implementation tasks

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            2000
        )

    def generate_viva_questions(
        self,
        content
    ):

        prompt = f"""
Generate 25 viva questions.

Requirements:

- Short answer
- Interview style
- Concept clarity

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            1500
        )

    def save(
        self,
        text,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)


def run_assignment_pipeline():

    generator = AssignmentGenerator()

    knowledge = (
        generator.load_knowledge(
            "outputs/fusion/knowledge.txt"
        )
    )

    os.makedirs(
        "outputs/assignments",
        exist_ok=True
    )

    easy = (
        generator.generate_easy_assignment(
            knowledge
        )
    )

    medium = (
        generator.generate_medium_assignment(
            knowledge
        )
    )

    advanced = (
        generator.generate_advanced_assignment(
            knowledge
        )
    )

    practical = (
        generator.generate_practical_assignment(
            knowledge
        )
    )

    viva = (
        generator.generate_viva_questions(
            knowledge
        )
    )

    generator.save(
        easy,
        "outputs/assignments/easy.txt"
    )

    generator.save(
        medium,
        "outputs/assignments/medium.txt"
    )

    generator.save(
        advanced,
        "outputs/assignments/advanced.txt"
    )

    generator.save(
        practical,
        "outputs/assignments/practical.txt"
    )

    generator.save(
        viva,
        "outputs/assignments/viva.txt"
    )

    print(
        "Assignment Generation Complete"
    )


if __name__ == "__main__":

    run_assignment_pipeline()