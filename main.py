from video_cutter import VideoCutter
from question_bank import QuestionBank
from content_generator import ContentGenerator

vc = VideoCutter("input/vlog.mp4", "output")
qb = QuestionBank("questions.txt")
cg = ContentGenerator()

clip = vc.cut_random_clip(duration=12, output_name="raw_clip.mp4")

question = qb.get_random_question()
print("Soal:", question)

final_video = "output/final_video.mp4"
cg.add_text_overlay(clip, question, final_video)

print("Video final jadi:", final_video)