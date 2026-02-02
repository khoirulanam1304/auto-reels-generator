import subprocess
import os
from text_utils import write_wrapped_text_to_file

class ContentGenerator:
    def add_text_overlay(self, input_video, text, output_video):
        temp_text_file = "temp_text.txt"

        write_wrapped_text_to_file(text, temp_text_file)

        vf_filter = (
            "drawbox="
            "x=54:"
            "y=650:"
            "w=972:"
            "h=600:"
            "color=white:"
            "t=fill"
            ","
            "drawtext="
            "font=segoeui:"
            f"textfile='{temp_text_file}':"
            "fontcolor=black:"
            "fontsize=64:"
            "line_spacing=16:"
            "x=(w-text_w)/2:"
            "y=(h-text_h)/2"
        )
        
        command = [
            "ffmpeg",
            "-y",
            "-i", input_video,
            "-vf", vf_filter,
            "-c:a", "copy",
            output_video
        ]

        subprocess.run(command)