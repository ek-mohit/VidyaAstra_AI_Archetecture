# scene_detector.py

from scenedetect import (
    open_video,
    SceneManager
)

from scenedetect.detectors import ContentDetector


def detect_scenes(video_path):

    video = open_video(video_path)

    scene_manager = SceneManager()

    scene_manager.add_detector(
        ContentDetector()
    )

    scene_manager.detect_scenes(
        video
    )

    scenes = scene_manager.get_scene_list()

    return scenes