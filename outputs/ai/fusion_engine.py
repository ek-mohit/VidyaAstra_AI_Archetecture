"""
fusion_engine.py

Combines:

1. Transcript
2. OCR Results
3. Vision Analysis

Creates:

Unified Lecture Knowledge
"""

import json
from pathlib import Path


class KnowledgeFusionEngine:

    def __init__(self):
        pass

    def load_transcript(
        self,
        transcript_json_path
    ):

        with open(
            transcript_json_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def load_vision_results(
        self,
        vision_json_path
    ):

        with open(
            vision_json_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def extract_transcript_text(
        self,
        transcript_data
    ):

        segments = transcript_data[
            "segments"
        ]

        return "\n".join(
            seg["text"]
            for seg in segments
        )

    def extract_visual_knowledge(
        self,
        vision_data
    ):

        visual_context = []

        for frame in vision_data:

            visual_context.append(
                {
                    "frame":
                        frame["image"],
                    "type":
                        frame["content_type"],
                    "ocr":
                        frame["ocr_text"],
                    "analysis":
                        frame["analysis"]
                }
            )

        return visual_context

    def build_unified_document(
        self,
        transcript_data,
        vision_data
    ):

        transcript_text = (
            self.extract_transcript_text(
                transcript_data
            )
        )

        visual_context = (
            self.extract_visual_knowledge(
                vision_data
            )
        )

        document = {
            "language":
                transcript_data.get(
                    "language",
                    "unknown"
                ),

            "lecture_content":
                transcript_text,

            "visual_content":
                visual_context,

            "combined_context":
                self.combine_text(
                    transcript_text,
                    visual_context
                )
        }

        return document

    def combine_text(
        self,
        transcript_text,
        visual_context
    ):

        combined = []

        combined.append(
            "===== LECTURE TRANSCRIPT =====\n"
        )

        combined.append(
            transcript_text
        )

        combined.append(
            "\n\n===== VISUAL CONTENT =====\n"
        )

        for item in visual_context:

            combined.append(
                f"\nFRAME: {item['frame']}"
            )

            combined.append(
                f"\nTYPE: {item['type']}"
            )

            combined.append(
                f"\nOCR:\n{item['ocr']}"
            )

            combined.append(
                f"\nVISION ANALYSIS:\n"
                f"{item['analysis']}\n"
            )

        return "\n".join(
            combined
        )

    def save_knowledge(
        self,
        knowledge,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                knowledge,
                f,
                indent=4,
                ensure_ascii=False
            )

    def save_text_version(
        self,
        knowledge,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                knowledge[
                    "combined_context"
                ]
            )


def run_fusion_pipeline():

    engine = KnowledgeFusionEngine()

    transcript = engine.load_transcript(
        "outputs/transcripts/lecture.json"
    )

    vision = engine.load_vision_results(
        "outputs/vision/vision_results.json"
    )

    knowledge = (
        engine.build_unified_document(
            transcript,
            vision
        )
    )

    Path(
        "outputs/fusion"
    ).mkdir(
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


if __name__ == "__main__":
    run_fusion_pipeline()