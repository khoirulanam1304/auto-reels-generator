import subprocess
import os
from text_utils import write_wrapped_text_to_file, estimate_line_height

class ContentGenerator:
    def add_text_overlay(
        self,
        input_video,
        text,
        output_video,
        font_path=None,
        target_width=720,
        target_height=1280,
    ):
        temp_text_file = "temp_text.txt"
        resolved_font_path = font_path or self._get_default_bold_font_path()

        font_size = max(36, int(target_width * 0.06))
        line_spacing = max(10, int(font_size * 0.25))
        padding = int(target_height * 0.18)
        box_width = int(target_width * 0.9)
        box_inner_padding = int(target_width * 0.07)
        max_text_width = box_width - (2 * box_inner_padding)

        line_count = write_wrapped_text_to_file(
            text,
            temp_text_file,
            max_width=max_text_width,
            font_size=font_size,
            font_path=resolved_font_path,
        )

        #hitung box
        line_height = estimate_line_height(font_size, resolved_font_path, line_spacing)
        box_height = (line_count * line_height) + padding

        #posisi box ditengah layar
        box_y = int((target_height - box_height) / 2)
        box_x = int((target_width - box_width) / 2)

        lines = self._read_wrapped_lines(temp_text_file)
        text_block_height = line_count * line_height
        text_start_y = int(box_y + (box_height - text_block_height) / 2)

        filters = [
            (
                f"drawbox="
                f"x={box_x}:"
                f"y={box_y}:"
                f"w={box_width}:"
                f"h={box_height}:"
                f"color=white:"
                f"t=fill"
            )
        ]

        font_filter = "font=Arial Bold"
        if resolved_font_path:
            font_filter = f"fontfile='{self._escape_ffmpeg_path(resolved_font_path)}'"

        for idx, line in enumerate(lines):
            escaped_line = self._escape_drawtext_text(line)
            line_y = text_start_y + (idx * line_height)
            filters.append(
                "drawtext="
                f"{font_filter}:"
                f"text='{escaped_line}':"
                "fontcolor=black:"
                f"fontsize={font_size}:"
                "x=(w-text_w)/2:"
                f"y={line_y}"
            )

        vf_filter = ",".join(filters)
        
        command = [
            "ffmpeg",
            "-y",
            "-i", input_video,
            "-vf", vf_filter,
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            output_video
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _get_default_bold_font_path(self):
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def _read_wrapped_lines(self, path):
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def _escape_drawtext_text(self, text):
        clean = "".join(ch for ch in text if ch.isprintable())
        clean = clean.replace("□", "").replace("�", "")
        return (
            clean.replace("\\", r"\\")
            .replace(":", r"\:")
            .replace("'", r"\'")
            .replace("%", r"\%")
        )

    def _escape_ffmpeg_path(self, path):
        return path.replace("\\", "/").replace(":", r"\:")
