import random, math

from Socket.MySocket import utilizador_online

def selecionaAleatorio(utilizadores,numero_envia):
    tam = len(utilizadores)
    if tam == 0:
        print('Utilizadores vazios')
        return ([],[])
    k = math.ceil(math.log(numero_envia))#+16 #garante 99.9999887465% de probabilidade de chegar a todos
    # segundo o artigo do cuckoo
    if k > tam:
        k = tam
    envia = []
    random.shuffle(utilizadores)
    quantos = 0

    for (i,v) in utilizadores:
        #verifica se esta online
        online = utilizador_online(v[0],v[1])
        if online:
            envia.append((i,v))
            quantos += 1
            if quantos >= k:
                break            

    return (envia,[i for i in utilizadores if i not in envia])

def cria_mensagem(mensagem,faltam):
    mensagem['faltam'] = faltam
    return mensagem