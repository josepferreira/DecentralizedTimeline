import logging, asyncio, sys

from kademlia.network import Server

DEBUG = True 

# starting a node
def bootstrap_node(ip, porta): 
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

   
    # bootstrap_node = (ip, porta)
    # loop.run_until_complete(server.bootstrap([bootstrap_node]))

    return (server, loop)

def main(argv):
    print('*** Start Bootstrap ***')
    (server, loop) = bootstrap_node(argv[1], int(argv[2]))

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