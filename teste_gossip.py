import random
import math
from statistics import mean
import matplotlib.pyplot as plt
import gc


def selecionaAleatorio(l,n):
    tam = len(l)
    k = math.ceil(math.log(n))+10 #garante 99.9999887465% de probabilidade de chegar a todos
    #print(k)
    # segundo o artigo do cuckoo
    if k > tam:
        k = tam
    #print('SEL: ', k)
    #print('TAM: ', len(l))
    envia = random.sample(l,k=k)
    mensagem = [i for i in l if i not in envia]
    return (envia,mensagem)

def testaGossip(lista):
    #print('-----------------------------------------')
    #print(lista)
    #print('====')
    tam = len(lista)
    nrnodos = tam
    
    (envia,mensagem) = selecionaAleatorio(lista,nrnodos)
    chegou = []
    enviei = {}
    for i in lista:
        enviei[i] = []

    mensagens = {}

    for i in envia:
        mensagens[i] = mensagem
    listaMensagens = [mensagens]

    rondas = 0
    nrMsg = len(envia)

    while(len(listaMensagens) != 0):
        rondas += 1
        novaListaMsg = []
        #if listaMensagens != []:
            #print(listaMensagens)
            #print(chegou)
        for msgs in listaMensagens:
            for k,v in msgs.items():
                novasMensagens = {}
                if k not in chegou:
                    #print('k: ', k)
                    chegou.append(k)
                    #print('C: ', chegou)
                    #print('M: ', v)
                    sel = [i for i in v if i not in enviei[k]]
                    (e,m) = selecionaAleatorio(sel,len(sel))
                    # print('Selecionei: ', len(e))
                    enviei[k].extend(e)
                    #print('NM: ', m)
                    #print('En: ', e)
                    for i in e:
                        novasMensagens[i] = m
                    novaListaMsg.append(novasMensagens)
                    nrMsg += len(e)
        listaMensagens = novaListaMsg
        #print('Rondas: ', rondas)
        #print('Chegou: ', len(chegou))

        rmm = ( nrMsg / (tam-1) ) - 1
        rel = len(chegou) / tam
    return (rondas,nrMsg,rmm,rel)

def testeGossipMedia(n,tentativas=100):
    rondas = []
    msgs = []
    rmms = []
    rels = []
    l = [i for i in range(n)]
    for i in range(tentativas):
        #print(i)
        (r,m,rm,rl) = testaGossip(l)
        rondas.append(r)
        msgs.append(m)
        rmms.append(rm)
        rels.append(rl)
    #print(msgs)
    res = (mean(rondas), mean(msgs), mean(rmms), mean(rels)) 
    del rondas, msgs, rmms, rels
    gc.collect()
    return res

rondas = []
msgs = []
rmms = []
rels = []
x = [i for i in range(100,600)]
for i in x:
    print(i)
    (r,m,rm,rl) = testeGossipMedia(i,100)
    rondas.append(r)
    msgs.append(m)
    rmms.append(rm)
    rels.append(rl)
print('Rondas: ' , rondas)
print(':::::::::::::::::::::::::::::::::::::::')
print('Mensagens: ', msgs)

plt.plot(x,rondas)
plt.ylabel('rondas')
plt.show()

plt.plot(x,msgs)
plt.ylabel('Nr. Mensagens')
plt.show()

plt.plot(x,rmms)
plt.ylabel('RMM')
plt.show()

plt.plot(x,rels)
plt.ylabel('Reliability')
plt.show()