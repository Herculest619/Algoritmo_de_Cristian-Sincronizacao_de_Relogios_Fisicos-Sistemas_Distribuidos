import socket
import sys
import ntplib
from datetime import datetime, timezone
from threading import Thread, Lock
import time

HOST = '127.0.0.1'  # Endereço IP Localhost
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # Tamanho do buffer para recepção dos dados

# Variável global para armazenar a hora atual ajustada
current_time = None
# Lock para garantir acesso seguro à variável global
time_lock = Lock()
# Intervalo de atualização da hora via NTP (em segundos)
UPDATE_INTERVAL = 10

def update_time_periodically():
    """
    Função que atualiza a hora via NTP periodicamente, ajustando o atraso da rede.
    """
    global current_time
    client = ntplib.NTPClient()

    while True:
        try:
            response = client.request('pool.ntp.org')
            ntp_time = response.tx_time  # Hora recebida do servidor NTP
            print("Hora recebida em segundos:", ntp_time)

            offset = response.offset  # Atraso da rede (offset) = RTT/2
            print("Atraso da rede em segundos:", offset)

            # Ajusta a hora com base no atraso da rede
            adjusted_time = ntp_time + offset

            with time_lock:
                current_time = adjusted_time  # Armazena o tempo ajustado em segundos

            print("Hora atualizada via NTP (ajustada):", datetime.fromtimestamp(adjusted_time, timezone.utc))
            print("\n")

        except Exception as error:
            print("Erro ao atualizar a hora via NTP:", error)

        time.sleep(UPDATE_INTERVAL)  # Espera o intervalo especificado antes de atualizar novamente

def get_current_time():
    """
    Retorna o tempo atual ajustado, considerando o tempo decorrido desde a última sincronização.
    """
    global current_time
    with time_lock:
        if current_time is None:
            return None
        # Calcula o tempo decorrido desde a última sincronização
        elapsed_time = time.time() - current_time
        return current_time + elapsed_time

def on_new_client(clientsocket, addr):
    """
    Função para tratar cada nova conexão de cliente.
    """
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)  # Recebe os dados do cliente
            if not data:  # Se não receber dados, encerra a conexão
                break
            texto_recebido = data.decode('utf-8')  # Converte os bytes em string
            print('\nRecebido do cliente {} na porta {}: {}'.format(addr[0], addr[1], texto_recebido))  # Imprime o texto recebido

            # Responde ao cliente com a hora atual ajustada ou uma mensagem personalizada
            if texto_recebido.lower() == 'hora':
                current_time_value = get_current_time()
                if current_time_value is not None:
                    time_to_send = datetime.fromtimestamp(current_time_value, timezone.utc).isoformat()
                else:
                    time_to_send = "Hora não disponível"
                clientsocket.send(time_to_send.encode('utf-8'))
            elif texto_recebido.lower() == 'bye':
                clientsocket.send(b'Encerrando conexao. Adeus!')
                print('\nVai encerrar o socket do cliente {} !'.format(addr[0]))
                clientsocket.close()  # Encerra o socket do cliente
                return
            else:
                clientsocket.send(data)  # Envia o mesmo texto ao cliente
        except Exception as error:
            print("\nErro na conexão com o cliente:", error)
            return

def main(argv):
    try:
        # Inicia a thread para atualizar a hora periodicamente
        time_thread = Thread(target=update_time_periodically)
        time_thread.daemon = True  # Thread encerra quando o programa principal terminar
        time_thread.start()

        # Configura o socket para aceitar conexões
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Servidor escutando em {HOST}:{PORT}...")

            while True:
                clientsocket, addr = server_socket.accept()
                print('\nConectado ao cliente no endereço:', addr)
                client_thread = Thread(target=on_new_client, args=(clientsocket, addr))
                client_thread.start()  # Inicia uma nova thread para tratar o cliente
    except Exception as error:
        print("\nErro na execução do servidor!!")
        print(error)

if __name__ == "__main__":
    main(sys.argv[1:])