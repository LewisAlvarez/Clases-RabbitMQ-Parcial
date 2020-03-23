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
connection_Generally = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channelGenerally = connection_Generally.channel()

#Declaramos el exchange, el cual va a administrar la cola hacia el consumidor 1
channelGroupOne.exchange_declare(exchange='logs-1', exchange_type='fanout') # create a direct

#Declaramos el exchange, el cual va a administrar la cola hacia el consumidor 2
channelGroupTwo.exchange_declare(exchange='logs-2', exchange_type='fanout') # create a direct

#Declaramos el exchange, el cual va a administrar la cola hacia ambos consumidores
channelGenerally.exchange_declare(exchange='Broadcast', exchange_type='fanout') # create a fanout pipe

for i in range(22):
    if i==7 or i==14 or i==21:
            channelGenerally.basic_publish(exchange='Broadcast', routing_key='', body='Hablando a los 2 consumidores')
            print(" [x] Sent 'Hablando a los 2 consumidores")
            time.sleep(2)
    else:
            if (i % 2 == 0):
                 channelGroupOne.basic_publish(exchange='logs-1', routing_key='Grupo-01', body='Hablando con el consumidor 1, Msj:'+ str(i))
                 print(" [x] Sent 'Hablando con el consumidor 1")
                 time.sleep(2)
            else:
                 channelGroupTwo.basic_publish(exchange='logs-2', routing_key='Grupo-02', body='Hablando con consumidor 2, Msj:'+ str(i))
                 print(" [x] Sent 'Hablando con consumidor 2")
                 time.sleep(2)

    
connection_Generally.close()
connection_GroupOne.close()
connection_GroupTwo.close()