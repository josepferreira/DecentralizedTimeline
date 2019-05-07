
- Publicar mensagem
    - guarda mensagem na sua storage local
    - envia mensagem para os seus seguidores segundo uma estratégia de gossip (temos de implementar gossip depois)

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

**Falta-nos guardar na storage local**

**Temos de decidir como guardar as timelines**
- por mim tinhamos uma do utlizador
- e tinhamos uma de todos os outros
- ao guardar em disco tbm guardamos assim (separado)
- sempre que queremos mostrar fazemos um merge e ordenamos segundo um critério q pode ser o seguinte:
    - para as pubs do mesmo user têm de ser ordenadas por id
    - senão podem de ser ordenadas por timestamp

**Para eliminar podemos ter um schedule**

#### Conteúdo da mensagem
- username do utilizador
- timestamp
- id da mensagem local
- texto da publicação
- importante para o gosip:
    - nr de "vizinhos" a que tem de enviar
    - vizinhos aos quais ainda falta enviar