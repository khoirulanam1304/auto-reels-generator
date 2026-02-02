import re

def write_wrapped_text_to_file(text, output_file):
    """
    Membungkus teks menjadi beberapa baris
    berdasarkan tanda baca.
    """
    # pisah berdasarkan !?.
    sentences = re.split(r'(?<=[?.!])\s+', text)

    final_lines = []
    for s in sentences:
        if len(s) > 35:
            final_lines.extend(split_long_sentence(s, 35))
        else:
            final_lines.append(s)
            
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(final_lines))

def split_long_sentence(sentence, max_len):
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
