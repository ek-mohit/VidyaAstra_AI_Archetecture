"""
processing_pipeline.py

Master AI Pipeline

Flow:

Video
 ↓
Extract Audio
 ↓
Transcription
 ↓
Frame Extraction
 ↓
Vision Analysis
 ↓
Knowledge Fusion
 ↓
Notes
 ↓
Quiz
 ↓
Assignments
 ↓
Flashcards
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector DB

Output:
Complete Lecture Package
"""

import os
import json
from pathlib import Path

# VIDEO PROCESSOR
from video_processor.extract_audio import (
    extract_audio
)

from video_processor.extract_frames import (
    extract_frames
)

# AI MODULES
from ai.transcription import (
    process_audio
)

from ai.vision import (
    VisionAnalyzer
)

from ai.fusion_engine import (
    KnowledgeFusionEngine
)

from ai.notes_generator import (
    NotesGenerator
)

from ai.quiz_generator import (
    QuizGenerator
)

from ai.assignment_generator import (
    AssignmentGenerator
)

from ai.flashcard_generator import (
    FlashcardGenerator
)

from ai.vector_store import (
    LectureVectorStore
)


class VidyastraPipeline:

    def __init__(self):

        self.output_root = "outputs"

        Path(
            self.output_root
        ).mkdir(
            exist_ok=True
        )

    # ----------------------------------
    # STEP 1
    # ----------------------------------

    def process_video(
        self,
        video_path
    ):

        print(
            "\n[1/9] Extracting Audio..."
        )

        audio_path = extract_audio(
            video_path
        )

        print(
            f"Audio saved: {audio_path}"
        )

        print(
            "\n[2/9] Extracting Frames..."
        )

        frames = extract_frames(
            video_path
        )

        print(
            f"{len(frames)} frames extracted"
        )

        return audio_path, frames

    # ----------------------------------
    # STEP 2
    # ----------------------------------

    def transcribe_audio(
        self,
        audio_path
    ):

        print(
            "\n[3/9] Running Transcription..."
        )

        result = process_audio(
            audio_path
        )

        print(
            "Transcription Complete"
        )

        return result

    # ----------------------------------
    # STEP 3
    # ----------------------------------

    def analyze_frames(
        self,
        frame_folder
    ):

        print(
            "\n[4/9] Running Vision Analysis..."
        )

        analyzer = VisionAnalyzer()

        results = (
            analyzer.process_frames(
                frame_folder
            )
        )

        os.makedirs(
            "outputs/vision",
            exist_ok=True
        )

        output_file = (
            "outputs/vision/"
            "vision_results.json"
        )

        analyzer.save_results(
            results,
            output_file
        )

        print(
            "Vision Analysis Complete"
        )

        return output_file

    # ----------------------------------
    # STEP 4
    # ----------------------------------

    def build_knowledge(
        self,
        transcript_json,
        vision_json
    ):

        print(
            "\n[5/9] Building Knowledge Base..."
        )

        engine = (
            KnowledgeFusionEngine()
        )

        transcript = (
            engine.load_transcript(
                transcript_json
            )
        )

        vision = (
            engine.load_vision_results(
                vision_json
            )
        )

        knowledge = (
            engine.build_unified_document(
                transcript,
                vision
            )
        )

        os.makedirs(
            "outputs/fusion",
            exist_ok=True
        )

        engine.save_knowledge(
            knowledge,
            "outputs/fusion/knowledge.json"
        )

        engine.save_text_version(
            knowledge,
            "outputs/fusion/knowledge.txt"
        )

        print(
            "Knowledge Fusion Complete"
        )

        return (
            "outputs/fusion/"
            "knowledge.txt"
        )

    # ----------------------------------
    # STEP 5
    # ----------------------------------

    def generate_notes(
        self,
        knowledge_file
    ):

        print(
            "\n[6/9] Generating Notes..."
        )

        generator = NotesGenerator()

        content = (
            generator.load_knowledge(
                knowledge_file
            )
        )

        os.makedirs(
            "outputs/notes",
            exist_ok=True
        )

        notes = (
            generator.generate_detailed_notes(
                content
            )
        )

        generator.save_output(
            notes,
            "outputs/notes/"
            "detailed_notes.txt"
        )

        print(
            "Notes Generated"
        )

    # ----------------------------------
    # STEP 6
    # ----------------------------------

    def generate_quizzes(
        self,
        knowledge_file
    ):

        print(
            "\n[7/9] Generating Quiz..."
        )

        generator = QuizGenerator()

        content = (
            generator.load_knowledge(
                knowledge_file
            )
        )

        os.makedirs(
            "outputs/quizzes",
            exist_ok=True
        )

        quiz = (
            generator.generate_mcq_quiz(
                content
            )
        )

        generator.save(
            quiz,
            "outputs/quizzes/mcq.txt"
        )

        print(
            "Quiz Generated"
        )

    # ----------------------------------
    # STEP 7
    # ----------------------------------

    def generate_assignments(
        self,
        knowledge_file
    ):

        print(
            "\n[8/9] Generating Assignments..."
        )

        generator = (
            AssignmentGenerator()
        )

        content = (
            generator.load_knowledge(
                knowledge_file
            )
        )

        os.makedirs(
            "outputs/assignments",
            exist_ok=True
        )

        assignment = (
            generator
            .generate_medium_assignment(
                content
            )
        )

        generator.save(
            assignment,
            "outputs/assignments/"
            "assignment.txt"
        )

        print(
            "Assignment Generated"
        )

    # ----------------------------------
    # STEP 8
    # ----------------------------------

    def generate_flashcards(
        self,
        knowledge_file
    ):

        print(
            "\n[9/9] Generating Flashcards..."
        )

        generator = (
            FlashcardGenerator()
        )

        content = (
            generator.load_knowledge(
                knowledge_file
            )
        )

        response = (
            generator.generate_flashcards(
                content
            )
        )

        cards = (
            generator.parse_flashcards(
                response
            )
        )

        os.makedirs(
            "outputs/flashcards",
            exist_ok=True
        )

        generator.save_json(
            cards,
            "outputs/flashcards/cards.json"
        )

        print(
            f"{len(cards)} flashcards generated"
        )

    # ----------------------------------
    # STEP 9
    # ----------------------------------

    def create_vector_db(
        self,
        knowledge_file
    ):

        print(
            "\n[FINAL] Creating Vector DB..."
        )

        with open(
            knowledge_file,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        chunks = []

        chunk_size = 1000

        for i in range(
            0,
            len(content),
            chunk_size
        ):

            chunks.append(
                content[
                    i:i + chunk_size
                ]
            )

        store = (
            LectureVectorStore()
        )

        store.add_chunks(
            chunks
        )

        print(
            "Vector Database Ready"
        )

    # ----------------------------------
    # MAIN EXECUTION
    # ----------------------------------

    def run(
        self,
        video_path
    ):

        audio_path, frames = (
            self.process_video(
                video_path
            )
        )

        transcript_info = (
            self.transcribe_audio(
                audio_path
            )
        )

        transcript_json = (
            transcript_info["json"]
        )

        frame_folder = os.path.dirname(
            frames[0]
        )

        vision_json = (
            self.analyze_frames(
                frame_folder
            )
        )

        knowledge_file = (
            self.build_knowledge(
                transcript_json,
                vision_json
            )
        )

        self.generate_notes(
            knowledge_file
        )

        self.generate_quizzes(
            knowledge_file
        )

        self.generate_assignments(
            knowledge_file
        )

        self.generate_flashcards(
            knowledge_file
        )

        self.create_vector_db(
            knowledge_file
        )

        print(
            "\n================================"
        )

        print(
            "VIDYASTRA PIPELINE COMPLETE"
        )

        print(
            "================================"
        )


# --------------------------------------
# ENTRY POINT
# --------------------------------------

if __name__ == "__main__":

    VIDEO_PATH = (
        "sample_lecture.mp4"
    )

    pipeline = (
        VidyastraPipeline()
    )

    pipeline.run(
        VIDEO_PATH
    )