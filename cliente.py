import socket
import time
import json
from datetime import datetime, timedelta

HOST = 'localhost'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print('Conectado ao servidor')
print('Solicitando a hora atualizada ao servidor')

formato = '%H:%M:%S'


while True:

    inicioDaContagem = time.time()
    
    # Pego a resposta do servidor e decodifico 
    data = s.recv(1024)

    if data is None:
        print('Fechando a conexão')
        s.close()
        break
    
    response = data.decode()

    # Converto a resposta em JSON
    response_json = json.loads(response)

    # Extraio os dados do JSON
    horarioServidor = datetime.strptime(response_json.get('horarioAtual'), formato)
    tempoDeRespostaDoServidor = response_json.get('tempoDeResposta')
    x = response_json.get('x')
    y = response_json.get('y')


    print(f"Hora do servidor NTP: {horarioServidor.strftime('%H:%M:%S')}")
    print(f"Tempo de resposta do servidor: {str(tempoDeRespostaDoServidor)} segundos")

    fimDaContagem = time.time()

    tempoDeRespostaCliente = fimDaContagem - inicioDaContagem
    
    atraso = (( fimDaContagem - inicioDaContagem) - (y - x )) / 2

    # calculando o deslocamento
    deslocamento = (( x - inicioDaContagem + atraso) + (y - fimDaContagem - atraso )) / 2

    horaAtualizada = horarioServidor + timedelta(seconds=deslocamento)

    print(f"Tempo de requisição do cliente: {tempoDeRespostaCliente:.6f} segundos")
    print(f"Atraso: {atraso:.6f} segundos")
    print(f"Deslocamento: {deslocamento}")
    print(f"Hora alvo: {horaAtualizada.strftime('%H:%M:%S')}")

    # Ajuste gradual
    print("Iniciando ajuste gradual do relógio...")
    incremento = deslocamento / 10  # Dividir o deslocamento em 10 etapas
    for i in range(10):
        time.sleep(1)  # Espera 1 segundo entre cada ajuste
        horarioAtual = horarioServidor + timedelta(seconds=incremento * (i + 1))
        print(f"Ajuste {i + 1}: {horarioAtual.strftime('%H:%M:%S.%f')[:-3]}")

    print("Ajuste gradual concluído.")
    print('---------------------------------- \n')
    print('Solicitando a hora atualizada ao servidor....')
    print('\n')
