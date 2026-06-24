"""
quiz_generator.py

Creates:

1. MCQ Quiz
2. True False Quiz
3. Short Answer Quiz
4. Long Answer Questions
"""

import os

from ai.llm_service import (
    LLMService
)


class QuizGenerator:

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

    def generate_mcq_quiz(
        self,
        content
    ):

        prompt = f"""
Create 20 multiple-choice questions.

Requirements:

- 4 options
- mark correct answer
- educational quality

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            2000
        )

    def generate_true_false(
        self,
        content
    ):

        prompt = f"""
Create 20 True/False questions.

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            1500
        )

    def generate_short_answer(
        self,
        content
    ):

        prompt = f"""
Create 15 short answer questions.

Content:

{content}
"""

        return self.llm.generate(
            prompt,
            1500
        )

    def generate_long_answer(
        self,
        content
    ):

        prompt = f"""
Create 10 long answer exam questions.

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


def run_quiz_pipeline():

    generator = QuizGenerator()

    knowledge = (
        generator.load_knowledge(
            "outputs/fusion/knowledge.txt"
        )
    )

    os.makedirs(
        "outputs/quizzes",
        exist_ok=True
    )

    mcq = generator.generate_mcq_quiz(
        knowledge
    )

    tf = generator.generate_true_false(
        knowledge
    )

    short_q = (
        generator.generate_short_answer(
            knowledge
        )
    )

    long_q = (
        generator.generate_long_answer(
            knowledge
        )
    )

    generator.save(
        mcq,
        "outputs/quizzes/mcq.txt"
    )

    generator.save(
        tf,
        "outputs/quizzes/true_false.txt"
    )

    generator.save(
        short_q,
        "outputs/quizzes/short_answer.txt"
    )

    generator.save(
        long_q,
        "outputs/quizzes/long_answer.txt"
    )

    print(
        "Quiz Generation Complete"
    )


if __name__ == "__main__":

    run_quiz_pipeline()