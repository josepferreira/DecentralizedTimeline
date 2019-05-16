import logging, asyncio, sys, json, socket, functools, random
from datetime import datetime, timedelta

from threading import Thread

from kademlia.network import Server
from Socket.MySocket import MySocket
from Storage.MyStorage import MyStorage

from Menu.Menu import Menu
import Menu.Menu as menu
from Menu.Item import Item
import Gossip as gossip


from termcolor import colored

#sys.stderr = open('./erros.txt', 'w')


DEBUG = False#True 

# ---------------

# Primeiro tem de se ligar ao Kademlia (nodo do bootstrap)
# Em seguida apresentar o menu

# Funções:
# - Escrever uma nova publicação
# - Seguir um Utilizador
# - Ver a timeline
# - Pedir para ver outros Users

menu = Menu('Menu')
queue = asyncio.Queue()
username = ""
ip = ""
porta = ""
following = {} #vai ser um dicionário, a chave é o username e os valores:
                # ip, porta, ultima mensagem
mensagens_recebidas = []
my_timeline = []
ultima_mensagem = 0
following_timeline = []
server = Server()
myStorage = None

def build_menu():
    global menu
    menu.add_item(Item('1 - Show timeline', mostra_timeline))
    menu.add_item(Item('2 - Follow username', segue_utilizador))
    menu.add_item(Item('3 - Send message', envia_mensagem))
    menu.add_item(Item('4 - Encontrar utilizadores', encontra_utilizadores))
    menu.add_item(Item('0 - Exit', desconecta))
    return menu

def task(loop):
    global menu
    menu.draw()
    while True:
        msg = yield from queue.get()
        if not msg == '\n' and menu.run(int(msg)):
            break
        menu.draw()
    loop.call_soon_threadsafe(loop.stop)

# handler process IO request
def handle_stdin():
    data = sys.stdin.readline()
    asyncio.ensure_future(queue.put(data)) # Queue.put is a coroutine, so you can't call it directly.

def user_info(nickname, ip_address, p2p_port):
    info = {'ip': ip_address, 'porta': p2p_port, 'followers': {}}
    return json.dumps(info)

# build a json with user info and put it in the DHT
async def build_user_info():
    print('BUI')
    exists = await server.get(username)                                 #check if user exists in DHT
    if exists is None:
        print('Novo user')
        info = user_info(username, ip, porta)
        print(info)
        print(username)
        asyncio.ensure_future(server.set(username, info))
    else:
        print("Utilizador existe!!")
        saved = json.loads(exists)
        if ip != saved['ip']:
            #Necessario atualizar ip na dht
            print("Atualizado IP na DHT")
            saved['ip'] = ip
            asyncio.ensure_future(server.set(username, json.dumps(saved)))
###########
#########
#######
######
####
##
#



def novoTimestamp():
    ''' 
    Função que define o timestamp de uma publicação.
    O limite será daqi a 12h
    '''
    return datetime.timestamp(datetime.now() + timedelta(hours=12))

def encontra_vizinhos_fisicos():
    '''
        Devolve o nome dos utilizadores dos vizinhos que estao ligados diretamente a ele
    '''
    vizinhos = server.bootstrappable_neighbors()
    lista_vizinhos = []
    for (endV, portaV) in vizinhos:
         if portaV != 7060 and portaV != porta:
             socketV = MySocket(endV, portaV)
             uNovo = socketV.pede_nome_utillizador()
             lista_vizinhos.append(uNovo)
    return lista_vizinhos

