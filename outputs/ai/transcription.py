"""
transcription.py

Features:
- Faster Whisper
- Auto language detection
- Transcript JSON
- Transcript TXT
- Subtitle (SRT)
- RAG-ready chunks
"""

import json
import os
from pathlib import Path
from faster_whisper import WhisperModel


class LectureTranscriber:

    def __init__(
        self,
        model_size="base",
        device="cpu",
        compute_type="int8"
    ):

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(
        self,
        audio_path,
        beam_size=5
    ):

        segments, info = self.model.transcribe(
            audio_path,
            beam_size=beam_size
        )

        result = []

        for segment in segments:

            result.append(
                {
                    "start": round(segment.start, 2),
                    "end": round(segment.end, 2),
                    "text": segment.text.strip()
                }
            )

        return {
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "segments": result
        }

    def transcript_to_text(
        self,
        transcript
    ):

        return "\n".join(
            seg["text"]
            for seg in transcript["segments"]
        )

    def save_text(
        self,
        transcript,
        output_file
    ):

        text = self.transcript_to_text(
            transcript
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

    def save_json(
        self,
        transcript,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                transcript,
                f,
                indent=4,
                ensure_ascii=False
            )

    def seconds_to_srt_time(
        self,
        seconds
    ):

        hours = int(seconds // 3600)

        minutes = int(
            (seconds % 3600) // 60
        )

        secs = int(seconds % 60)

        millis = int(
            (seconds - int(seconds))
            * 1000
        )

        return (
            f"{hours:02}:{minutes:02}:"
            f"{secs:02},{millis:03}"
        )

    def save_srt(
        self,
        transcript,
        output_file
    ):

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            for idx, seg in enumerate(
                transcript["segments"],
                start=1
            ):

                start_time = self.seconds_to_srt_time(
                    seg["start"]
                )

                end_time = self.seconds_to_srt_time(
                    seg["end"]
                )

                f.write(f"{idx}\n")

                f.write(
                    f"{start_time} --> "
                    f"{end_time}\n"
                )

                f.write(
                    seg["text"] + "\n\n"
                )

    def create_rag_chunks(
        self,
        transcript,
        chunk_size=1000
    ):

        text = self.transcript_to_text(
            transcript
        )

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start = end

        return chunks

    def save_chunks(
        self,
        chunks,
        output_dir
    ):

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        for i, chunk in enumerate(
            chunks
        ):

            file_path = os.path.join(
                output_dir,
                f"chunk_{i+1}.txt"
            )

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(chunk)


def process_audio(
    audio_path,
    output_root="outputs"
):

    Path(output_root).mkdir(
        exist_ok=True
    )

    transcript_dir = os.path.join(
        output_root,
        "transcripts"
    )

    subtitle_dir = os.path.join(
        output_root,
        "subtitles"
    )

    chunk_dir = os.path.join(
        output_root,
        "chunks"
    )

    os.makedirs(
        transcript_dir,
        exist_ok=True
    )

    os.makedirs(
        subtitle_dir,
        exist_ok=True
    )

    os.makedirs(
        chunk_dir,
        exist_ok=True
    )

    transcriber = LectureTranscriber(
        model_size="base"
    )

    transcript = transcriber.transcribe(
        audio_path
    )

    name = Path(
        audio_path
    ).stem

    json_file = os.path.join(
        transcript_dir,
        f"{name}.json"
    )

    txt_file = os.path.join(
        transcript_dir,
        f"{name}.txt"
    )

    srt_file = os.path.join(
        subtitle_dir,
        f"{name}.srt"
    )

    transcriber.save_json(
        transcript,
        json_file
    )

    transcriber.save_text(
        transcript,
        txt_file
    )

    transcriber.save_srt(
        transcript,
        srt_file
    )

    chunks = transcriber.create_rag_chunks(
        transcript
    )

    transcriber.save_chunks(
        chunks,
        os.path.join(
            chunk_dir,
            name
        )
    )

    return {
        "json": json_file,
        "text": txt_file,
        "subtitle": srt_file,
        "chunks": len(chunks),
        "language":
            transcript["language"]
    }


if __name__ == "__main__":

    result = process_audio(
        "lecture.wav"
    )

    print(result)