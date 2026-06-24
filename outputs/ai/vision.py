"""
vision.py

Features:
- OCR Extraction
- Vision Analysis
- Content Classification
- Frame Summarization
- Batch Processing

Model:
Qwen2.5-VL
"""

import os
import json
from PIL import Image

from transformers import (
    AutoProcessor,
    AutoModelForImageTextToText
)

from paddleocr import PaddleOCR


class VisionAnalyzer:

    def __init__(self):

        print("Loading OCR...")

        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en'
        )

        print("Loading Qwen2.5-VL...")

        model_name = "Qwen/Qwen2.5-VL-3B-Instruct"

        self.processor = AutoProcessor.from_pretrained(
            model_name
        )

        self.model = AutoModelForImageTextToText.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )

    def extract_text(
        self,
        image_path
    ):

        result = self.ocr.ocr(
            image_path
        )

        extracted_text = []

        for page in result:

            for line in page:

                extracted_text.append(
                    line[1][0]
                )

        return "\n".join(
            extracted_text
        )

    def analyze_image(
        self,
        image_path
    ):

        image = Image.open(
            image_path
        ).convert("RGB")

        prompt = """
You are analyzing a lecture slide.

Return:

1. Content Type
   (Slide / Whiteboard / Diagram / Code / Table)

2. Main Topics

3. Important Concepts

4. Summary

5. Possible Quiz Questions
"""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.processor(
            text=[text],
            images=[image],
            return_tensors="pt"
        )

        inputs = {
            k: v.to(
                self.model.device
            )
            for k, v in inputs.items()
        }

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=1024
        )

        result = self.processor.batch_decode(
            output_ids,
            skip_special_tokens=True
        )[0]

        return result

    def classify_content(
        self,
        ocr_text
    ):

        text = ocr_text.lower()

        if "class" in text and "public" in text:
            return "Code"

        if "table" in text:
            return "Table"

        if "algorithm" in text:
            return "Slide"

        return "Unknown"

    def process_frame(
        self,
        image_path
    ):

        ocr_text = self.extract_text(
            image_path
        )

        content_type = self.classify_content(
            ocr_text
        )

        ai_analysis = self.analyze_image(
            image_path
        )

        return {
            "image": image_path,
            "content_type": content_type,
            "ocr_text": ocr_text,
            "analysis": ai_analysis
        }

    def process_frames(
        self,
        frame_folder
    ):

        results = []

        files = sorted(
            os.listdir(frame_folder)
        )

        for file in files:

            if file.endswith(
                (".jpg", ".png", ".jpeg")
            ):

                path = os.path.join(
                    frame_folder,
                    file
                )

                print(
                    f"Processing {file}"
                )

                data = self.process_frame(
                    path
                )

                results.append(
                    data
                )

        return results

    def save_results(
        self,
        results,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results,
                f,
                indent=4,
                ensure_ascii=False
            )


if __name__ == "__main__":

    analyzer = VisionAnalyzer()

    results = analyzer.process_frames(
        "outputs/frames/sample_lecture"
    )

    analyzer.save_results(
        results,
        "outputs/vision/vision_results.json"
    )

    print(
        f"Processed {len(results)} frames"
    )