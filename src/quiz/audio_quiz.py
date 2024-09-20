import os
from commons.audio_processor import generate_tts

def ensure_directory_exists(path):
    """
    Checks if a directory exists at the specified path. If not, it creates the directory.
    
    :param path: The path to the directory to check or create.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def generate_audio_question(question_title, audio_output_dir):
    """
    Generates audio for the given question title and saves it in the specified output directory.
    
    :param question_title: The title of the question to convert into speech.
    :param audio_output_dir: The directory where the audio files will be stored.
    """
    question_audio_dir = os.path.join(audio_output_dir, "question/mp3")
    ensure_directory_exists(question_audio_dir)  # Ensure the question audio directory exists
    question_audio_path = os.path.join(question_audio_dir, "1.mp3")
    
    # Generate Text-to-Speech (TTS) audio for the question
    generate_tts(
        text=question_title,
        file_name=question_audio_path,
        speaking_rate=1.2
    )

def generate_audio_answers(answers, audio_output_dir):
    """
    Generates audio for the list of answer options and saves them in the specified directory.
    
    :param answers: List of answer options to convert into speech.
    :param audio_output_dir: The directory where the audio files will be stored.
    """
    options_audio_dir = os.path.join(audio_output_dir, "options/mp3")
    ensure_directory_exists(options_audio_dir)  # Ensure the options audio directory exists
    
    for idx, answer in enumerate(answers, start=1):
        answer_audio_path = os.path.join(options_audio_dir, f"{idx}.mp3")
        
        # Generate TTS audio for each answer option
        generate_tts(
            text=answer,
            file_name=answer_audio_path,
            speaking_rate=1.4
        )
        print(f"Generated audio for answer {idx}: {answer_audio_path}")
        
def generate_audio_correct_answer(correct_answer, audio_output_dir):
    """
    Generates audio for the correct answer and saves it in the specified output directory.
    
    :param correct_answer: The correct answer to convert into speech.
    :param audio_output_dir: The directory where the audio files will be stored.
    """
    correct_audio_dir = os.path.join(audio_output_dir, "correct/mp3")
    ensure_directory_exists(correct_audio_dir)  # Ensure the correct answer audio directory exists
    answer_audio_path = os.path.join(correct_audio_dir, "1.mp3")
    
    print(correct_answer)  # Log the correct answer for debugging
    
    # Generate TTS audio for the correct answer
    generate_tts(
        text=correct_answer,
        file_name=answer_audio_path,
        speaking_rate=1.4
    )
    
def generate_all_audios(question_title, answers, correct_answer, audio_output_dir):
    """
    Generates all necessary audio files: question, answers, and the correct answer.
    
    :param question_title: The title of the question to convert into speech.
    :param answers: List of answer options to convert into speech.
    :param correct_answer: The correct answer to convert into speech.
    :param audio_output_dir: The directory where all audio files will be stored.
    """
    # Generate audio for the question
    generate_audio_question(question_title=question_title, audio_output_dir=audio_output_dir)
    
    # Generate audio for the answer options
    generate_audio_answers(answers=answers, audio_output_dir=audio_output_dir)
    
    # Generate audio for the correct answer
    generate_audio_correct_answer(correct_answer=correct_answer, audio_output_dir=audio_output_dir)
