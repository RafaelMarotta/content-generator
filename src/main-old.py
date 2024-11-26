from quiz import full_video_quiz

# Example questions
questions = [
    {
        "title": "EM QUAL ANO FOI REALIZADA A PRIMEIRA COPA DO MUNDO DE FUTEBOL?",
        "title_speech": "<speak>Em qual ano foi realizada a primeira Copa do Mundo de futebol?</speak>",
        "answers": ["1928", "1930", "1934", "1938"],
        "answers_speech": [
            "<speak>1928</speak>",
            "<speak>1930</speak>",
            "<speak>1934</speak>",
            "<speak>1938</speak>"
        ],
        "correct_answer_index": 1,
        "correct_answer_speech": "<speak>Correto! A primeira Copa do Mundo foi em 1930!</speak>",
        "question_number": 1
    },
    {
        "title": "QUAL PAÍS É O MAIOR CAMPEÃO DA COPA DO MUNDO?",
        "title_speech": "<speak>Qual país é o maior campeão da Copa do Mundo?</speak>",
        "answers": ["Brasil", "Alemanha", "Itália", "Argentina"],
        "answers_speech": [
            "<speak>Brasil</speak>",
            "<speak>Alemanha</speak>",
            "<speak>Itália</speak>",
            "<speak>Argentina</speak>"
        ],
        "correct_answer_index": 0,
        "correct_answer_speech": "<speak>Correto! O Brasil é o maior campeão da Copa do Mundo!</speak>",
        "question_number": 2
    }
    # Add more questions as needed
]

# Execute the video generation
full_video_quiz.generate_video({
    "title": "quiz-futebol",
    "template": "layout_template.html",
    "questions": questions
})

print("Video generation completed successfully.")
