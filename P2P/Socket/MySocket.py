import socket, asyncio, json, sys
from datetime import datetime, timedelta

def novoTimestamp():
    #vamos guardar 12h
    return datetime.timestamp(datetime.now() + timedelta(hours=12))

def alteraTimestamp(elem,t):
    delta = elem['timestamp'] - t
    elem['timestamp'] = datetime.timestamp(datetime.now() + timedelta(seconds=delta))
    return elem

class MySocket:

    def __init__(self, ip, porta, username="",
                my_timeline=[],following={},following_timeline=[]):
        self.ip = ip
        self.porta = porta
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.my_timeline = my_timeline
        self.following = following
        self.following_timeline = following_timeline
        self.continua = True

    def bind(self):
        print('Bind: ',self.ip,self.porta)
        self.s.bind((self.ip, self.porta))

    def processa_pedido_timeline(self, data):
        # print('processa pedido')
        print(data)
        # intersecao de sets para saber quais os que eu sigo q o outro quer
        utilizadores_comuns = data['utilizadores'].keys() & self.following.keys()
        
        # apenas vou enviar se o id da ultima mensagem do outro for inferior ao meu
        faltam = {i:data['utilizadores'][i] for i in utilizadores_comuns 
                            if self.following[i]['ultima_mensagem'] > data['utilizadores'][i]}
        faltam[self.username] = data['utilizadores'][self.username]
        print(faltam)

        # colocar a timeline dos que eu sigo
        timeline_r = [i for i in self.following_timeline 
                        if i['utilizador'] in faltam.keys()
                        and faltam[i['utilizador']] < i['id']]
        
        print('Passei faltam')
        # colocar a minha timeline, apenas as q já passaram o tempo
        print(self.my_timeline)
        my_timeline_r = [i for i in self.my_timeline if i['id'] > faltam[self.username]
                                                    and i['timestamp'] > datetime.timestamp(datetime.now())]

        print('Passei minha')
        print(timeline_r)
        timeline_r.extend(my_timeline_r)

        utilizadores = [i for i in utilizadores_comuns]
        utilizadores.append(self.username)
        
        # print(timeline_r)
        resposta = {'timeline':timeline_r,
                'utilizadores':utilizadores,'e_timeline':True, 'timestamp':datetime.timestamp(datetime.now())}
        print(resposta)
        return resposta

    def processa_mensagem(self, data):
        resposta = 'ACK'.encode('utf-8')
        try:
            info = json.loads(data)
            print('\n\n\n', info, '\n\n\n')
            if 'e_timeline' in info.keys():
                # é um pedido de timeline, temos de responder
                # print('E TIMELINE')
                msg = self.processa_pedido_timeline(info)
                resposta = json.dumps(msg).encode('utf-8')
                # print('RESP:')
                # print(resposta)
                return resposta

            # para já assumimos que a mensagem que vem é de timeline, mas pode também ser
            # de um pedido q tenhamos feito
            else:
                if 'termina' in info.keys():
                    self.continua = False
                else:
                    if 'pedido_utilizador' in info.keys():
                        print('Estao a pedir-me o username!!')
                        msg = {'utilizador': self.username}
                        resposta = json.dumps(msg).encode('utf-8')
                    else:
                        info['timestamp'] = novoTimestamp()
                        self.following_timeline.append(info)
                        if info['id'] > self.following_timeline[info['utilizador']]['ultima_mensagem']:
                            print('depois ver o caso de se for maior que k+2')
                            self.following[info['utilizador']]['ultima_mensagem'] = info['id']              
                # print(self.following_timeline)
        except: pass
        #timeline.append({'id': info['id'], 'message': info['msg']})
        print(resposta)
        return resposta

    async def processa_pedido(self, client):
        request = None
        #while request != 'quit':
        request = (await self.loop.sock_recv(client, 255)).decode('utf8')
        print('Recebemos: ', request)
        response = self.processa_mensagem(request)
        await self.loop.sock_sendall(client, response)
        client.close()
        if self.continua == False:
            self.loop.stop()


    async def processa_conexoes(self):
        while True:
            client, _ = await self.loop.sock_accept(self.s)
            self.loop.create_task(self.processa_pedido(client))

    def cria_fila(self):
        '''
        É necessário chamar o método "listen" do socket para que ele comece a escutar conexões na porta.
        Depois é feito o add_reader, com o socket (file descriptor) e a callback para ser chamada aquando de uma ligação no socket
        '''
        #global queue
        try:
            print('TIme: ', self.following_timeline)
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.s.listen(8)
            self.s.setblocking(False)
            print('Em escuta de novas conexões')
            self.loop.run_until_complete(self.processa_conexoes())
        except: 
            print('Erro na cria fila')                                                                 # Keeps the user online
    
    def pede_nome_utillizador(self):
        data = None
        try:
            msg = {'pedido_utilizador': True}
            mensagem = json.dumps(msg)
            self.s.connect((self.ip, self.porta))
            self.s.sendall(mensagem.encode('utf-8'))
            data = self.s.recv(256)
            recebido = data.decode('utf-8')
            try:
                dados = json.loads(recebido)
                data = dados['utilizador']
            except:
                pass
        except:
            print('Utilizador offline')
        finally:
            print('closing socket')
            self.s.close()
            return data


    def envia(self, mensagem):
        data = None
        try:
            self.s.connect((self.ip, self.porta))
            self.s.sendall(mensagem.encode('utf-8'))
            print('Consegui enviar')
            data = self.s.recv(256)
            print ('receivedasd "%s"' % data.decode('utf-8'))
            recebido = data.decode('utf-8')
            try:
                dados = json.loads(recebido)
                print(dados)
                if 'e_timeline' in dados.keys():
                    # é resposta de timeline
                    # vamos atualizar os timestamps (e talvez filtrar as q n podiam ser enviadas)
                    dados['timeline'] = [alteraTimestamp(i,dados['timestamp']) for i in dados['timeline'] if i['timestamp'] > dados['timestamp']]
                    print('Filtrar os que terminam e atualizar a data de término dos outros! Não consideramos tempos de entrega da mensagem!')
                    data = (dados['timeline'],dados['utilizadores'])
                    print(data)
            except:
                pass
            # if not data.decode('utf-8') == 'ACK':
            #     info = json.loads(data)
            #     if info['type'] == 'timeline':
            #         record_messages(data, timeline)
        except:
            print('Utilizador offline')
        finally:
            print('closing socket')
            self.s.close()
            return data