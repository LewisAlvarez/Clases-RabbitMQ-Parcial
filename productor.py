#! / usr / bin / env python
# -*- coding: utf-8 -*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Especificamos el canar, es decir, la cola
#channel.queue_declare(queue='Grupo-01')

#Especificamos el Exchange donde va a ir, en este caso default
#Ademas el routing_key donde va el nombre de la cosa y el body con el contenido del mensaje
#El mensaje que se va a enviar es Hello-World

channel.basic_publish(exchange='logs',
                      routing_key='Grupo-01',
                      body='Hello World!')
print(" [x] Sent 'Hello World! Grupo 1'")

channel.basic_publish(exchange='logs',
                      routing_key='Grupo-02',
                      body='Hello World!')
print(" [x] Sent 'Hello World! Grupo 2'")

channel.basic_publish(exchange='logs',
                      routing_key='Generally',
                      body='Hello World!')
print(" [x] Sent 'Hello World! Para Anbos grupos'")

connection.close()