async def encontra_utilizadores_a():
    '''
    Função que procura X(=10) utilizadores aleatórios que não sejam seguidores do utilizador atual para lhe mostrar.
    Primeiro tenta ver os seguidores dos utilizadores que este segue.
    Depois verifica os dos seus seguidores.
    Depois vê os seus vizinhos.
    '''
    utilizadores = set()
    encontrados = False
    a_seguir = [i for i in following.keys()]
    random.shuffle(a_seguir)
    for u in a_seguir:
        info = await server.get(u)
        info_json = json.loads(info)
        utilizadores.update([i for i in info_json['followers'] if i != username and i not in a_seguir])
        if len(utilizadores) > 10:
            encontrados = True
            break

    seguidores = []
    if encontrados == False:
        # vai buscar aos meus seguidores
        my_info = await server.get(username)
        my_info_json = json.loads(my_info)
        seguidores = my_info_json['followers'].keys()
        random.shuffle(seguidores)
        for u in seguidores:
            if u not in a_seguir:
                info = await server.get(u)
                info_json = json.loads(info)
                utilizadores.update([i for i in info_json['followers'] if i != username and i not in a_seguir])
                utilizadores.add(u)
                if len(utilizadores) > 10:
                    encontrados = True
                    break

        if encontrados == False:
            # vai buscar os vizinhos fisicos e retira todos os vizinhos fisicos que ele já viu para tras ou que já estão na lista dos utilizadores
            vizinhos_fisicos = encontra_vizinhos_fisicos()
            vizinhos_fisicos = [x for x in vizinhos_fisicos if x not in seguidores and x not in utilizadores and x not in a_seguir]
            for u in vizinhos_fisicos:
                # como o utilizador nao esta em nenhuma das outras hipoteses podemos adicioná-lo
                utilizadores.add(u)
                info = await server.get(u)
                info_json = json.loads(info)
                utilizadores.update([i for i in info_json['followers'] if i != username and i not in a_seguir])
                if len(utilizadores) > 10:
                    encontrados = True
                    break
            

    
    print('--------------Utilizadores-------------')
    if len(utilizadores) == 0:
        print(colored('Ja conhece todos os utilizadores da rede!', 'red'))
    else:
        for u in utilizadores:
            print(colored('-> User: ', 'blue'), u)
    print('---------------------------------------')

def menu_anterior():
    '''
    Limpa o menu atual e volta ao anterior
    '''
    global menu
    menu.clean()
    build_menu()

def segue_utilizador_encontra_utilizadores():
    '''
    Pede para seguir um utilizador e volta ao menu anterior.
    '''
    menu_anterior()
    segue_utilizador()

def cria_menu_encontra_utilizadores():
    '''
    Função que altera o menu quando existe um pedido para encontrar utilizadores.
    A partir daí as 2 opções são: seguir um utilizador ou voltar atrás.
    '''
    global menu
    menu.clean()
    menu.add_item(Item('1 - Seguir utilizador', segue_utilizador_encontra_utilizadores))
    menu.add_item(Item('0 - Voltar', menu_anterior))


def encontra_utilizadores():
    '''
    Faz um pedido para encontrar utilizadores e cria o novo menu.
    '''
    global menu
    cria_menu_encontra_utilizadores()
    asyncio.ensure_future(encontra_utilizadores_a())

 
async def faz_pedido_seguir(idUtilizador):
    '''
    Faz um pedido para seguir o utilizador.
    Dá erro caso o utilizador n exista ou caso já o siga.
    '''
    utilizador = await server.get(idUtilizador)

    if utilizador is None:
        print('Esse utilizador não existe! Deixe de ser assim estúpido e não nos faça perder tempo!')
    else:
        json_user = json.loads(utilizador)
        print(json_user)
        try:
            if json_user['followers'][username]:
                print('Não podes pedir para seguir porque já o segues!')
                return 
        except Exception:
            print('Following ' + idUtilizador)
            following[idUtilizador] =  {'ip': json_user['ip'], 'porta': json_user['porta'], 'ultima_mensagem':-1}
            json_user['followers'][username] = (ip, porta)
            asyncio.ensure_future(server.set(idUtilizador, json.dumps(json_user)))

