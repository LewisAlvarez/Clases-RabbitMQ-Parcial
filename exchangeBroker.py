#! / usr / bin / env python
# -*- coding: utf-8 -*-
import pika
import time
#Hacemos la conexxion con el servidor
#Creamos el canal de comunicacion

#Conxxion canal Grupo-01 para el consumidor Consumidor-1
connection_GroupOne = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channelGroupOne = connection_GroupOne.channel()

#Conxxion canal Grupo-02 para el consumidor Consumidor-2
connection_GroupTwo = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channelGroupTwo = connection_GroupTwo.channel()

#Conxxion canal General (Broadcast) para ambos consumidores
connection_Generally = pika.BlockingConnection(pika.ConnectionParameters('localhost')) #Todas se conectan con el servidor rabbit en localhost -- el Fanout la deberia hacer
channelGenerally = connection_Generally.channel()

#Declaramos el exchange, el cual va a administrar la cola hacia el consumidor 1
channelGroupOne.exchange_declare(exchange='Grupo-01', exchange_type='direct') # create a direct

#Declaramos el exchange, el cual va a administrar la cola hacia el consumidor 2
channelGroupTwo.exchange_declare(exchange='Grupo-02', exchange_type='direct') # create a direct

#Declaramos el exchange, el cual va a administrar la cola hacia ambos consumidores
channelGenerally.exchange_declare(exchange='Broadcast', exchange_type='fanout') # create a fanout pipe

#Mensajes

for i in range(22):
    if i==7 or i==14 or i==21:
            channelGenerally.basic_publish(exchange='Broadcast', routing_key='', body='Hablando a los 2 consumidores')
            print(" [x] Sent 'Hablando a los 2 consumidores")
            time.sleep(2)
    else:
            if (i % 2 == 0):
                mensajeGrupoUno = 'Hablando con el consumidor 1 - '+ "Msj: "+str(i)
                channelGroupOne.basic_publish(exchange='Grupo-01', routing_key='firstGroup', body=mensajeGrupoUno)
                print(" [x] Sent " + str(mensajeGrupoUno) )
                time.sleep(2)
            else:
                mensajeGrupoDos = 'Hablando con el consumidor 2 - '+ "Msj:" +str(i)
                channelGroupTwo.basic_publish(exchange='Grupo-02', routing_key='secondGroup', body=mensajeGrupoDos)
                print(" [x] Sent " + str(mensajeGrupoDos))
                time.sleep(2)

#Cerramos las conexiones
connection_Generally.close()
connection_GroupOne.close()
connection_GroupTwo.close()