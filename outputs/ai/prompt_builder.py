"""
prompt_builder.py

Builds prompts for:

1. AI Tutor
2. Notes
3. Quiz
4. Assignment
5. Flashcards

Main focus:
Lecture-specific RAG Tutor
"""


class PromptBuilder:

    @staticmethod
    def build_tutor_prompt(
        question,
        context
    ):

        prompt = f"""
You are Vidyastra AI.

You are an educational assistant.

Your job:

1. Answer ONLY from provided context.
2. Do NOT invent information.
3. If answer is unavailable,
   say:

   "This topic was not covered in the lecture."

4. Explain clearly.
5. Use bullet points when useful.
6. Give examples if available.

===================================
LECTURE CONTEXT
===================================

{context}

===================================
QUESTION
===================================

{question}

===================================
ANSWER
===================================
"""

        return prompt

    @staticmethod
    def build_notes_prompt(
        lecture_content
    ):

        prompt = f"""
Generate detailed academic notes.

Requirements:

- Proper headings
- Sub-headings
- Definitions
- Examples
- Important concepts

LECTURE CONTENT:

{lecture_content}
"""

        return prompt

    @staticmethod
    def build_quiz_prompt(
        lecture_content
    ):

        prompt = f"""
Generate 20 MCQs.

Requirements:

- 4 options
- Mark correct answer
- Educational quality

LECTURE CONTENT:

{lecture_content}
"""

        return prompt

    @staticmethod
    def build_assignment_prompt(
        lecture_content
    ):

        prompt = f"""
Generate an academic assignment.

Requirements:

- Easy Questions
- Medium Questions
- Advanced Questions

LECTURE CONTENT:

{lecture_content}
"""

        return prompt

    @staticmethod
    def build_flashcard_prompt(
        lecture_content
    ):

        prompt = f"""
Generate flashcards.

Return JSON format:

[
  {{
    "front":"question",
    "back":"answer"
  }}
]

LECTURE CONTENT:

{lecture_content}
"""

        return prompt

    @staticmethod
    def build_summary_prompt(
        lecture_content
    ):

        prompt = f"""
Create lecture summary.

Requirements:

- Key Concepts
- Important Definitions
- Quick Revision Notes

LECTURE CONTENT:

{lecture_content}
"""

        return prompt


if __name__ == "__main__":

    sample_context = """
Normalization removes redundancy.

1NF removes repeating groups.

2NF removes partial dependency.

3NF removes transitive dependency.
"""

    sample_question = (
        "What is 3NF?"
    )

    prompt = (
        PromptBuilder.build_tutor_prompt(
            sample_question,
            sample_context
        )
    )

    print(prompt)