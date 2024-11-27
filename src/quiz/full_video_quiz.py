import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from quiz import images_quiz
from quiz import audio_quiz
from quiz import video_quiz
from commons import join_videos
from commons import background_audio
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("APP_PATH")
temp_dir = os.path.join(base_path, "temp")
assets_dir = os.path.join(base_path, "assets")
output_dir = os.path.join(base_path, "output")


def generate_video_for_single_question(question_data, template, video_title):
    title = question_data['title']
    title_speech = question_data['title_speech']
    answers = question_data['answers']
    answers_speech = question_data['answers_speech']
    correct_answer_idx = question_data['correct_answer_index']
    correct_answer_speech = question_data['correct_answer_speech']
    question_number = question_data['question_number']
    
    temp_question_dir = os.path.join(temp_dir, str(video_title), str(question_number), "")
    
    # Ensure the output directory exists
    os.makedirs(temp_question_dir, exist_ok=True)

    # Generate all images (question, options, etc.)
    images_quiz.generate_all_images(
        question_title=title,
        answers=answers,
        question_number=question_number,
        correct_answer_index=correct_answer_idx,
        output_dir=temp_question_dir,
        layout_template_path=os.path.join(assets_dir, "template", template)
    )
    
    # Generate all audios (question, answers)
    audio_quiz.generate_all_audios(question_title=title_speech, answers=answers_speech, correct_answer=correct_answer_speech, audio_output_dir=temp_question_dir)

    output_dir = os.path.join(temp_question_dir, "output")

    # Create all individual videos (question, options, timer, correct answer)
    video_quiz.create_all_videos(temp_dir=temp_question_dir, assets_dir=assets_dir, output_dir=output_dir)

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


def generate_videos_for_questions_in_parallel(data, max_threads=2):
    video_paths = []

    # Use ThreadPoolExecutor with a max thread limit
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit each video generation task to the executor
        future_to_question = {
            executor.submit(generate_video_for_single_question, question, data['template'], data['title']): question
            for question in data['questions']
        }
        
        for future in future_to_question:
            try:
                video_path = future.result()  # Wait for the task to complete and get the result
                video_paths.append(video_path)
            except Exception as exc:
                question_data = future_to_question[future]
                print(f"Question {question_data['question_number']} generated an exception: {exc}")
    
    print("All individual videos have been generated.")
    return video_paths


def join_all_generated_videos(video_paths, final_output_path):
    # Ensure the final output directory exists
    final_output_dir = os.path.dirname(final_output_path)
    os.makedirs(final_output_dir, exist_ok=True)
    
    # Join all videos into one final video
    join_videos.join_all_videos_melt(video_paths, final_output_path)
    print(f"Final quiz video created at: {final_output_path}")


def generate_video(data):
    # # Step 1: Clean up the temp folder
    # if os.path.exists(temp_dir):
    #     shutil.rmtree(temp_dir)
    # os.makedirs(temp_dir, exist_ok=True)

    # Step 2: Generate all videos in parallel
    generated_video_paths = generate_videos_for_questions_in_parallel(data)

    title = data["title"]

    # Step 3: Join all generated videos into a single final video
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

    final_output_video_path = os.path.join(output_dir, f"{safe_title}.mp4")
    join_all_generated_videos(generated_video_paths, final_output_video_path)
    join_all_generated_videos(generated_video_paths, os.path.join(output_dir, f"{safe_title}-copy.mp4"))

    music_path = os.path.join(assets_dir, "mp3/background-sound.mp3")
    # Step 4: Add background music
    background_audio.add_background_music(video_path=os.path.join(output_dir, f"{safe_title}-copy.mp4"), 
                         music_path=music_path,
                         output_path=final_output_video_path)
