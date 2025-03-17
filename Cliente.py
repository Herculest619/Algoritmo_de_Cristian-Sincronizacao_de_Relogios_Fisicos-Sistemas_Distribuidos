import socket
import time
from datetime import datetime, timezone

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 20000        # Porta do servidor
BUFFER_SIZE = 1024  # Tamanho do buffer

def main():
    try:
        # Cria um socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conecta ao servidor
            client_socket.connect((HOST, PORT))
            print(f"\nConectado ao servidor {HOST}:{PORT}")

            while True:
                # Envia a mensagem 'hora' ao servidor e registra o tempo de envio
                start_time = time.time()
                client_socket.send(b'hora')

                # Recebe a resposta do servidor
                data = client_socket.recv(BUFFER_SIZE)
                end_time = time.time()

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
                #print("Tempo ajustado (algoritmo de Cristian):", adjusted_time)

                # Ajuste gradual do relógio
                current_time = time.time()
                time_difference = adjusted_time - current_time

                if time_difference > 0:
                    print("Relógio está atrasado. Ajustando gradualmente...")
                    # Adianta o relógio gradualmente
                    time.sleep(time_difference / 2)  # Ajuste gradual
                elif time_difference < 0:
                    print("Relógio está adiantado. Ajustando gradualmente...")
                    # Atrasa o relógio gradualmente
                    time.sleep(abs(time_difference) / 2)  # Ajuste gradual

                time.sleep(3)
    except Exception as error:
        print(f"Erro na conexão com o servidor: {error}")
        print("Tentando novamente em 5 segundos...")
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()