"""
rag_pipeline.py

Complete RAG Pipeline

Flow:

Question
   ↓
Retriever
   ↓
Reranker
   ↓
Prompt Builder
   ↓
LLM
   ↓
Answer
"""

from ai.retriever import (
    LectureRetriever
)

from ai.reranker import (
    LectureReranker
)

from ai.prompt_builder import (
    PromptBuilder
)

from ai.llm_service import (
    LLMService
)


class VidyastraRAG:

    def __init__(self):

        self.retriever = (
            LectureRetriever()
        )

        self.reranker = (
            LectureReranker()
        )

        self.llm = (
            LLMService()
        )

    def retrieve_context(
        self,
        question,
        retrieval_k=20,
        final_k=5
    ):

        retrieved_chunks = (
            self.retriever.retrieve(
                query=question,
                top_k=retrieval_k
            )
        )

        ranked_chunks = (
            self.reranker.rerank(
                query=question,
                retrieved_chunks=retrieved_chunks,
                top_k=final_k
            )
        )

        context = (
            self.reranker.build_context(
                ranked_chunks
            )
        )

        return {
            "context": context,
            "chunks": ranked_chunks
        }

    def ask(
        self,
        question
    ):

        retrieval_result = (
            self.retrieve_context(
                question
            )
        )

        context = (
            retrieval_result[
                "context"
            ]
        )

        prompt = (
            PromptBuilder
            .build_tutor_prompt(
                question,
                context
            )
        )

        answer = (
            self.llm.generate(
                prompt,
                max_tokens=1000
            )
        )

        return {
            "question":
                question,

            "answer":
                answer,

            "context":
                context,

            "sources":
                retrieval_result[
                    "chunks"
                ]
        }

    def ask_with_sources(
        self,
        question
    ):

        result = self.ask(
            question
        )

        answer = result["answer"]

        answer += (
            "\n\n---\nSources Used:\n"
        )

        for idx, source in enumerate(
            result["sources"],
            start=1
        ):

            answer += (
                f"\n[{idx}] "
                f"{source['id']}"
            )

        return answer

    def get_sources(
        self,
        question
    ):

        retrieval_result = (
            self.retrieve_context(
                question
            )
        )

        return retrieval_result[
            "chunks"
        ]


if __name__ == "__main__":

    rag = VidyastraRAG()

    while True:

        question = input(
            "\nAsk Question: "
        )

        if (
            question.lower()
            == "exit"
        ):
            break

        result = rag.ask(
            question
        )

        print(
            "\nANSWER:\n"
        )

        print(
            result["answer"]
        )

        print(
            "\nRetrieved Sources:"
        )

        for source in (
            result["sources"]
        ):

            print(
                f"\n{source['id']}"
            )

            print(
                f"Score: "
                f"{source['rerank_score']:.4f}"
            )