import time
import psutil
import subprocess
import threading
import csv
from quiz import full_video_quiz

# Flag para controle de monitoramento
monitoring = False

# Função para monitorar o uso do sistema continuamente e registrar em um arquivo CSV
def monitor_system_usage(csv_file, interval=5):
    global monitoring
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Escreve o cabeçalho no CSV
        writer.writerow(["CPU User Time (s)", "CPU System Time (s)", "Memory Used (MiB)", "Memory Total (MiB)",
                         "GPU Usage (%)", "GPU Memory Used (MiB)", "GPU Memory Total (MiB)"])

        while monitoring:
            # Uso da CPU em tempo total (segundos)
            cpu_times = psutil.cpu_times()
            cpu_user_time = cpu_times.user  # Tempo em modo usuário
            cpu_system_time = cpu_times.system  # Tempo em modo sistema

            # Uso da Memória em valores absolutos (em bytes)
            memory = psutil.virtual_memory()
            memory_used = memory.used  # Memória usada em bytes
            memory_total = memory.total  # Memória total em bytes

            # Uso da GPU (se disponível, NVIDIA)
            try:
                gpu_usage = subprocess.check_output(
                    ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total', '--format=csv,nounits,noheader'],
                    encoding='utf-8'
                ).strip().split('\n')[0].split(', ')
                gpu_usage_percent = gpu_usage[0]
                gpu_memory_used = gpu_usage[1]
                gpu_memory_total = gpu_usage[2]
            except FileNotFoundError:
                # Se a GPU não estiver disponível, marca como N/A
                gpu_usage_percent = "N/A"
                gpu_memory_used = "N/A"
                gpu_memory_total = "N/A"
            
            # Converte os dados para MiB
            memory_used_mib = memory_used / (1024 * 1024)
            memory_total_mib = memory_total / (1024 * 1024)

            # Registrar dados absolutos de CPU, Memória e GPU no CSV
            writer.writerow([cpu_user_time, cpu_system_time, memory_used_mib, memory_total_mib,
                             gpu_usage_percent, gpu_memory_used, gpu_memory_total])

            # Intervalo de monitoramento
            time.sleep(interval)

