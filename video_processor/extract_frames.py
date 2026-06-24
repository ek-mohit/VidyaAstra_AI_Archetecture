# extract_frames.py

import cv2
import os

from video_processor.config import (
    FRAME_OUTPUT_DIR,
    FRAME_INTERVAL_SECONDS
)

from video_processor.utils import (
    create_dir,
    get_filename_without_ext
)


def extract_frames(video_path):

    video_name = get_filename_without_ext(video_path)

    save_dir = os.path.join(
        FRAME_OUTPUT_DIR,
        video_name
    )

    create_dir(save_dir)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_interval = int(
        fps * FRAME_INTERVAL_SECONDS
    )

    frame_count = 0

    saved_frames = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_count % frame_interval == 0:

            frame_path = os.path.join(
                save_dir,
                f"frame_{frame_count}.jpg"
            )

            cv2.imwrite(frame_path, frame)

            saved_frames.append(frame_path)

        frame_count += 1

    cap.release()

    return saved_frames