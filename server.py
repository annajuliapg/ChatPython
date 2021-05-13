import socket
import threading

# infos para conexão
host = '127.0.0.1'
port = 55555

# Iniciando servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Servidor Iniciado!")

# Listas para clientes (ip e porta) e nomes de usuario
clientes = []
usuarios = []

# Mandando mensagem para todos os clientes conectados
def broadcast(mensagem):
    for cliente in clientes:
        cliente.send(mensagem)

# Administranod mensagem dos clientes
def handle(cliente):
    while True:
        try:
            # Broadcast de mensagens - envia para todos os clientes
            mensagem = cliente.recv(1024)
            broadcast(mensagem)
        except:
            # Removendo e desconectando clientes
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nomeUsuario = usuarios[index]
            # Manda para os clientes
            broadcast(str("-------------------------------\n" + "{} saiu!".format(nomeUsuario)).encode('ascii'))
            # Printa no server
            print(str("-------------------------------\n" + "{} saiu!".format(nomeUsuario)))
            usuarios.remove(nomeUsuario)
            # Manda para os clientes
            broadcast(str("Usuarios Online: " + " | ".join(usuarios) + "\n-------------------------------").encode('ascii'))
            # Printa no server
            print(str("Usuarios Online: " + " | ".join(usuarios) + "\n-------------------------------"))
            break
            raise

def verificaNomeUsuario(nomeUsuario, cliente):
    if nomeUsuario in usuarios:
        cliente.send('INVALIDO'.encode('ascii'))
        return False
    else:
        cliente.send('VALIDO'.encode('ascii'))
        return True

# Recebendo e administrando mensagens
def receive():
    while True:
        # Aceitando conexão
        cliente, address = server.accept()
        print("Conectado com {}".format(str(address)))

        while True:
            # Requisitando e guardando nome de usuario
            #cliente.send('USER'.encode('ascii'))
            nomeUsuario = cliente.recv(1024).decode('ascii')

            if verificaNomeUsuario(nomeUsuario, cliente):
                break

        usuarios.append(nomeUsuario)
        clientes.append(cliente)

        # Printando e enviando nome de usuarios conectados
        print("Nome de usuario: {}".format(nomeUsuario))

        #broadcast(str("-------------------------------\n" + "{} entrou!".format(nomeUsuario)).encode('ascii'))
        broadcast(f"-------------------------------\n{nomeUsuario} entrou! ".encode('ascii'))
        broadcast(f"Usuarios Online: {' | '.join(usuarios)}\n-------------------------------".encode('ascii'))
        
        cliente.send("\nConectado no servidor!".encode('ascii'))

        # Começando thread para clientes
        thread = threading.Thread(target=handle, args=(cliente,))
        thread.start()

receive()
