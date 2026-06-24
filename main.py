"""
main.py

Vidyastra AI Entry Point

Features:

1. Process Lecture Video
2. Ask Questions
3. Generate Notes
4. Generate Quiz
5. Generate Assignments
6. Generate Flashcards
"""

import os

from ai.processing_pipeline import (
    VidyastraPipeline
)

from ai.rag_pipeline import (
    VidyastraRAG
)


class VidyastraAI:

    def __init__(self):

        self.pipeline = (
            VidyastraPipeline()
        )

        self.rag = (
            VidyastraRAG()
        )

    def process_lecture(
        self,
        video_path
    ):

        if not os.path.exists(
            video_path
        ):

            raise FileNotFoundError(
                f"Video not found: {video_path}"
            )

        print(
            "\nStarting Lecture Processing..."
        )

        self.pipeline.run(
            video_path
        )

        print(
            "\nLecture Processing Complete."
        )

    def ask(
        self,
        question
    ):

        result = self.rag.ask(
            question
        )

        return result["answer"]

    def chat_mode(
        self
    ):

        print(
            "\nVidyastra AI Tutor"
        )

        print(
            "Type 'exit' to quit.\n"
        )

        while True:

            question = input(
                "You: "
            )

            if (
                question.lower()
                == "exit"
            ):
                break

            response = (
                self.ask(
                    question
                )
            )

            print(
                "\nAI:"
            )

            print(response)

            print(
                "\n"
            )


def show_menu():

    print("\n")

    print("=" * 50)

    print(
        "VIDYASTRA AI"
    )

    print("=" * 50)

    print(
        "1. Process Lecture Video"
    )

    print(
        "2. Ask Questions"
    )

    print(
        "3. Interactive Tutor"
    )

    print(
        "4. Exit"
    )

    print("=" * 50)


def main():

    app = VidyastraAI()

    while True:

        show_menu()

        choice = input(
            "\nEnter Choice: "
        )

        if choice == "1":

            video_path = input(
                "\nVideo Path: "
            )

            try:

                app.process_lecture(
                    video_path
                )

            except Exception as e:

                print(
                    f"\nError: {e}"
                )

        elif choice == "2":

            question = input(
                "\nQuestion: "
            )

            try:

                answer = app.ask(
                    question
                )

                print(
                    "\nAnswer:\n"
                )

                print(answer)

            except Exception as e:

                print(
                    f"\nError: {e}"
                )

        elif choice == "3":

            app.chat_mode()

        elif choice == "4":

            print(
                "\nGoodbye!"
            )

            break

        else:

            print(
                "\nInvalid Option"
            )


if __name__ == "__main__":

    main()

