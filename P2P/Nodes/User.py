import sys, socket

import logging, asyncio, sys

from kademlia.network import Server

DEBUG = True 

# ---------------

# Primeiro tem de se ligar ao Kademlia (nodo do bootstrap)
# Em seguida apresentar o menu

# Funções:
# - Escrever uma nova publicação
# - Seguir um Utilizador
# - Ver a timeline
# - Pedir para ver outros Users

nickname = ""
following = []


# starting a node
def connect_node(ip, porta): 
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # DEBUG
    if DEBUG:
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    server = Server()
    
    loop = asyncio.get_event_loop()

    loop.run_until_complete(server.listen(porta))
    
    if DEBUG:
        loop.set_debug(True)

   
    bootstrap_node = ("localhost", 7060)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    return (server, loop)

def get_nickname():
    nick = input('Escreva o seu username: ')
    return nick.replace('\n', '')

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def main(argv):
    print('*** Bem-Vindo ***')
    
    #Preciso validar os argumentos
    nickname = get_nickname()
    ip = get_ip()

    print('*** Start Bootstrap ***')
    (server, loop) = connect_node(ip, int(argv[1]))

    try:                                                  
        loop.run_forever()                                                                  
    except Exception:
        pass
    finally:
        print('Good Bye!')
        server.stop()                                                                       
        loop.close()                                                                        
        sys.exit(1) 

main(sys.argv)