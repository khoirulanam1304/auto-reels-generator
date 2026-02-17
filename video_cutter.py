import subprocess
import random
import os

class VideoCutter:
    def __init__(self, input_video, output_dir, target_width=720, target_height=1280):
        self.input_video = input_video
        self.output_dir = output_dir
        self.target_width = target_width
        self.target_height = target_height

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def cut_random_clip(self, duration=12, output_name="clip.mp4"):
        start_time = random.randint(0, 600)
        output_path = os.path.join(self.output_dir, output_name)

        command = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", self.input_video,
            "-t", str(duration),
            "-vf",
            f"scale={self.target_width}:{self.target_height}:force_original_aspect_ratio=increase,"
            f"crop={self.target_width}:{self.target_height}",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            output_path
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output_path
