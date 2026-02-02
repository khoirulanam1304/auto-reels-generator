import subprocess
import os
from text_utils import write_wrapped_text_to_file

class ContentGenerator:
    def add_text_overlay(self, input_video, text, output_video):
        temp_text_file = "temp_text.txt"

        line_count = write_wrapped_text_to_file(text, temp_text_file)

        #hitung box
        font_size = 64
        line_spacing = 16
        padding = 250

        box_height = (line_count * (font_size + line_spacing)) + padding

        #posisi box ditengah layar
        box_y = int((1920 - box_height) / 2)

        vf_filter = (
            f"drawbox="
            f"x=54:"
            f"y={box_y}:"
            f"w=972:"
            f"h={box_height}:"
            f"color=white:"
            f"t=fill"
            ","
            "drawtext="
            "font=segoeui:"
            f"textfile='{temp_text_file}':"
            "fontcolor=black:"
            f"fontsize={font_size}:"
            f"line_spacing={line_spacing}:"
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

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)