def segue_utilizador():
    '''
    Função que pergunta qual o utilizador que quer seguir.
    De seguida realza um pedido para segir esse utilizador.
    '''
    idUtilizador = input('User Nickname: ')
    idUtilizador = idUtilizador.replace('\n', '')
    if idUtilizador == username:
        print('Não podes pedir para te seguir a ti próprio!')
    elif idUtilizador in following.keys():
        #estou a seguir o utilizador já, pelo q n vale a pena pedir para seguir outra vez
        print('Não podes pedir para seguir porque já o segues!')
    else:
        asyncio.ensure_future(faz_pedido_seguir(idUtilizador))
    return False

def ordena_mensagem(a,b):
    '''
    Ordena as mensagens segundo os seguintes critérios:
        - se forem do mesmo utilizador são ordenadas por id
        - se forem de utilizadores diferentes são ordenadas por timestamp
    '''
    if a['utilizador'] == b['utilizador']:
        return a['id'] - b['id']
    
    if a['data'] > b['data']:
        return 1
    if a['data'] < b['data']:
        return -1
    return 0
 
def mostra_timeline():
    '''
    Junta as timelines do utilizador e dos que este segue e mostra as mesmas ordenadas.
    '''
    global following_timeline
    timeline = [a for a in my_timeline]
    data_atual = datetime.timestamp(datetime.now())
    following_timeline = [i for i in following_timeline if i['timestamp'] > data_atual]
    print('Filtrar publicações dos followers!')
    timeline.extend(following_timeline)
    cmp = functools.cmp_to_key(ordena_mensagem)
    timeline.sort(key=cmp)
    # menu.clear()
    print('============================================TIMELINE============================================')
    for msg in timeline:
        print(msg['utilizador'] + ' - ' + msg['mensagem'])
        print(msg)
    print('================================================================================================')
    input('Press Enter')
    # menu.clear()
    return False


async def escreve_timeline_utilizadores(msg):
    '''
    Envia nova publicação para os seguidores do utilizador.
    '''
    utilizador = await server.get(username)
    seguidores = json.loads(utilizador)
    print('LALALALLALALALALALA\n\n\n\n\n\n\n')
    print(seguidores)
   
    

    if seguidores is None:
        print('ERRO: O utilizador ', username, ' não está na DHT ...')
        return
    else:
        followers = [i for i in seguidores['followers'].items()]
        envia,faltam = gossip.selecionaAleatorio(followers,len(followers))
        print('Vou apresentar os sguidores: ')
        print(seguidores["followers"])
        msg = gossip.cria_mensagem(msg, faltam)
        msg_json = json.dumps(msg)
        for _,userInfo in envia:
            ms = MySocket(userInfo[0], userInfo[1])
            ms.envia(msg_json)


def envia_mensagem():
    '''
    Pergunta qual a nova publicação e cria uma tarefa para a enviar para os seguidores.
    '''
    global ultima_mensagem
    msg = input('Insira a publicação: ')
    msg = msg.replace('\n','')
    data = datetime.now()
    mensagem = {'utilizador': username,'mensagem': msg, 'id': ultima_mensagem, 'data':str(data),'timestamp':novoTimestamp()}
    my_timeline.append(mensagem)
    
    #Update da timeline local

    print(mensagem)
    
    ultima_mensagem += 1
    mensagem_envia = {'info': mensagem}
    asyncio.ensure_future(escreve_timeline_utilizadores(mensagem_envia))
    return False


async def pede_timeline_user(utilizador,faltam):

    """
    Pede a timeline a um utilizador em especifico
    Envia também quais são os que nos faltam
    Esses têm o id da ultima publicacao que recebemos para que ele nos possa responder.
    com os pubs q tem mais recentes apenas
    """
    user_info = await server.get(utilizador) #para já vamos buscar à DHT (depois podemos ter localmente, mas temos de ter cuidado com as mudanças de ip)
    userInfo = json.loads(user_info)
    ms = MySocket(userInfo['ip'], userInfo['porta'])
    mensagem = {'e_timeline':True,'utilizadores':faltam}
    msg_json = json.dumps(mensagem)
    dados = ms.envia(msg_json)
    return dados


