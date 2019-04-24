## Dúvidas

- Podemos usar o kademlia?
    - o kademlia n permite muitas conexões à partida?

- Se faz sentido usar um push e pull?
    - fazemos sempre um push quando existe um novo conteúdo, q será propagado pelas subscricoes
    - fazemos um pull qd há tipo um "refresh"?

- relativamente às saídos de um nodo podemos assumir q é uma saída segura avisando os vizinhos (o q pode facilitar tanto as subscricoes como hierarquias) ou temos de tratar casos em que saiam sem avisar (por exemplo por uma falha)

- para além disso podemos assumir que um nodo n está conectado a outro que quer subscrever e:
    - para o subscrever é necessário que exista um nodo intermédio q seja um "hub" e q subscreva o nodo destino, mas q n mostre as mensagens desse nó ao utilizador (pq efetivamente n o subscreveu). É possível este cenário?

    - ou seria melhor ele tentar criar uma ligação com o nodo destino diretamente (por exemplo eliminando alguma entrada na tabela e colocando aqule nodo) e apenas caso n fosse possível é q fazia o referido anteriormente? 
