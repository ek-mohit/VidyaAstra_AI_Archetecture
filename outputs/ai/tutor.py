"""
tutor.py

Lecture-based AI Tutor
using RAG.
"""

from ai.vector_store import (
    LectureVectorStore
)

from ai.llm_service import (
    LLMService
)


class LectureTutor:

    def __init__(self):

        self.store = (
            LectureVectorStore()
        )

        self.llm = (
            LLMService()
        )

    def answer_question(
        self,
        question
    ):

        search_result = (
            self.store.search(
                question,
                top_k=5
            )
        )

        docs = (
            search_result["documents"][0]
        )

        context = "\n\n".join(
            docs
        )

        prompt = f"""
You are a lecture tutor.

Answer ONLY from
the provided context.

If answer is unavailable,
say:

"Not covered in lecture."

CONTEXT:

{context}

QUESTION:

{question}
"""

        answer = (
            self.llm.generate(
                prompt,
                max_tokens=500
            )
        )

        return answer


if __name__ == "__main__":

    tutor = LectureTutor()

    while True:

        q = input(
            "\nAsk Question: "
        )

        if q.lower() == "exit":
            break

        response = (
            tutor.answer_question(q)
        )

        print("\nAnswer:\n")

        print(response)