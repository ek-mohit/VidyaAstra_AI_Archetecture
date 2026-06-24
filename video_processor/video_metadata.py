# video_metadata.py

import cv2


def get_video_metadata(video_path):

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    duration = frames / fps

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    cap.release()

    return {
        "fps": fps,
        "duration_seconds": duration,
        "width": width,
        "height": height
    }