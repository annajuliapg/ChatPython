import socket
import threading

# Info para conexão
host = '127.0.0.1'
port = 55555

# Iniciando servidor
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Servidor Iniciado!\n-------------------------------")
except Exception as e: 
    print(e)

# Lista para guardar as salas e usuarios conectados nelas
salas = {}

# Ver lista de usuários na sala
def userList(idSala):
    if len(salas[idSala]['usuarios']) == 0:
        return 0
    else:
        return (' | '.join(salas[idSala]['usuarios']))

# Mandando mensagem para todos os clientes conectados
def broadcast(mensagem, idSala):
    for cliente in salas[idSala]['clientes']:
        cliente.send(mensagem)

# Administrando mensagem dos clientes
def handle(cliente, idSala):
    while True:
        try:
            # Broadcast de mensagens: envia para todos os clientes na sala
            mensagem = cliente.recv(1024)
            broadcast(mensagem, idSala)
        except:
            # Removendo e desconectando clientes
            index = salas[idSala]['clientes'].index(cliente)
            salas[idSala]['clientes'].remove(cliente)
            nomeUsuario = salas[idSala]['usuarios'][index]
            salas[idSala]['usuarios'].remove(nomeUsuario)

            # Printa no server
            print(f"Sala: {idSala}\n{nomeUsuario} {cliente.getpeername()} saiu!\nUsuarios Online na Sala: {userList(idSala)}\n-------------------------------")

            #Fecha o socket
            cliente.close()

            # Manda para os clientes
            broadcast(f"-------------------------------\n{nomeUsuario} saiu!\nUsuarios Online na Sala {idSala}: {userList(idSala)}\n-------------------------------".encode('ascii'), idSala)
            break

# Recebendo conexão do cliente
def receive():
    while True:
        try:
            # Aceitando conexão
            cliente, address = server.accept()
            print(f"Conectou: {address}")

            idSala = str(cliente.recv(1024).decode('ascii'))

            print(f"Sala: {idSala}")

            # Verificando se a sala ja existe
            if idSala in salas:
                # Se a sala existe, verificar se o nome de usuario ja esta sendo usado na sala
                while True:
                    # Requisitando e guardando nome de usuario
                    nomeUsuario = cliente.recv(1024).decode('ascii')

                    if nomeUsuario not in salas[idSala]['usuarios']:
                        cliente.send('VALIDO'.encode('ascii'))
                        break
                    cliente.send('INVALIDO'.encode('ascii'))

            else:
                # Se a sala não existia ela é criada, não é preciso verificar o nome de usuario
                nomeUsuario = cliente.recv(1024).decode('ascii')
                cliente.send('VALIDO'.encode('ascii'))
                salas[idSala] = {'clientes': [], 'usuarios':[]}

            salas[idSala]['clientes'].append(cliente)
            salas[idSala]['usuarios'].append(nomeUsuario)

            # Printando e enviando nome de usuarios conectados
            print(f"Nome de usuario: {nomeUsuario}\n-------------------------------")

            broadcast(f"-------------------------------\n{nomeUsuario} entrou!\nUsuarios Online na Sala {idSala}: {userList(idSala)}\n-------------------------------".encode('ascii'), idSala)
            
            cliente.send("\nConectado no servidor!".encode('ascii'))

            # Começando thread para clientes
            thread = threading.Thread(target=handle, args=(cliente, idSala))
            thread.start()
        
        except Exception as e: 
            print(e)

receive()
