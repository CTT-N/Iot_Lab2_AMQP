import json
from datetime import datetime

import pika

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "sensor_data_queue"


def connect_rabbitmq():
    """Ket noi RabbitMQ va tao channel."""
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials(
            username="guest",
            password="guest"
        ),
        connection_attempts=3,
        retry_delay=2,
        socket_timeout=5
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return connection, channel


def declare_queue(channel):
    """Khai bao queue can nhan du lieu."""
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )


def display_sensor_data(data):
    """Hien thi thong tin cam bien."""
    received_time = datetime.now().strftime("%H:%M:%S")

    print("\n------------------------------")
    print(f"Thoi gian nhan: {received_time}")
    print(f"Device: {data['device_id']}")
    print(f"Location: {data.get('location', 'Unknown')}")
    print(f"Temperature: {float(data['temperature']):.1f}")
    print(f"Humidity: {float(data['humidity']):.1f}")


def check_alerts(temperature, humidity):
    """Kiem tra va hien thi canh bao."""
    if temperature > 35:
        print("CANH BAO: Nhiet do cao")

    if humidity < 40:
        print("CANH BAO: Do am thap")


def process_message(ch, method, properties, body):
    """Xu ly mot thong diep nhan duoc."""
    try:
        data = json.loads(body.decode("utf-8"))

        # Kiem tra cac truong du lieu bat buoc
        device_id = data["device_id"]
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])

        # Chuan hoa du lieu sau khi kiem tra
        data["device_id"] = device_id
        data["temperature"] = temperature
        data["humidity"] = humidity

        display_sensor_data(data)
        check_alerts(temperature, humidity)

        # Xac nhan da xu ly thanh cong
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError
    ) as error:
        print(f"Du lieu khong hop le: {error}")

        # Tu choi thong diep, khong dua lai vao queue
        ch.basic_reject(
            delivery_tag=method.delivery_tag,
            requeue=False
        )


def main():
    connection = None

    try:
        connection, channel = connect_rabbitmq()
        declare_queue(channel)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=process_message,
            auto_ack=False
        )

        print("Da ket noi RabbitMQ.")
        print(f"Dang lang nghe queue: {QUEUE_NAME}")
        print("Nhan Ctrl+C de dung chuong trinh.\n")

        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nDa dung Monitoring Consumer.")

    except pika.exceptions.AMQPConnectionError as error:
        print(f"Loi ket noi RabbitMQ: {error}")

    except Exception as error:
        print(f"Loi khong mong doi: {error}")

    finally:
        if connection is not None and connection.is_open:
            connection.close()
            print("Da dong ket noi RabbitMQ.")


if __name__ == "__main__":
    main()