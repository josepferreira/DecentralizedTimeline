
- Publicar mensagem
    - guarda mensagem na sua storage local
    - envia mensagem para os seus seguidores segundo uma estratégia de gossip

- Seguir utilizador
    - pedir à DHT 
    - adicionar aos seguidores
    - colocar na DHT
    - **Posivelmente pode ser feito num só passo, alterando a implementação na DHT**

- Pedir timeline
    - pedes a um dos q segues aleatórios para te dar a timeline dos q segues
    - se já tens a timeline de todos paras
    - senão pedes a um dos aleatórios q falta
        - existe uma grande probabilidade de um dos que tu segues seguirem os mm q tu

- Encontrar utlizadores
    - caso n tenhamos seguidores nem a seguir pedimos a uns aleatórios
    - caso tenhamos pedimos a esses seguidores os q eles seguem (se tivermos muitas opçõe spodemos pedir apenas uma pecetagem)
    - pode pesquisar tbm pelo nome de utilizador (pesquisa na dht)