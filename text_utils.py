import re

try:
    from PIL import ImageFont
except ImportError:  # pragma: no cover - fallback when Pillow isn't available
    ImageFont = None


def write_wrapped_text_to_file(
    text,
    output_file,
    max_width,
    font_size=64,
    font_path=None,
    max_chars_fallback=35,
):
    """
    Membungkus teks menjadi beberapa baris agar tidak melebihi lebar box.
    Jika Pillow tersedia, ukur lebar pixel untuk pemotongan yang lebih presisi.
    """
    sentences = re.split(r'(?<=[?.!])\s+', text)
    font = _load_font(font_size, font_path)
    max_chars_fallback = _estimate_max_chars(max_width, font_size, max_chars_fallback)

    final_lines = []
    for sentence in sentences:
        if not sentence:
            continue
        if font is None:
            final_lines.extend(_split_long_sentence_by_chars(sentence, max_chars_fallback))
            continue
        final_lines.extend(_wrap_sentence_by_width(sentence, max_width, font))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(final_lines))

    return len(final_lines)


def _load_font(font_size, font_path):
    if ImageFont is None:
        return None
    if not font_path:
        return None
    try:
        return ImageFont.truetype(font_path, font_size)
    except OSError:
        return None


def estimate_line_height(font_size, font_path, line_spacing):
    font = _load_font(font_size, font_path)
    if font is None:
        return font_size + line_spacing
    try:
        ascent, descent = font.getmetrics()
        return ascent + descent + line_spacing
    except AttributeError:
        return font_size + line_spacing


def _estimate_max_chars(max_width, font_size, fallback):
    if not max_width or not font_size:
        return fallback
    estimated = int(max_width / (font_size * 0.6))
    if estimated <= 0:
        return fallback
    return estimated


def _measure_text_width(text, font):
    if hasattr(font, "getlength"):
        return font.getlength(text)
    return font.getsize(text)[0]


def _wrap_sentence_by_width(sentence, max_width, font):
    words = sentence.split()
    lines = []
    current = ""

    for word in words:
        candidate = f"{current} {word}" if current else word
        if _measure_text_width(candidate, font) <= max_width:
            current = candidate
            continue

        if current:
            lines.append(current)
            current = ""

        if _measure_text_width(word, font) <= max_width:
            current = word
            continue

        lines.extend(_split_long_word_by_width(word, max_width, font))

    if current:
        lines.append(current)

    return lines


def _split_long_word_by_width(word, max_width, font):
    chunks = []
    current = ""
    for char in word:
        candidate = f"{current}{char}"
        if _measure_text_width(candidate, font) <= max_width:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = char
    if current:
        chunks.append(current)
    return chunks


def _split_long_sentence_by_chars(sentence, max_len):
    words = sentence.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) <= max_len:
            current += " " + word if current else word
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines