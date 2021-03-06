# -*- coding: utf-8 -*-
#! / usr / bin / env python 
import pika 

#Credenciales para conectarse al servidor 
credentials = pika.PlainCredentials('consumidorDos', 'password')

#Primero debemos de conectarnos al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.56.4', credentials=credentials))  # connect to server
channel = connection.channel()  # create a communication channel

#Declaramos los canales para el grupo 2 y el canal general o de Broadcast.
channel.exchange_declare (exchange = 'Grupo-02', exchange_type = 'direct' ) 
channel.exchange_declare (exchange = 'Broadcast' , exchange_type = 'fanout' ) 

#Declaramos nuevamente la cola de la que se van a recibir los mensajes, en este caso variable
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

#(Union o enlace) con cada uno de los canales
channel.queue_bind(exchange='Grupo-02', queue=queue_name, routing_key='secondGroup')
channel.queue_bind(exchange='Broadcast', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

#Recibimos el mensaje
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


#Decimos de cual cola estamos recibiendo el mensaje 
#  # how to consume the message
# which queue it will listen?
# Which method should be called on message arrival
# automatic acknowledgment activated.
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()  # initialize the consumer
