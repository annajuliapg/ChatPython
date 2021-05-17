import socket
import threading

# Conectando no servidor
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 55555))

    sala = input("Sala: ")

    cliente.send(sala.encode('ascii'))

    while True:
        nomeUsuario = input("Nome de usuario: ")

        cliente.send(nomeUsuario.encode('ascii'))
        valid = cliente.recv(1024).decode('ascii')

        if valid == 'VALIDO':
            break
        
        print('Nome de usuário já existe na sala, digite outro')

except Exception as e: 
    print(e)

# Escutando servidor e mandando nome de usuario
def receive():
    while True:
        try:
            mensagem = cliente.recv(1024).decode('ascii')
            print(mensagem)
        except Exception as e: 
            # Fechando conexão com erro
            print(e)
            cliente.close()
            break

# Mandando mensagem para servidor
def write():
    while True:
        try:
            mensagem = '{}: {}'.format(nomeUsuario, input(''))
            print("\033[A\033[A") # Para apagar o escrito do input
            cliente.send(mensagem.encode('ascii'))
        except Exception as e: 
            # Fechando conexão com erro
            print(e)
            cliente.close()
            break


# Começando threads para receber e enviar
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
