from moviepy.editor import *
import os
import re

def numerical_sort(value):
    """ Helper function to sort filenames numerically """
    numbers = re.findall(r'\d+', value)
    return int(numbers[0]) if numbers else 0

import os
import re

def numerical_sort(value):
    """ Helper function to sort filenames numerically """
    # Extract numbers from the filename using a regular expression
    numbers = re.findall(r'\d+', os.path.basename(value))
    # Convert the first found number to an integer for sorting
    return int(numbers[0]) if numbers else 0

def create_question_video(temp_dir, output_video_path, image_duration=0.25):
    """
    Create a video with images and audio for a question, with the audio playing only once.
    The video continues without sound after the audio finishes.
    """
    
    question_audio_path = os.path.join(temp_dir, "question/mp3/1.mp3")
    question_images_dir = os.path.join(temp_dir, "question/img")
    
    # Load all images from the question's directory in sequence.
    question_images = sorted(
        [os.path.join(question_images_dir, img) for img in os.listdir(question_images_dir) if img.endswith(".png")],
        key=numerical_sort
    )

    print("Question images:")
    print(question_images)

    # Load the audio file for the question.
    question_audio = AudioFileClip(question_audio_path)

    # Create a list of ImageClips with the duration for each image.
    image_clips = [ImageClip(img).set_duration(image_duration) for img in question_images]

    # Concatenate all the image clips into a video sequence.
    video_clip = concatenate_videoclips(image_clips, method="compose")

    # Set the audio to play only once and keep the video running after the audio finishes.
    video_clip_with_audio = video_clip.set_audio(question_audio)

    # Adjust the duration of the audio so it is not repeated.
    video_clip_with_audio.audio = video_clip_with_audio.audio.set_duration(question_audio.duration)

    # Export the final video, with the audio playing only once and the video continuing after the audio ends.
    video_clip_with_audio.write_videofile(output_video_path, fps=24)
    
def create_options_video(temp_dir, output_video_path, image_duration=1.5):
    """
    Create a video with the answer options and corresponding audio.
    """
    
    options_images_dir = os.path.join(temp_dir, "options/img")
    options_audio_dir = os.path.join(temp_dir, "options/mp3")
    
    option_images = sorted([os.path.join(options_images_dir, img) for img in os.listdir(options_images_dir) if img.endswith(".png")])
    option_audios = sorted([os.path.join(options_audio_dir, audio) for audio in os.listdir(options_audio_dir) if audio.endswith(".mp3")])

    if len(option_images) != len(option_audios):
        raise ValueError("The number of images and audios does not match!")

    option_clips = [ImageClip(img).set_duration(image_duration).set_audio(AudioFileClip(audio)) for img, audio in zip(option_images, option_audios)]
    video_clip = concatenate_videoclips(option_clips, method="compose")
    video_clip.write_videofile(output_video_path, fps=24)
    
def natural_sort_key(s):
    """ Function to naturally sort strings with numbers. """
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def create_timer_video(temp_dir, audio_path, output_video_path, image_duration=0.5, audio_speed=2.0):
    """
    Create a timer video based on the timer progress images, sorted correctly, and add an audio loop.
    Allows adjusting the audio speed.
    """
    
    timer_images_dir = os.path.join(temp_dir, "timer/img")
    
    # Load and naturally sort the timer progress images.
    timer_images = sorted([os.path.join(timer_images_dir, img) for img in os.listdir(timer_images_dir) if img.endswith(".png")], key=natural_sort_key)

    # Log to check the order of the loaded images.
    print("Images loaded in the following order:")
    for img in timer_images:
        print(img)

    # Create a list of ImageClips with the duration for each image.
    timer_clips = [ImageClip(img).set_duration(image_duration) for img in timer_images]

    # Concatenate all the clips into a sequence.
    video_clip = concatenate_videoclips(timer_clips, method="compose")

    # Load the audio.
    audio_clip = AudioFileClip(audio_path)

    # Adjust the audio speed if necessary.
    if audio_speed != 1.0:
        audio_clip = audio_clip.fx(vfx.speedx, audio_speed)

    # Loop the audio until the end of the video.
    audio_clip_loop = afx.audio_loop(audio_clip, duration=video_clip.duration)

    # Associate the looped audio with the video.
    video_clip = video_clip.set_audio(audio_clip_loop)

    # Export the final video.
    video_clip.write_videofile(output_video_path, fps=24)

def create_correct_answer_video(temp_dir, output_video_path, image_duration=5):
    """
    Create a video with the correct answer image and audio.
    """
    correct_image_path = os.path.join(temp_dir, "correct/img/1.png")
    correct_audio_path = os.path.join(temp_dir, "correct/mp3/1.mp3")
    correct_image = ImageClip(correct_image_path).set_duration(image_duration)
    correct_audio = AudioFileClip(correct_audio_path)
    correct_clip = correct_image.set_audio(correct_audio)
    correct_clip.write_videofile(output_video_path, fps=24)

def create_all_videos(temp_dir, assets_dir, output_dir):
    """
    Generate all the videos: question, options, timer, and correct answer.
    """
    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)

    # Generate the question video.
    question_video_path = os.path.join(output_dir, "question_video.mp4")
    create_question_video(temp_dir=temp_dir, output_video_path=question_video_path)
    print(f"Question video created: {question_video_path}")

    # Generate the options video.
    options_video_path = os.path.join(output_dir, "options_video.mp4")
    create_options_video(temp_dir, options_video_path)
    print(f"Options video created: {options_video_path}")

    # Generate the timer video.
    timer_video_path = os.path.join(output_dir, "timer_video.mp4")
    audio_path = os.path.join(assets_dir, "mp3/clock.wav")  # Add the correct audio path here.
    create_timer_video(temp_dir, audio_path, timer_video_path)
    print(f"Timer video created: {timer_video_path}")

    # Generate the correct answer video.
    correct_answer_video_path = os.path.join(output_dir, "correct_answer_video.mp4")
    create_correct_answer_video(temp_dir, correct_answer_video_path)
    print(f"Correct answer video created: {correct_answer_video_path}")
