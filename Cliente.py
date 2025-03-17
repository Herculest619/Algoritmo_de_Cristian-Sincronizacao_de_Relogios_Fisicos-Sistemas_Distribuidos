import socket
import time
from datetime import datetime, timezone

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 20000        # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer

# Variável global para simular o tempo local
hora_local = time.time()  # Inicializa o tempo local com o tempo atual

def incrementar_tempo_local():
    """
    Função que incrementa o tempo local manualmente, simulando a passagem do tempo.
    """
    global hora_local
    while True:
        hora_local += 1  # Incrementa 1 segundo
        time.sleep(1)  # Espera 1 segundo antes de incrementar novamente

def main():
    global hora_local
    try:
        # Inicia a thread para incrementar o tempo local
        import threading
        threading.Thread(target=incrementar_tempo_local, daemon=True).start()

        # Cria um socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conecta ao servidor
            client_socket.connect((HOST, PORT))
            print(f"\nConectado ao servidor {HOST}:{PORT}")

            while True:
                # Envia a mensagem 'hora' ao servidor e registra o tempo de envio
                start_time = hora_local
                client_socket.send(b'hora')

                # Recebe a resposta do servidor
                data = client_socket.recv(BUFFER_SIZE)
                end_time = hora_local

                # Decodifica a resposta do servidor
                server_time_str = data.decode('utf-8')
                print("Resposta do servidor:", server_time_str)

                # Converte a string ISO 8601 para um objeto datetime
                server_time_dt = datetime.fromisoformat(server_time_str)

                # Converte o objeto datetime para um timestamp (segundos desde a época Unix)
                server_time = server_time_dt.timestamp()

                # Calcula o RTT (tempo de ida e volta)
                rtt = end_time - start_time

                # Ajusta o tempo com base no RTT (algoritmo de Cristian)
                adjusted_time = server_time + (rtt / 2)

                # Exibe o tempo ajustado
                print("Tempo recebido do servidor (timestamp):", server_time)
                print("RTT calculado:", rtt)

                # Ajuste gradual do relógio
                time_difference = adjusted_time - hora_local

                if time_difference > 0:
                    print("Adiantando relógio em", time_difference, "segundos")
                    hora_local += time_difference / 2  # Ajuste gradual
                    print("Hora local:", datetime.fromtimestamp(hora_local, timezone.utc))
                    print("\n")
                elif time_difference < 0:
                    print("Atrasando relógio em", abs(time_difference), "segundos") #abs = valor absoluto
                    hora_local += time_difference / 2  # Ajuste gradual
                    print("Hora local:", datetime.fromtimestamp(hora_local, timezone.utc))
                    print("\n")
                else:
                    print("Relógio sincronizado")
                    time.sleep(60)  # Aguarda 1 minuto antes de sincronizar novamente

                #time.sleep(1)
    except Exception as error:
        print(f"Erro na conexão com o servidor: {error}")
        print("Tentando novamente em 15 segundos...")
        time.sleep(15)
        main()

if __name__ == "__main__":
    main()