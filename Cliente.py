import socket
import time

HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 20000        # Porta do servidor

def main():
    try:
        # Cria um socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: # Cria um socket TCP/IP
            # Conecta ao servidor
            client_socket.connect((HOST, PORT))
            print(f"Conectado ao servidor {HOST}:{PORT}")

            while True:
                '''# Solicita ao usuário uma mensagem para enviar ao servidor
                message = input("Digite 'hora' para obter a hora ou 'bye' para sair: ")
                if message.lower() not in ['hora', 'bye']:
                    print("Comando inválido. Use 'hora' ou 'bye'.")
                    continue'
                

                # Envia a mensagem ao servidor
                client_socket.send(message.encode('utf-8'))'

                if message.lower() == 'bye':
                    print("Encerrando conexão com o servidor...")
                    break'
                '''
                client_socket.send(b'hora')     

                # Recebe a resposta do servidor
                data = client_socket.recv(1024)
                print("Resposta do servidor:", data.decode('utf-8'))
                time.sleep(3)
    except Exception as error:
        print(f"Erro na conexão com o servidor: {error}")
        print("Tentando novamente em 5 segundos...")
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()