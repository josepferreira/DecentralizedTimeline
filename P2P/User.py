import logging, asyncio, sys, json, socket

from threading import Thread

from kademlia.network import Server
from Socket.MySocket import MySocket

DEBUG = False#True 

# ---------------

# Primeiro tem de se ligar ao Kademlia (nodo do bootstrap)
# Em seguida apresentar o menu

# Funções:
# - Escrever uma nova publicação
# - Seguir um Utilizador
# - Ver a timeline
# - Pedir para ver outros Users
queue = asyncio.Queue()
username = ""
ip = ""
porta = ""
following = []
timeline = []
server = Server()

# dos gajos!!!!
##
###
#####
########
##########
from Menu.Menu import Menu
import Menu.Menu as menu
from Menu.Item import Item

def build_menu():
    menu = Menu('Menu')
    menu.add_item(Item('1 - Show timeline', mostra_timeline))
    menu.add_item(Item('2 - Follow username', segue_utilizador))
    menu.add_item(Item('3 - Send message', envia_mensagem))
    menu.add_item(Item('0 - Exit', desconecta))
    return menu

def task(loop, menu):
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
    print('Esta feito')
###########
#########
#######
######
####
##
#

async def faz_pedido_seguir(idUtilizador):
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
            following.append({'id': idUtilizador, 'ip': json_user['ip'], 'porta': json_user['porta']})
            json_user['followers'][username] = (ip, porta)
            asyncio.ensure_future(server.set(idUtilizador, json.dumps(json_user)))

def segue_utilizador():
    idUtilizador = input('User Nickname: ')
    idUtilizador = idUtilizador.replace('\n', '')
    asyncio.ensure_future(faz_pedido_seguir(idUtilizador))
    return False


def mostra_timeline():
    menu.clear()
    print('*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-TIMELINE*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-')
    for msg in timeline:
        print(msg['utilizador'] + ' - ' + msg['mensagem'])
    print('*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-*#-')
    input('Press Enter')
    menu.clear()
    return False

## Para mandar mensagens

async def escreve_timeline_utilizadores(msg):
    utilizador = await server.get(username)
    seguidores = json.loads(utilizador)
    print('LALALALLALALALALALA\n\n\n\n\n\n\n')
    print(seguidores)

    if seguidores is None:
        print('ERRO: O utilizador ', username, ' não está na DHT ...')
        return
    else:
        print('Vou apresentar os sguidores: ')
        print(seguidores["followers"])
        for _,userInfo in seguidores["followers"].items():
            ms = MySocket(userInfo[0], userInfo[1])
            ms.envia(msg)
        print('AGORA VEM A PARTE DO FLOODING?')

def utilizador_online(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print('Conectar:',host,porta)
        s.connect((host, port))
        print('Connect feito')
        s.send('hi'.encode('utf-8'))
        print('Enviei')
        return True
    except:
        print('TIMEOUT TIMEOUT TIMEOUT!!!')
        return False

def transforma_msg(mensagem):
    msg = {'msg': mensagem, 'id': username}
    return json.dumps(msg)

def envia_mensagem():
    msg = input('Insert message: ')
    msg = msg.replace('\n','')
    timeline.append({'utilizador': username, 'mensagem': msg})
    print(msg)
    msg_json = transforma_msg(msg)
    asyncio.ensure_future(escreve_timeline_utilizadores(msg_json))
    return False



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

    loop.run_until_complete(server.listen(porta))

    
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
    ms = MySocket(ip, porta)
    ms.bind()
    ms.cria_fila()

def main(argv):
    print('Saudações')
    
    get_utilizador()
    get_ip()
    global porta
    porta = int(argv[1])
    print('Quero ver o ip: ', ip,porta)

    print('Realiza a conexão à DHT')
    loop = conectar_dht(ip, porta)

    asyncio.ensure_future(build_user_info())                                                    # Register in DHT user info


    loop.add_reader(sys.stdin, handle_stdin)
    
    thread = Thread(target = cria_conexao)
    thread.start()

    m = build_menu()
    asyncio.ensure_future(task(loop,m))

    utilizador_online('192.168.1.81', 7062)

    try:                                                  
        loop.run_forever()                                                                  
    except Exception:
        pass
    finally:
        print('Vai embora!')
        server.stop()                                                                       
        loop.close()                                                                        
        sys.exit(1) 

main(sys.argv)