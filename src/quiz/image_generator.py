import imgkit
import os
from commons.template_processor import generate_html_from_template  # Importing the HTML generation function

def generate_quiz_image(parameters):
    """
    Generates a quiz image based on the parameters provided.

    Parameters:
        parameters (dict): A dictionary containing all necessary parameters.
    """
    # Extract parameters from the dictionary
    question_title = parameters.get('question_title', '')
    answers = parameters.get('answers', [])
    question_number = parameters.get('question_number', '')
    output_image_path = parameters.get('output_image_path', '../temp/img/quiz_image.png')
    correct_answer_index = parameters.get('correct_answer_index', None)
    layout_template_path = parameters.get('layout_template_path', "../../assets/template/layout_template.html")
    progress_percentage = parameters.get('progress_percentage')

    # Generate dynamic answers HTML
    answers_html = ''
    option_letters = ['A', 'B', 'C', 'D', 'E']  # Extend this list if necessary

    for i, answer in enumerate(answers):
        letter = option_letters[i]
        # Check if this is the correct answer and apply the appropriate CSS class
        if correct_answer_index is not None and i == correct_answer_index:
            option_class = 'option-correct'
        else:
            option_class = 'option'
        answers_html += f'''
        <div class="{option_class}">
            <div class="option-letter">{letter}</div>
            <div class="option-text">{answer}</div>
        </div>
        '''

    # Prepare parameters for template placeholders
    template_parameters = {
        'question_title': question_title,
        'question_number': str(question_number),
        'answers_html': answers_html,
        'progress_percentage': progress_percentage
    }

    # Ensure the output directory exists
    output_html_path = "../../temp/html/quiz_template_final.html"
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    # Generate HTML using the generate_html_from_template function
    generate_html_from_template(
        root_template_path=layout_template_path,
        parameters=template_parameters,
        output_path=output_html_path
    )

    print(f"Generated HTML at: {output_html_path}")

    # Open and print the content of the HTML file for debugging
    with open(output_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        print("Generated HTML Content:")
        print(html_content)

    # Options for imgkit to handle CSS and set image size
    options = {
        'format': 'png',
        'width': 1920,
        'height': 1080,
        'encoding': "UTF-8",
        'enable-local-file-access': '',
    }

    # Generate image from the final HTML and save it
    # Generate image and capture output
    try:
        imgkit.from_file(output_html_path, output_image_path, options=options)
    except OSError as e:
        print("An error occurred during image generation:")
        print(e)
        raise
