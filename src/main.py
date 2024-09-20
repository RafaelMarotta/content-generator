from quiz import full_video_quiz
# Example usage
questions_data = [
    {
        "title": "QUAL É O PLANETA MAIS PRÓXIMO DO SOL?",
        "title_speech": """<speak>Qual é o planeta mais próximo do sol?</speak>""",
        "answers": ["Mercúrio", "Vênus", "Marte", "Júpiter"],
        "answers_speech": [
            """<speak>Mercúrio</speak>""",
            """<speak>Vênus</speak>""",
            """<speak>Marte</speak>""",
            """<speak>Júpiter</speak>"""
        ],
        "correct_answer_index": 0,
        "correct_answer_speech": """<speak>E a resposta correta é: <break time="0.5s"/> Mercúrio! Muito bem se você acertou.</speak>""",
        "question_number": 1
    },
    {
        "title": "QUAL A CAPITAL DO BRASIL?",
        "title_speech": """<speak>Qual a capital do Brasil?</speak>""",
        "answers": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
        "answers_speech": [
            """<speak>São Paulo</speak>""",
            """<speak>Rio de Janeiro</speak>""",
            """<speak>Brasília</speak>""",
            """<speak>Salvador</speak>"""
        ],
        "correct_answer_index": 2,
        "correct_answer_speech": """<speak>A resposta certa é: <break time="0.5s"/> Brasília!</speak>""",
        "question_number": 2
    },
    {
        "title": "QUEM PINTOU A MONA LISA?",
        "title_speech": """<speak>Quem pintou a Mona Lisa?</speak>""",
        "answers": ["Leonardo da Vinci", "Michelangelo", "Vincent van Gogh", "Pablo Picasso"],
        "answers_speech": [
            """<speak>Leonardo da Vinci</speak>""",
            """<speak>Michelangelo</speak>""",
            """<speak>Vincent van Gogh</speak>""",
            """<speak>Pablo Picasso</speak>"""
        ],
        "correct_answer_index": 0,
        "correct_answer_speech": """<speak>A resposta correta é: <break time="0.5s"/> Leonardo da Vinci!</speak>""",
        "question_number": 3
    }
]

full_video_quiz.generate_video(questions_data)