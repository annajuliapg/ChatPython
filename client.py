import socket
import threading

# Escolhendo o nome de usuario
nomeUsuario = input("Nome de usuario: ")

# Conectando no servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Escutando servidor e mandando nome de usuario
def receive():
    while True:
        try:
            # Receber mensagem do servidor
            # Se 'USER' mandar nome de usuario
            mensagem = cliente.recv(1024).decode('ascii')
            if mensagem == 'USER':
                cliente.send(nomeUsuario.encode('ascii'))
            else:
                print(mensagem)
        except:
            # Fechando conexão com erro
            print("Um erro ocorreu")
            cliente.close()
            break

# Mandando mensagem para servidor
def write():
    while True:
        mensagem = '{}: {}'.format(nomeUsuario, input(''))
        cliente.send(mensagem.encode('ascii'))

# Começanod threads para receber e enviar
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

