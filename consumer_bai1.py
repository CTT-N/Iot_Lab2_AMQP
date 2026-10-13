import pika
from datetime import datetime

def connect_rabbit():
    parameters = pika.ConnectionParameters(
            host='localhost',
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

def callback(ch, method, properties, body):
    print(f"Đã nhận message: {body.decode()}")
    received_time = datetime.now().strftime("%H:%M:%S")
    print(f"Thời điểm nhận: {received_time}")

    print()
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    connection = None
    q = 'iot_lab_queue'
    
    try:
        connection, channel = connect_rabbit()

        channel.queue_declare(
            queue= q, 
            durable=True, 
            arguments={'x-queue-type': 'quorum'}
        )

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=q, on_message_callback=callback
        )

        print(' [*] Chờ thông điệp. Để thoát, nhấn CTRL+C')
        channel.start_consuming()

    except KeyboardInterrupt:
        print("Đã dừng chương trình.")

    except pika.exceptions.AMQPConnectionError as error:
        print("Loại lỗi:", type(error).__name__)
        print("Chi tiết:", repr(error))
        if error.__cause__:
            print("Nguyên nhân:", repr(error.__cause__))

    except Exception as error:
        print(f"Lỗi: {error}")

    finally:
        if connection is not None and connection.is_open:
            connection.close()
            print("Đóng kết nối RabbitMQ.")


