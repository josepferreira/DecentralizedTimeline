# Estratégia

1. Quando um nodo quer entrar na rede tem de comunicar com os Master Piece
    1. O master piece vai guardá-lo;
    2. Envia nodos aleatórios para ele se conectar

2. Pede aos nodos os vizinhos e os subscritores
    1. Apresenta a lista de subscritores ao utilizador
    2. Guarda a tabela de routing

### Subscrição

- Hierarquia de subscrição 
- Gerida pela distância (xor)

## Nova estratégia

- Usar especie de gossip em que dizemos aos nós mais proximos quais são os nós que faltam
    - tentar ver a quais nos vamos conectar (ver um número sufuciente que garanta a entrega da mensagem)
    - até podemos fazer testes baseados em grafos e ver tbm o número de rondas médio
- Guardar na DHT ip, porta, id de no, followers e following ( em que nó vai ficar guardado?)