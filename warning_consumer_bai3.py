import logging
import pika

logging.basicConfig(
    filename="alerts.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()
channel.exchange_declare(
    exchange="iot_alert_exchange",
    exchange_type="direct",
    durable=True
)
channel.queue_declare(queue="warning_queue", durable=True)
channel.queue_bind(
    exchange="iot_alert_exchange",
    queue="warning_queue",
    routing_key="warning"
)
channel.exchange_declare(
    exchange="iot_all_alerts_exchange",
    exchange_type="topic",
    durable=True
)
channel.queue_declare(queue="all_alerts_queue", durable=True)
channel.queue_bind(
    exchange="iot_all_alerts_exchange",
    queue="all_alerts_queue",
    routing_key="#"
)

def warning_callback(ch, method, properties, body):
    message = body.decode("utf-8")
    print(f"[warning_queue] Da nhan: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def all_alerts_callback(ch, method, properties, body):
    message = body.decode("utf-8")
    level = method.routing_key.upper()
    print(f"[ALL ALERTS] [{level}] {message}")
    logging.info("[%s] %s", level, message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue="warning_queue",
    on_message_callback=warning_callback,
    auto_ack=False
)
channel.basic_consume(
    queue="all_alerts_queue",
    on_message_callback=all_alerts_callback,
    auto_ack=False
)

print("Warning Consumer dang cho canh bao warning...")
print("All Alerts Consumer dang cho moi canh bao qua Topic Exchange...")
print("Log duoc ghi vao alerts.log. Nhan Ctrl+C de dung.")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nDang dung Warning / All Alerts Consumer...")
    channel.stop_consuming()
finally:
    if connection.is_open:
        connection.close()
    print("Da dong ket noi.")
