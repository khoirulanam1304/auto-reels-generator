from video_cutter import VideoCutter
from question_bank import QuestionBank
from content_generator import ContentGenerator

TARGET_WIDTH = 720
TARGET_HEIGHT = 1280

vc = VideoCutter("input/vlog.mp4", "output", target_width=TARGET_WIDTH, target_height=TARGET_HEIGHT)
qb = QuestionBank("questions.txt")
cg = ContentGenerator()

clip = vc.cut_random_clip(duration=12, output_name="raw_clip.mp4")

question = qb.get_random_unused_question()
print("Soal:", question)

final_video = "output/final_video.mp4"
cg.add_text_overlay(
    clip,
    question,
    final_video,
    font_path=None,
    target_width=TARGET_WIDTH,
    target_height=TARGET_HEIGHT,
)

print("Video final jadi:", final_video)
