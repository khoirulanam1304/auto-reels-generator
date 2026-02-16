import subprocess
import os
from text_utils import write_wrapped_text_to_file, estimate_line_height

class ContentGenerator:
    def add_text_overlay(self, input_video, text, output_video, font_path=None):
        temp_text_file = "temp_text.txt"

        font_size = 64
        line_spacing = 16
        padding = 500
        box_width = 972
        box_inner_padding = 80
        max_text_width = box_width - (2 * box_inner_padding)

        line_count = write_wrapped_text_to_file(
            text,
            temp_text_file,
            max_width=max_text_width,
            font_size=font_size,
            font_path=font_path,
        )

        #hitung box
        line_height = estimate_line_height(font_size, font_path, line_spacing)
        box_height = (line_count * line_height) + padding

        #posisi box ditengah layar
        box_y = int((1920 - box_height) / 2)

        font_filter = f"fontfile='{font_path}':" if font_path else "font=segoeui:"

        vf_filter = (
            f"drawbox="
            f"x=54:"
            f"y={box_y}:"
            f"w={box_width}:"
            f"h={box_height}:"
            f"color=white:"
            f"t=fill"
            ","
            "drawtext="
            f"{font_filter}"
            f"textfile='{temp_text_file}':"
            "fontcolor=black:"
            f"fontsize={font_size}:"
            f"line_spacing={line_spacing}:"
            "x=(w-text_w)/2:"
            f"y={box_y}+({box_height}-text_h)/2"
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