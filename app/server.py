import socket
import ntplib
from time import ctime
import time
import json
from threading import Thread

HOST = '0.0.0.0'
PORT = 50000

# Função para buscar a hora atualizada do servidor NTP
def buscarHoraNTP():
    c = ntplib.NTPClient()
    resposta = c.request('pool.ntp.org')
    tempoCompleto = ctime(resposta.tx_time)
    hora = tempoCompleto[11:19]
    return hora

# Função para lidar com cada cliente
def conectarClientes(conn, ender):
    print('Conectado em', ender)
    try:
        while True:
            inicioDaContagem = time.time()

            horarioAtual = buscarHoraNTP()

            fimDaContagem = time.time()

            tempoDeResposta = fimDaContagem - inicioDaContagem

            print(f"Tempo de resposta do servidor: {tempoDeResposta:.6f} segundos")

            response_data = {
                "horarioAtual": horarioAtual,
                "tempoDeResposta": tempoDeResposta,
                "x": inicioDaContagem,
                "y": fimDaContagem
            }
            print(response_data)

            conn.send(json.dumps(response_data).encode())
            time.sleep(15)
    finally:
        conn.send(json.dumps(None).encode())
        conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# O servidor ficará ouvindo até 4 conexões
s.listen(4)

print('Aguardando conexão de um cliente')

while True:
    conn, ender = s.accept()
    client_thread = Thread(target=conectarClientes, args=(conn, ender))
    client_thread.start()


