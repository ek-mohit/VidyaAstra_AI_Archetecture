# pipeline.py

from extract_audio import extract_audio

from extract_frames import extract_frames

from video_metadata import get_video_metadata

from scene_detector import detect_scenes


def process_video(video_path):

    metadata = get_video_metadata(video_path)

    audio_file = extract_audio(video_path)

    frames = extract_frames(video_path)

    scenes = detect_scenes(video_path)

    return {
        "metadata": metadata,
        "audio_file": audio_file,
        "frames": frames,
        "scenes": scenes
    }


if __name__ == "__main__":

    result = process_video(
        "sample_lecture.mp4"
    )

    print(result)