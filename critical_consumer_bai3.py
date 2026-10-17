import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=pika.PlainCredentials("guest", "guest")
    )
)
channel = connection.channel()
channel.exchange_declare(
    exchange="iot_alert_exchange",
    exchange_type="direct",
    durable=True
)
channel.queue_declare(queue="critical_queue", durable=True)
channel.queue_bind(
    exchange="iot_alert_exchange",
    queue="critical_queue",
    routing_key="critical"
)

def callback(ch, method, properties, body):
    message = body.decode("utf-8")
    print(f"[critical_queue] Da nhan: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue="critical_queue",
    on_message_callback=callback,
    auto_ack=False
)

print("Critical Consumer dang cho canh bao critical...")
print("Nhan Ctrl+C de dung chuong trinh.")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nDang dung Critical Consumer...")
    channel.stop_consuming()
finally:
    if connection.is_open:
        connection.close()