# Exemplo de perguntas
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
  },
  {
    "title": "QUAL JOGADOR DETÉM O RECORDE DE MAIS GOLS NA COPA DO MUNDO?",
    "title_speech": "<speak>Qual jogador detém o recorde de mais gols na Copa do Mundo?</speak>",
    "answers": ["Pele", "Miroslav Klose", "Cristiano Ronaldo", "Lionel Messi"],
    "answers_speech": [
      "<speak>Pele</speak>",
      "<speak>Miroslav Klose</speak>",
      "<speak>Cristiano Ronaldo</speak>",
      "<speak>Lionel Messi</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Exato! Miroslav Klose detém o recorde de mais gols na Copa do Mundo!</speak>",
    "question_number": 3
  },
  {
    "title": "QUANTOS TÍTULOS DE COPA DO MUNDO POSSUI A SELEÇÃO BRASILEIRA?",
    "title_speech": "<speak>Quantos títulos de Copa do Mundo possui a seleção brasileira?</speak>",
    "answers": ["4", "5", "6", "7"],
    "answers_speech": [
      "<speak>4</speak>",
      "<speak>5</speak>",
      "<speak>6</speak>",
      "<speak>7</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Certo! O Brasil tem 5 títulos de Copa do Mundo!</speak>",
    "question_number": 4
  },
  {
    "title": "EM QUE ANO O FUTEBOL FOI INTRODUZIDO COMO ESPORTE OLÍMPICO?",
    "title_speech": "<speak>Em que ano o futebol foi introduzido como esporte olímpico?</speak>",
    "answers": ["1896", "1900", "1904", "1920"],
    "answers_speech": [
      "<speak>1896</speak>",
      "<speak>1900</speak>",
      "<speak>1904</speak>",
      "<speak>1920</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Correto! O futebol foi introduzido como esporte olímpico em 1900!</speak>",
    "question_number": 5
  },
  {
    "title": "QUAL JOGADOR ARGENTINO É CONSIDERADO UM DOS MELHORES DE TODOS OS TEMPOS?",
    "title_speech": "<speak>Qual jogador argentino é considerado um dos melhores de todos os tempos?</speak>",
    "answers": ["Lionel Messi", "Diego Maradona", "Carlos Tevez", "Gabriel Batistuta"],
    "answers_speech": [
      "<speak>Lionel Messi</speak>",
      "<speak>Diego Maradona</speak>",
      "<speak>Carlos Tevez</speak>",
      "<speak>Gabriel Batistuta</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Correto! Diego Maradona é um dos melhores jogadores argentinos de todos os tempos!</speak>",
    "question_number": 6
  },
  {
    "title": "QUAL CLUBE BRASILEIRO FOI O PRIMEIRO A CONQUISTAR A LIBERTADORES?",
    "title_speech": "<speak>Qual clube brasileiro foi o primeiro a conquistar a Libertadores?</speak>",
    "answers": ["Flamengo", "Palmeiras", "Cruzeiro", "Santos"],
    "answers_speech": [
      "<speak>Flamengo</speak>",
      "<speak>Palmeiras</speak>",
      "<speak>Cruzeiro</speak>",
      "<speak>Santos</speak>"
    ],
    "correct_answer_index": 3,
    "correct_answer_speech": "<speak>Certo! O Santos foi o primeiro clube brasileiro a vencer a Libertadores!</speak>",
    "question_number": 7
  },
  {
    "title": "QUAL FOI O PRIMEIRO PAÍS A SEDIAR A COPA DO MUNDO FORA DA EUROPA E AMÉRICA DO SUL?",
    "title_speech": "<speak>Qual foi o primeiro país a sediar a Copa do Mundo fora da Europa e América do Sul?</speak>",
    "answers": ["Japão", "Coreia do Sul", "Estados Unidos", "África do Sul"],
    "answers_speech": [
      "<speak>Japão</speak>",
      "<speak>Coreia do Sul</speak>",
      "<speak>Estados Unidos</speak>",
      "<speak>África do Sul</speak>"
    ],
    "correct_answer_index": 2,
    "correct_answer_speech": "<speak>Exato! Os Estados Unidos sediaram a Copa do Mundo de 1994!</speak>",
    "question_number": 8
  },
  {
    "title": "QUAL TIME FOI CAMPEÃO DA PRIMEIRA LIGA DOS CAMPEÕES DA UEFA?",
    "title_speech": "<speak>Qual time foi campeão da primeira Liga dos Campeões da UEFA?</speak>",
    "answers": ["Real Madrid", "Barcelona", "Milan", "Manchester United"],
    "answers_speech": [
      "<speak>Real Madrid</speak>",
      "<speak>Barcelona</speak>",
      "<speak>Milan</speak>",
      "<speak>Manchester United</speak>"
    ],
    "correct_answer_index": 0,
    "correct_answer_speech": "<speak>Correto! O Real Madrid foi o primeiro campeão da Liga dos Campeões!</speak>",
    "question_number": 9
  },
  {
    "title": "QUAL PAÍS SEDIOU A COPA DO MUNDO DE 2002?",
    "title_speech": "<speak>Qual país sediou a Copa do Mundo de 2002?</speak>",
    "answers": ["Japão", "Coreia do Sul e Japão", "Alemanha", "França"],
    "answers_speech": [
      "<speak>Japão</speak>",
      "<speak>Coreia do Sul e Japão</speak>",
      "<speak>Alemanha</speak>",
      "<speak>França</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Exato! A Copa de 2002 foi sediada por Coreia do Sul e Japão!</speak>",
    "question_number": 10
  },
  {
    "title": "QUAL É O MAIOR ESTÁDIO DE FUTEBOL DO MUNDO?",
    "title_speech": "<speak>Qual é o maior estádio de futebol do mundo?</speak>",
    "answers": ["Maracanã", "Camp Nou", "Estádio Primeiro de Maio", "Estádio Azteca"],
    "answers_speech": [
      "<speak>Maracanã</speak>",
      "<speak>Camp Nou</speak>",
      "<speak>Estádio Primeiro de Maio</speak>",
      "<speak>Estádio Azteca</speak>"
    ],
    "correct_answer_index": 2,
    "correct_answer_speech": "<speak>Correto! O maior estádio é o Estádio Primeiro de Maio, na Coreia do Norte!</speak>",
    "question_number": 11
  },
  {
    "title": "QUAL JOGADOR FOI O MAIS JOVEM A MARCAR NUMA COPA DO MUNDO?",
    "title_speech": "<speak>Qual jogador foi o mais jovem a marcar numa Copa do Mundo?</speak>",
    "answers": ["Pelé", "Kylian Mbappé", "Lionel Messi", "Diego Maradona"],
    "answers_speech": [
      "<speak>Pelé</speak>",
      "<speak>Kylian Mbappé</speak>",
      "<speak>Lionel Messi</speak>",
      "<speak>Diego Maradona</speak>"
    ],
    "correct_answer_index": 0,
    "correct_answer_speech": "<speak>Correto! Pelé foi o mais jovem a marcar numa Copa!</speak>",
    "question_number": 12
  },
  {
    "title": "QUAL FOI O PRIMEIRO CLUBE DE FUTEBOL DO MUNDO?",
    "title_speech": "<speak>Qual foi o primeiro clube de futebol do mundo?</speak>",
    "answers": ["Manchester United", "Liverpool", "Sheffield FC", "Barcelona"],
    "answers_speech": [
      "<speak>Manchester United</speak>",
      "<speak>Liverpool</speak>",
      "<speak>Sheffield FC</speak>",
      "<speak>Barcelona</speak>"
    ],
    "correct_answer_index": 2,
    "correct_answer_speech": "<speak>Exato! O Sheffield FC é o primeiro clube de futebol do mundo!</speak>",
    "question_number": 13
  },
  {
    "title": "QUAL SELEÇÃO POSSUI O MAIOR NÚMERO DE TÍTULOS DA COPA AMÉRICA?",
    "title_speech": "<speak>Qual seleção possui o maior número de títulos da Copa América?</speak>",
    "answers": ["Brasil", "Uruguai", "Argentina", "Chile"],
    "answers_speech": [
      "<speak>Brasil</speak>",
      "<speak>Uruguai</speak>",
      "<speak>Argentina</speak>",
      "<speak>Chile</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Certo! O Uruguai tem o maior número de títulos da Copa América!</speak>",
    "question_number": 14
  },
  {
    "title": "QUAL FOI O ÚNICO PAÍS A GANHAR UMA COPA DO MUNDO JOGANDO EM TODOS OS CONTINENTES?",
    "title_speech": "<speak>Qual foi o único país a ganhar uma Copa do Mundo jogando em todos os continentes?</speak>",
    "answers": ["Brasil", "Alemanha", "Itália", "Argentina"],
    "answers_speech": [
      "<speak>Brasil</speak>",
      "<speak>Alemanha</speak>",
      "<speak>Itália</speak>",
      "<speak>Argentina</speak>"
    ],
    "correct_answer_index": 0,
    "correct_answer_speech": "<speak>Correto! O Brasil venceu em todos os continentes onde a Copa foi disputada!</speak>",
    "question_number": 15
  },
  {
    "title": "QUAL JOGADOR FOI O MAIS CARO DA HISTÓRIA DO FUTEBOL?",
    "title_speech": "<speak>Qual jogador foi o mais caro da história do futebol?</speak>",
    "answers": ["Cristiano Ronaldo", "Lionel Messi", "Neymar", "Kylian Mbappé"],
    "answers_speech": [
      "<speak>Cristiano Ronaldo</speak>",
      "<speak>Lionel Messi</speak>",
      "<speak>Neymar</speak>",
      "<speak>Kylian Mbappé</speak>"
    ],
    "correct_answer_index": 2,
    "correct_answer_speech": "<speak>Correto! Neymar foi o jogador mais caro da história do futebol!</speak>",
    "question_number": 16
},
{
    "title": "QUAL CLUBE POSSUI O MAIOR NÚMERO DE TÍTULOS DA LIGA DOS CAMPEÕES?",
    "title_speech": "<speak>Qual clube possui o maior número de títulos da Liga dos Campeões?</speak>",
    "answers": ["Real Madrid", "Barcelona", "Bayern de Munique", "Liverpool"],
    "answers_speech": [
      "<speak>Real Madrid</speak>",
      "<speak>Barcelona</speak>",
      "<speak>Bayern de Munique</speak>",
      "<speak>Liverpool</speak>"
    ],
    "correct_answer_index": 0,
    "correct_answer_speech": "<speak>Exato! O Real Madrid é o clube com mais títulos da Liga dos Campeões!</speak>",
    "question_number": 17
},
{
    "title": "QUAL FOI O PRIMEIRO PAÍS A GANHAR DUAS COPAS DO MUNDO SEGUIDAS?",
    "title_speech": "<speak>Qual foi o primeiro país a ganhar duas Copas do Mundo seguidas?</speak>",
    "answers": ["Alemanha", "Itália", "Brasil", "Argentina"],
    "answers_speech": [
      "<speak>Alemanha</speak>",
      "<speak>Itália</speak>",
      "<speak>Brasil</speak>",
      "<speak>Argentina</speak>"
    ],
    "correct_answer_index": 1,
    "correct_answer_speech": "<speak>Correto! A Itália foi o primeiro país a ganhar duas Copas do Mundo seguidas!</speak>",
    "question_number": 18
},
{
    "title": "QUEM FOI O ARTILHEIRO DA COPA DO MUNDO DE 2014?",
    "title_speech": "<speak>Quem foi o artilheiro da Copa do Mundo de 2014?</speak>",
    "answers": ["Lionel Messi", "Neymar", "James Rodríguez", "Thomas Müller"],
    "answers_speech": [
      "<speak>Lionel Messi</speak>",
      "<speak>Neymar</speak>",
      "<speak>James Rodríguez</speak>",
      "<speak>Thomas Müller</speak>"
    ],
    "correct_answer_index": 2,
    "correct_answer_speech": "<speak>Exato! James Rodríguez foi o artilheiro da Copa do Mundo de 2014!</speak>",
    "question_number": 19
},
{
    "title": "QUAL SELEÇÃO GANHOU A PRIMEIRA COPA DO MUNDO FEMININA?",
    "title_speech": "<speak>Qual seleção ganhou a primeira Copa do Mundo feminina?</speak>",
    "answers": ["Estados Unidos", "Noruega", "Alemanha", "Brasil"],
    "answers_speech": [
      "<speak>Estados Unidos</speak>",
      "<speak>Noruega</speak>",
      "<speak>Alemanha</speak>",
      "<speak>Brasil</speak>"
    ],
    "correct_answer_index": 0,
    "correct_answer_speech": "<speak>Correto! Os Estados Unidos ganharam a primeira Copa do Mundo feminina!</speak>",
    "question_number": 20
}
]

# # Caminho para o arquivo CSV
csv_file = "system_usage_log.csv"

# # Início da medição do tempo
start_time = time.time()

# # Iniciar o monitoramento em paralelo
monitoring = True
monitoring_thread = threading.Thread(target=monitor_system_usage, args=(csv_file, 1))
monitoring_thread.start()

# Executar a função de geração de vídeo
full_video_quiz.generate_video({
    "title": "quiz-futebol",
    "template": "layout_template.html",
    "questions": questions
})

# Parar o monitoramento
monitoring = False
monitoring_thread.join()

# Fim da medição do tempo e cálculo do tempo de execução
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo total de execução: {elapsed_time:.2f} segundos")

# Notificação do arquivo CSV salvo
print(f"Dados de uso do sistema foram salvos em: {csv_file}")
