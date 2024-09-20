import os
import shutil
from quiz import images_quiz
from quiz import audio_quiz
from quiz import video_quiz
from commons import join_videos
from commons import background_audio

def generate_video_for_single_question(question_data):
    title = question_data['title']
    title_speech = question_data['title_speech']
    answers = question_data['answers']
    answers_speech = question_data['answers_speech']
    correct_answer_idx = question_data['correct_answer_index']
    correct_answer_speech = question_data['correct_answer_speech']
    question_number = question_data['question_number']
    
    temp_dir = os.path.join("..", "temp", str(question_number), "")
    
    # Ensure the output directory exists
    os.makedirs(temp_dir, exist_ok=True)

    # Generate all images (question, options, etc.)
    images_quiz.generate_all_images(
        question_title=title,
        answers=answers,
        question_number=question_number,
        correct_answer_index=correct_answer_idx,
        output_dir=temp_dir,
        layout_template_path="../assets/template/layout_template.html"
    )
    
    # Generate all audios (question, answers)
    audio_quiz.generate_all_audios(question_title=title_speech, answers=answers_speech, correct_answer=correct_answer_speech, audio_output_dir=temp_dir)

    output_dir = os.path.join(temp_dir, "output")

    # Create all individual videos (question, options, timer, correct answer)
    video_quiz.create_all_videos(temp_dir=temp_dir, output_dir=output_dir)

    # Join all generated videos in order
    video_paths = [
        os.path.join(output_dir, "question_video.mp4"),
        os.path.join(output_dir, "options_video.mp4"),
        os.path.join(output_dir, "timer_video.mp4"),
        os.path.join(output_dir, "correct_answer_video.mp4")
    ]
    output_video_path = os.path.join(output_dir, f"final_quiz_video_{question_number}.mp4")

    # Join all videos into the final video for the specific question
    join_videos.join_all_videos_melt(video_paths, output_video_path)
    
    print(f"Final quiz video for question {question_number} created at: {output_video_path}")
    return output_video_path

def generate_videos_for_questions_synchronously(questions_data):
    video_paths = []
    
    # Generate each video sequentially
    for question_data in questions_data:
        video_path = generate_video_for_single_question(question_data)
        video_paths.append(video_path)
    
    print("All individual videos have been generated.")
    return video_paths

def join_all_generated_videos(video_paths, final_output_path):
    # Ensure the final output directory exists
    final_output_dir = os.path.dirname(final_output_path)
    os.makedirs(final_output_dir, exist_ok=True)
    
    # Join all videos into one final video
    join_videos.join_all_videos_melt(video_paths, final_output_path)
    print(f"Final quiz video created at: {final_output_path}")

def generate_video(questions_data):
    # Step 1: Clean up the temp folder
    temp_folder = "../../temp"
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder, exist_ok=True)

    # Step 2: Generate all videos sequentially
    generated_video_paths = generate_videos_for_questions_synchronously(questions_data)

    # Step 3: Join all generated videos into a single final video
    final_output_video_path = os.path.join("..", "output", "final_quiz_video.mp4")
    join_all_generated_videos(generated_video_paths, final_output_video_path)

    # Step 4: Add background music
    background_audio.add_background_music(video_path=final_output_video_path, 
                         music_path="../assets/mp3/background-sound.mp3", 
                         output_path="../output/final_with_background.mp4")