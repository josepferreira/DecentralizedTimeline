import socket, asyncio, json

class MySocket:

    def __init__(self, ip, porta):
        self.ip = ip
        self.porta = porta
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.following_timeline = []

    def bind(self):
        print('Bind: ',self.ip,self.porta)
        self.s.bind((self.ip, self.porta))

    def processa_mensagem(self, data):
        try:
            info = json.loads(data)
            # para já assumimos que a mensagem que vem é de timeline, mas pode também ser
            # de um pedido q tenhamos feito
            print('\n\n\n', info, '\n\n\n')
            self.following_timeline.append(info)
            print(self.following_timeline)
        except: pass
        #timeline.append({'id': info['id'], 'message': info['msg']})
        return 'ACK'.encode('utf-8')

    async def processa_pedido(self, client):
        request = None
        #while request != 'quit':
        request = (await self.loop.sock_recv(client, 255)).decode('utf8')
        print('Recebemos: ', request)
        response = self.processa_mensagem(request)
        await self.loop.sock_sendall(client, response)
        client.close()


    async def processa_conexoes(self):
        while True:
            client, _ = await self.loop.sock_accept(self.s)
            self.loop.create_task(self.processa_pedido(client))

    def cria_fila(self, following_timeline):
        '''
        É necessário chamar o método "listen" do socket para que ele comece a escutar conexões na porta.
        Depois é feito o add_reader, com o socket (file descriptor) e a callback para ser chamada aquando de uma ligação no socket
        '''
        #global queue
        try:
            self.following_timeline = following_timeline
            print('TIme: ', self.following_timeline)
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.s.listen(8)
            self.s.setblocking(False)
            print('Em escuta de novas conexões')
            self.loop.run_until_complete(self.processa_conexoes())
        except: 
            print('Erro na cria fila')                                                                 # Keeps the user online


    def envia(self, mensagem):
        try:
            self.s.connect((self.ip, self.porta))
            self.s.sendall(mensagem.encode('utf-8'))
            print('Consegui enviar')
            data = self.s.recv(256)
            print ('received "%s"' % data.decode('utf-8'))
            # if not data.decode('utf-8') == 'ACK':
            #     info = json.loads(data)
            #     if info['type'] == 'timeline':
            #         record_messages(data, timeline)
        except:
            print('Utilizador offline')
        finally:
            print('closing socket')
            self.s.close()