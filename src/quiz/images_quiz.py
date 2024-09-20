import os
from quiz import image_generator

def generate_question_image(
    question_title,
    question_number,
    layout_template_path,
    output_dir='../temp/img/question'
):
    """Generate images that display the question text progressively to create an effect."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Split the question into words
    words = question_title.split()

    # Generate images with progressively revealed text
    for i in range(1, len(words) + 1):
        # Join the words up to the current index
        partial_question = ' '.join(words[:i])

        output_image_path = os.path.join(output_dir, f"{i}.png")

        # Create parameters dictionary
        params = {
            'question_title': partial_question,
            'answers': [],  # No answers displayed
            'question_number': question_number,
            'output_image_path': output_image_path,
            'layout_template_path': layout_template_path,
        }

        # Call generate_quiz_image with parameters
        image_generator.generate_quiz_image(params)
        print(f"Generated question image with effect: {output_image_path}")

def generate_options_images(
    question_title,
    answers,
    question_number,
    layout_template_path,
    output_dir='../temp/img/options'
):
    """Generate images where answers are progressively revealed."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop to generate images for progressively revealed answers
    for step in range(1, len(answers) + 1):
        # Generate the subset of answers to display
        answers_subset = answers[:step]

        output_image_path = os.path.join(output_dir, f"{step}.png")

        # Create parameters dictionary
        params = {
            'question_title': question_title,
            'answers': answers_subset,
            'question_number': question_number,
            'output_image_path': output_image_path,
            'layout_template_path': layout_template_path,
        }

        # Call `generate_quiz_image` with parameters
        image_generator.generate_quiz_image(params)
        print(f"Generated image for step {step}: {output_image_path}")

def generate_timer_image(
    question_title,
    answers,
    question_number,
    layout_template_path,
    output_dir='../temp/img/timer'
):
    """Generate images with the progress bar increasing from 0% to 100% in steps of 10%."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Loop over progress percentages from 0 to 100 in steps of 10
    for progress_percentage in range(0, 101, 10):
        # Generate the output image path for each progress percentage
        output_image_path = os.path.join(output_dir, f'progress_{progress_percentage}.png')

        # Create parameters dictionary
        params = {
            'question_title': question_title,
            'answers': answers,
            'question_number': question_number,
            'output_image_path': output_image_path,
            'layout_template_path': layout_template_path,
            'progress_percentage': progress_percentage
        }

        # Call `generate_quiz_image` with parameters
        image_generator.generate_quiz_image(params)
        print(f"Generated timer image with progress {progress_percentage}%: {output_image_path}")

def generate_correct_answer_image(
    question_title,
    answers,
    question_number,
    correct_answer_index,
    layout_template_path,
    output_dir='../temp/img/correct'
):
    """Generate the final image with all answers displayed and the correct one highlighted."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    final_output_image_path = os.path.join(output_dir, "1.png")

    # Set progress percentage to 100% for the final image
    progress_percentage = 100

    # Create parameters dictionary
    params = {
        'question_title': question_title,
        'answers': answers,
        'question_number': question_number,
        'output_image_path': final_output_image_path,
        'correct_answer_index': correct_answer_index,
        'layout_template_path': layout_template_path,
        'progress_percentage': progress_percentage
    }

    # Call `generate_quiz_image` with parameters
    image_generator.generate_quiz_image(params)
    print(f"Generated final image with correct answer: {final_output_image_path}")

def generate_all_images(
    question_title,
    answers,
    question_number,
    correct_answer_index,
    output_dir,
    layout_template_path
):
    """Generate all images for the quiz question."""
    # Generate images where the question text is progressively revealed
    generate_question_image(
        question_title,
        question_number,
        output_dir=os.path.join(output_dir,"question/img"),
        layout_template_path=layout_template_path
    )

    # Generate images where answers are progressively revealed
    generate_options_images(
        question_title,
        answers,
        question_number,
        output_dir=os.path.join(output_dir,"options/img"),
        layout_template_path=layout_template_path
    )

    # Generate images with the progress bar increasing from 0% to 100%
    generate_timer_image(
        question_title,
        answers,
        question_number,
        output_dir=os.path.join(output_dir,"timer/img"),
        layout_template_path=layout_template_path
    )

    # Generate the final image with the correct answer highlighted
    generate_correct_answer_image(
        question_title,
        answers,
        question_number,
        correct_answer_index,
        output_dir=os.path.join(output_dir,"correct/img"),
        layout_template_path=layout_template_path,
    )