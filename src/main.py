from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import time
import uuid
import os
import threading
import shutil  # Import para remoção de diretórios
from quiz import full_video_quiz
import collections.abc  # Corrige o erro do AttributeError

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://13.58.206.126:3000",
    "https://video-generator-front.vercel.app"
]}})

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        # Recebe o JSON de questões da requisição
        data = request.get_json()
        questions = data.get("questions", [])
        
        if not questions:
            return jsonify({"error": "Nenhuma questão fornecida"}), 400
        
        # Início da medição do tempo
        start_time = time.time()

        random_uuid = str(uuid.uuid4())

        # Caminho completo para o vídeo gerado
        video_path = os.path.join(os.getenv("APP_PATH", "."), "output", f"{random_uuid}.mp4")

        # Executar a função de geração de vídeo
        full_video_quiz.generate_video({
            "title": random_uuid,
            "template": "layout_template.html",
            "questions": questions,
            "output": video_path
        })

        # Fim da medição do tempo e cálculo do tempo de execução
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

        # Verificar se o arquivo foi realmente criado
        if not os.path.exists(video_path):
            return jsonify({"error": "Erro ao gerar o vídeo."}), 500

        # Após enviar o arquivo, removê-lo do sistema
        @after_this_request
        def cleanup(response):
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                    os.remove(os.path.join(os.getenv("APP_PATH", "."), "output", f"{random_uuid}-copy.mp4"))
                    shutil.rmtree(os.path.join(os.getenv("APP_PATH", "."), "temp", random_uuid))
                    print(f"Arquivo {video_path} removido com sucesso.")
            except Exception as e:
                print(f"Erro ao remover o arquivo {video_path}: {e}")
            return response

        # Retornar o vídeo gerado como resposta
        return send_file(video_path, as_attachment=True, mimetype='video/mp4', attachment_filename='quiz_video.mp4')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
