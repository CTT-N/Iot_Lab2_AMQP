import json
import time
import random
import pika

RABBITMQ_HOST = "localhost"
QUEUE_NAME = "sensor_data_queue"

SENSORS = [
    {"device_id": "sensor01", "location": "Phong khach"},
    {"device_id": "sensor02", "location": "Phong ngu"},
    {"device_id": "sensor03", "location": "Nha bep"},
]

def connect_rabbitmq():
    """Ket noi RabbitMQ va tao channel."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    return connection, channel

def declare_queue(channel):
    """Khai bao queue neu chua ton tai."""
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

def generate_sensor_data():
    """Tao du lieu ngau nhien cho mot cam bien."""
    sensor = random.choice(SENSORS)
    
    return {
        "device_id": sensor["device_id"],
        "location": sensor["location"],
        "temperature": round(random.uniform(20, 40), 1),
        "humidity": round(random.uniform(20, 90), 1),
    }

def send_sensor_data(channel, data):
    """Gui du lieu JSON vao RabbitMQ."""
    message = json.dumps(data, ensure_ascii=False)
    
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2
        ),
    )

    print(message)

def main():
    connection = None

    try:
        connection, channel = connect_rabbitmq()
        declare_queue(channel)

        print("Da ket noi RabbitMQ.")
        print(f"Dang gui du lieu vao queue: {QUEUE_NAME}")

        while True:
            data = generate_sensor_data()
            send_sensor_data(channel, data)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDa dung Sensor Producer.")

    except Exception as error:
        print(f"Loi: {error}")

    finally:
        if connection is not None and connection.is_open:
            connection.close()
            print("Da dong ket noi RabbitMQ.")


if __name__ == "__main__":
    main()
