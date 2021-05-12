import socket
import threading
import sys

# Escolhendo o nome de usuario
nomeUsuario = ''

def setNomeUsuario():

    while True:
        sys.stdout.flush()
        nome = input("Nome de usuario: ")
        print("nome escolhido->" + nome)

        cliente.send(nome.encode('ascii'))
        valid = cliente.recv(1024).decode('ascii')

        print(valid)
        if valid == 'VALIDO':
            break
            
    global nomeUsuario
    nomeUsuario = nome
    print("sai do while: "+ nomeUsuario)

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
                setNomeUsuario()
            else:
                print(mensagem)
        except:
            # Fechando conexão com erro
            print("Um erro ocorreu")
            cliente.close()
            break
            raise
        

# Mandando mensagem para servidor
def write():
    sys.stdout.flush()
    while True:
        mensagem = '{}: {}'.format(nomeUsuario, input(''))
        cliente.send(mensagem.encode('ascii'))

# Começanod threads para receber e enviar
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

