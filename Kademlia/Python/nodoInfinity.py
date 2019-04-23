import asyncio
from kademlia.network import Server

loop = asyncio.get_event_loop()

# Create a node and start listening on port 5678
node = Server()
loop.run_until_complete(node.listen(5678))
print('criei o nodo')

# Bootstrap the node by connecting to other known nodes, in this case
# replace 123.123.123.123 with the IP of another node and optionally
# give as many ip/port combos as you can for other nodes.
loop.run_until_complete(node.bootstrap([("127.0.0.1", 8468)]))

loop = asyncio.get_event_loop()
loop.set_debug(True)

try:
    print('No loop')
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()