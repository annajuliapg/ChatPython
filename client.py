import socket
import threading

# Conectando no servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

while True:
    nomeUsuario = input("Nome de usuario: ")

    cliente.send(nomeUsuario.encode('ascii'))
    valid = cliente.recv(1024).decode('ascii')

    if valid == 'VALIDO':
        break
    print('Nome de usuário já existe na sala, digite outro')


# Escutando servidor e mandando nome de usuario
def receive():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            print(mensagem)
        except:
            # Fechando conexão com erro
            print("Um erro ocorreu")
            cliente.close()
            break
            raise

# Mandando mensagem para servidor
def write():
    while True:
        mensagem = '{}: {}'.format(nomeUsuario, input(''))
        print("\033[A\033[A") # Para apagar o escrito do input
        cliente.send(mensagem.encode('ascii'))


# Começando threads para receber e enviar
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