async def pede_timeline():

    """
    Vamos pedir a timeline
    para já assumimos que as mensagens chegam a todos
    e por isso os utilizadores têm sempre a timeline "correta"
    Para além disso para já é bloqueante
    """
    print('-----------------Pedir timeline---------------')

    faltam = following.copy()
    estao = []
    for util,_ in faltam.items():
        if util not in estao:
            try:
                (timeline,utilizadores) = await pede_timeline_user(util,{i:faltam[i]['ultima_mensagem'] for i in faltam if i not in estao})
                following_timeline.extend(timeline)
                estao.extend(utilizadores)
            except:
                print('Exceção a pedir timeline')
    
    if len(estao) != len(faltam):
        utilizadores_faltam = [i for i in faltam.keys() if i not in estao]
        print('Falta pedir timeline, provavelmente a users que estavam offline!', utilizadores_faltam)
        print('Temos de decidir o que fazer, se calhar pedimos aos seguidores deles!')

    print('----------------Terminou pedir timeline----------------')    

# exit app
def desconecta():
    return True


# starting a node
def conectar_dht(ip, porta): 
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # DEBUG
    if DEBUG:
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
    
    loop = asyncio.get_event_loop()

    loop.run_until_complete(server.listen(porta, interface=ip))

    
    if DEBUG:
        loop.set_debug(True)

   
    bootstrap_node = ("localhost", 7060)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    
    return loop

def get_utilizador():
    global username
    username = input('Escreva o seu username: ')
    username = username.replace('\n', '')

def get_ip():
    global ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

def cria_conexao():
    ms = MySocket(ip, porta, username, my_timeline, following, following_timeline)
    ms.bind()
    ms.cria_fila()
    print('4')

def extrair_informacao():
    info = myStorage.read()

    global username, my_timeline, following, following_timeline

    username = info['username']
    my_timeline = info['timeline']
    print('Colocamos todas as nossas publicações em memória???')
    following = info['following']
    data_atual = datetime.timestamp(datetime.now())
    following_timeline = list(filter(lambda a: a['timestamp'] > data_atual,info['following_timeline']))
    print('Filtramos as publicaçoes que já tenham expirado!')

def para_thread():
    ms = MySocket(ip, porta)
    mensagem = {'termina': True}
    ms.envia(json.dumps(mensagem))

def guarda_informacoes():
    """
    Guarda informações localmente
    """
    info = {}
    info['username'] = username
    info['timeline'] = my_timeline
    info['following'] = following
    info['following_timeline'] = following_timeline
    myStorage.write(info)
    print("Está tudo guardado em disco")


def main(argv):
    print('Saudações')
    
    get_utilizador()

    global myStorage

    # Inicializar armazenamento local
    myStorage = MyStorage (username)

    extrair_informacao()
    

    get_ip()
    global porta
    porta = int(argv[1])
    print('Quero ver o ip: ', ip,porta)

    print('Realiza a conexão à DHT')
    loop = conectar_dht(ip, porta)

    asyncio.ensure_future(build_user_info())                                                    # Register in DHT user info

    asyncio.ensure_future(pede_timeline())

    loop.add_reader(sys.stdin, handle_stdin)
    
    thread = Thread(target = cria_conexao)
    thread.start()

    build_menu()
    asyncio.ensure_future(task(loop))

    



    
    # print('Os nomes dos meus viznhos sao: ', encontra_vizinhos_fisicos())

    #utilizador_online('192.168.2.7', 7062)

    try:                                                  
        loop.run_forever()                                                                  
    except Exception:
        pass
    finally:
        print('Vai embora!')
        server.stop()                                                                       
        loop.close()
        para_thread()
        thread.join()
        guarda_informacoes()                                                                        
        sys.exit(1) 

main(sys.argv)