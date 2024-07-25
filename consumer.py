"""
Módulo para consumir mensajes de RabbitMQ y enviar notificaciones por correo electrónico.
"""

import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pika

class Consumer:
    def __init__(self):
        self.last_message_time = time.time()

    def send_email(self, body):
        """
        Envía un correo electrónico con el cuerpo dado.
        """
        sender_email = "chevyagcr@gmail.com"
        receiver_email = "chevyagcr@gmail.com"
        password = "hiie zbbc vrvt mnhh"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Notificación de Actualización de Pregunta"
        message["From"] = sender_email
        message["To"] = receiver_email

        text = body
        part = MIMEText(text, "plain")
        message.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    def callback(self, ch, method, properties, body):  # pylint: disable=unused-argument
        """
        Función de callback para manejar los mensajes recibidos.
        """
        print(f" [x] Recibido {body!r}")
        self.send_email(body.decode())
        self.last_message_time = time.time()

    def monitor_activity(self):
        """
        Monitorea la actividad del consumidor.
        """
        while True:
            time.sleep(1)
            # Esto se puede usar para monitoreo adicional si es necesario

def main():
    consumer = Consumer()
    connection = pika.BlockingConnection(pika.ConnectionParameters('host.docker.internal'))
    channel = connection.channel()

    channel.queue_declare(queue='pregunta_updates')

    channel.basic_consume(queue='pregunta_updates', on_message_callback=consumer.callback, auto_ack=True)

    # Inicia el monitoreo de actividad en un hilo separado
    activity_thread = threading.Thread(target=consumer.monitor_activity, daemon=True)
    activity_thread.start()

    print(' [*] Esperando por mensajes')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Se detuvo por el usuario.")
    finally:
        connection.close()

if __name__ == "__main__":
    main()