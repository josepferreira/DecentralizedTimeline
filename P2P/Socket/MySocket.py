import socket, asyncio, json

queue = ""

def processa_pedido(q): # depois tentar ver como parar
    while True:
        (conexao, endereco) = yield from q.get()
        print('Fila recebeu')
        processa_mensagem(conexao,endereco)
        
        #loop.call_soon_threadsafe(loop.stop)

def processa_mensagem(conexao, endereco): #possivelmente a timeline
    try:
        print('Conexão vinda de: ', endereco)
        while True:
            data = conexao.recv(1024)
            print('Data está: ', data)
            if data:
                print('Recebido "%s"' % data.decode('utf-8'))
                result = processa_texto(data)
                conexao.sendall(result)
            else:
                break
    except:
        print('Exception')
    finally:
        print('Fechar')
        conexao.close()
# def processa_mensagem(conexao, endereco): #possivelmente a timeline
#     try:
#         print('Conexão vinda de: ', endereco)
#         while True:
#             data = conexao.recv(1024)
#             print('Data está: ', data)
#             if data:
#                 print('Recebido "%s"' % data.decode('utf-8'))
#                 result = processa_texto(data)
#                 conexao.sendall(result)
#             else:
#                 break
#     finally:
#         conexao.close()

def processa_texto(data):
    try:
        info = json.loads(data)
        print('\n\n\n', info, '\n\n\n')
    except: pass
    #timeline.append({'id': info['id'], 'message': info['msg']})
    return 'ACK'.encode('utf-8')

# PARA ENVIAR MENSAGENS:

class MySocket:

    def __init__(self, ip, porta):
        self.ip = ip
        self.porta = porta
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        print('Bind: ',self.ip,self.porta)
        self.s.bind((self.ip, self.porta))

    def cria_fila(self):
        global queue
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        queue = asyncio.Queue()
        self.s.listen(1)
        loop.add_reader(self.s,self.listen())
        asyncio.ensure_future(processa_pedido(queue))
        loop.run_forever()                                                                 # Keeps the user online
    
    def listen(self):
        connection, client_address = self.s.accept()
        print('Conexão recebida: ',client_address)
        #self.processa_mensagem(connection,client_address)
        asyncio.ensure_future(queue.put((connection,client_address)))



    def envia(self, mensagem):
        self.s.connect((self.ip, self.porta))
        try:
            self.s.sendall(mensagem.encode('utf-8'))

            data = self.s.recv(256)
            print ('received "%s"' % data.decode('utf-8'))
            # if not data.decode('utf-8') == 'ACK':
            #     info = json.loads(data)
            #     if info['type'] == 'timeline':
            #         record_messages(data, timeline)
        finally:
            print('closing socket')
            self.s.close()