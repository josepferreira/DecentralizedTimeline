## Problemas

Podemos ter aqule problema da inconsistência nos seguidores ao fazer get e set na DHT.

Podemos ter um problema de se não recebermos uma mensagem nunca mais recebemos outra
- se apenas aceitarmos uma mensagem caso já tenhamos recebido a anterior então se não recebermos por exemplo a **4** não conseguimos receber mais nenhuma
    - ou aceitamos sempre a ao ordenar isso ordena (mas n garante q vejamos sempre a 5 depois da 4)
    - ou ao receber a 5 sem receber a 4 avisamos o remetente
        - pode levar a problemas de muitas conexoes (mas será pouco provável isto acontecer não?)
        