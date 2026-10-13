import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='iot_lab_queue', durable=True, arguments={'x-queue-type': 'quorum'})

msg = 'Xin chao tu ung dung Python AMQP - B23DCCN571 - Đào Hà My!'
channel.basic_publish(
    exchange='',
    routing_key='iot_lab_queue',
    body= msg
)
print("Đã gửi thông điệp!")

connection.close()
