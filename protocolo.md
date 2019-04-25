# Mensagens:

###Header

- ID da mensagem
- Origem
- Destino

### Conexão à rede

- Ping: Quando um novo peer se junta à rede deve comunicar com o bootstrap
    - boolean -> super peer ou não
- Pong: Resposta do bootstrap ao novo nodo da rede
    - ID
    - Lista de super peers ao qual se vai ligar

- NewPeer: Para estabelecer a ligação ao SuperPeer e este deve de guardar o novo nodo
    - ID

### Descoberta de candidatos a subscrever

- FindSubs: Para pedir ao super-peer para lhe mostrar os peers existentes
    - O SuperPeer pode pedir aos outros para lhe mandar alguns subs

Push, pull, findSubReply, newSubscriber, quit, ack, 