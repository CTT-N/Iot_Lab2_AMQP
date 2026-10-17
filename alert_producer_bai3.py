import time
import pika

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()
print("Ket noi RabbitMQ thanh cong!")
channel.exchange_declare(
    exchange="iot_alert_exchange",
    exchange_type="direct",
    durable=True
)
channel.exchange_declare(
    exchange="iot_all_alerts_exchange",
    exchange_type="topic",
    durable=True
)

alerts = [
    ("info", "He thong IoT khoi dong"),
    ("warning", "Nhiet do phong may vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical")
]

try:
    count = 0
    while True:
        count += 1
        print(f"\n========== DOT CANH BAO {count} ==========")

        for routing_key, message in alerts:
            properties = pika.BasicProperties(
                delivery_mode=2,
                content_type="text/plain",
                content_encoding="utf-8"
            )
            body = message.encode("utf-8")
            channel.basic_publish(
                exchange="iot_alert_exchange",
                routing_key=routing_key,
                body=body,
                properties=properties
            )
            channel.basic_publish(
                exchange="iot_all_alerts_exchange",
                routing_key=routing_key,
                body=body,
                properties=properties
            )

            print(f"[Producer] Da gui [{routing_key}]: {message}")

        print("Cho 5 giay truoc dot tiep theo...")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nNguoi dung yeu cau dung Producer.")
finally:
    if connection.is_open:
        connection.close()
    print("Da dong ket noi RabbitMQ.")
