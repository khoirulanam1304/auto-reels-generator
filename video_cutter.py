import subprocess
import random
import os

class VideoCutter:
    def __init__(self, input_video, output_dir):
        self.input_video = input_video
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def cut_random_clip(self, duration=8, output_name="clip.mp4"):
        start_time = random.randint(0, 600)
        output_path = os.path.join(self.output_dir, output_name)

        command = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", self.input_video,
            "-t", str(duration),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:a", "copy",
            output_path
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output_path