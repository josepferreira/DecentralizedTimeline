## Problemas

Podemos ter aqule problema da inconsistência nos seguidores ao fazer get e set na DHT.

Podemos ter um problema de se não recebermos uma mensagem nunca mais recebemos outra
- se apenas aceitarmos uma mensagem caso já tenhamos recebido a anterior então se não recebermos por exemplo a **4** não conseguimos receber mais nenhuma
    - ou aceitamos sempre a ao ordenar isso ordena (mas n garante q vejamos sempre a 5 depois da 4)
    - ou ao receber a 5 sem receber a 4 avisamos o remetente
        - pode levar a problemas de muitas conexoes (mas será pouco provável isto acontecer não?)

Podemos ter um problema se a DHT não garantir que as informações estão acessiveis (caso um saia e deixe de ser acessivel a informação que esse estava a guardar)

## Problemas do código

Ao receber uma mensagem vamos ter de verificar se o id é superior (>=id_mensagem_atual+2), e caso seja n a podemos receber (ou processar) até que chegue a outra. Temos de decidir o que fazer visto que a outra pode-se ter perdido. (Isto é importante para a estratégia como pedimos a timeline visto que apenas pedimos a partir do ultimo id, e se aceitarmos todas as mensagens podemos perder mensagens não as recebendo)

Podemos ter um problema que é ao pedir a timeline e mandar o last id, o que nos responde ainda n recebeu uma mensagem que está em trânsito, o q pode levar a q n recebamos essa mensagem tbm. (Por exemplo pedimos ao user **j** e ele responde com a timeline do **k**, no entanto vinha uma mensagem do **k** que chega posteriormente ao **j** mas n nos chega a nós pq "estávamos offline" no momento do envia dessa mensagem supostamente)

Temos de ter atenção a pedir as timelines pq podem existir utilizadores q estejam offline e n conseguimos obter essas timelines. Para isso podemos pedir a um seguidor aleatório dele.

A storage deve carregar as informações do utilizador!

As mensagens são guardadas até um dado timestamp (tempo real) o q pode provocar discrepancias. Uma possivel solucao poderia ser ter um mecanismo de sincronização de relogios.

Não consideramos tempos de envio da mensagem quando enviamos a timeline o que pode provocar que uma pub fique mais tempo num utilizador do q noutro!
