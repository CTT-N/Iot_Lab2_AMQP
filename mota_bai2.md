# README - CHƯƠNG TRÌNH RABBITMQ BÀI 2

## 1. Broker sử dụng

- Message Broker: RabbitMQ
- Giao thức: AMQP
- Thư viện Python: `pika`
- Địa chỉ: `localhost`
- Cổng: `5672`
- Queue: `sensor_data_queue`

## 2. Cách chạy chương trình

Mở 2 Terminal riêng và chạy theo thứ tự:

**Terminal 1 - Chạy Consumer:**

```bat
.venv\Scripts\activate.bat
python monitor_consumer_bai2.py
```

**Terminal 2 - Chạy Producer:**

```bat
.venv\Scripts\activate.bat
python sensor_producer_bai2.py
```

Producer mô phỏng 3 cảm biến tại phòng khách, phòng ngủ và nhà bếp, sinh ngẫu nhiên nhiệt độ (20–40°C), độ ẩm (20–90%) và gửi dữ liệu JSON vào queue `sensor_data_queue` mỗi giây.

Consumer nhận và giải mã dữ liệu JSON, hiển thị thời gian nhận, mã cảm biến, vị trí, nhiệt độ và độ ẩm. Chương trình cảnh báo khi nhiệt độ > 35°C hoặc độ ẩm < 40°C.

Nhấn `Ctrl+C` trong Terminal tương ứng để dừng chương trình.

## 3. Kết quả đạt được

- Producer kết nối RabbitMQ và gửi dữ liệu của 3 cảm biến mô phỏng vào queue `sensor_data_queue`.
- Consumer nhận và hiển thị dữ liệu cảm biến theo thời gian thực.
- Hệ thống phát cảnh báo khi nhiệt độ vượt 35°C hoặc độ ẩm thấp hơn 40%.
- Consumer xác nhận bản tin hợp lệ sau khi xử lý và từ chối bản tin sai định dạng, không đưa lại queue.

**Ví dụ kết quả Consumer:**

```text
Da ket noi RabbitMQ.
Dang lang nghe queue: sensor_data_queue
Nhan Ctrl+C de dung chuong trinh.

------------------------------
Thoi gian nhan: 17:31:27
Device: sensor03
Location: Nha bep
Temperature: 34.2
Humidity: 89.7

------------------------------
Thoi gian nhan: 17:31:28
Device: sensor01
Location: Phong khach
Temperature: 32.6
Humidity: 79.6

------------------------------
Thoi gian nhan: 17:31:29
Device: sensor01
Location: Phong khach
Temperature: 32.6
Humidity: 76.5

------------------------------
Thoi gian nhan: 17:31:30
Device: sensor03
Location: Nha bep
Temperature: 28.1
Humidity: 56.1

Da dung Monitoring Consumer.
Da dong ket noi RabbitMQ.
```

**Ví dụ kết quả Producer:**

```text
Da ket noi RabbitMQ.
Dang gui du lieu vao queue: sensor_data_queue
{"device_id": "sensor03", "location": "Nha bep", "temperature": 34.2, "humidity": 89.7}
{"device_id": "sensor01", "location": "Phong khach", "temperature": 32.6, "humidity": 79.6}
{"device_id": "sensor01", "location": "Phong khach", "temperature": 32.6, "humidity": 76.5}
{"device_id": "sensor03", "location": "Nha bep", "temperature": 28.1, "humidity": 56.1}

Da dung Sensor Producer.
Da dong ket noi RabbitMQ.
```