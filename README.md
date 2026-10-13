# Iot_Lab2_AMQP
BUỔI THỰC HÀNH 2: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

# Bài 1: Gửi và nhận message cơ bản qua queue
# README – Bài 1: Producer và Consumer AMQP

## 1. Mục tiêu
Làm quen với mô hình Producer → Queue → Consumer sử dụng RabbitMQ và Python Pika.

## 2. Môi trường
- RabbitMQ Broker: `localhost:5672`
- Virtual Host: `/`
- Queue: `iot_lab_queue`
- Thư viện Python: `pika`

## 3. Cách chạy chương trình

Mở 2 terminal riêng trong thư mục dự án và kích hoạt môi trường Python đã cài Pika.

**Terminal 1 – Chạy Consumer:**

```bash
python -m consumer_bai1
```

Consumer kết nối RabbitMQ và chờ nhận message từ queue `iot_lab_queue`.

**Terminal 2 – Chạy Producer:**

```bash
python producer_bai1.py
```

Producer kết nối RabbitMQ, khai báo queue và gửi message vào queue.

## 4. Kết quả

- Producer hiển thị thông báo gửi message thành công.
- Consumer nhận message từ queue và in nội dung cùng thời điểm nhận.
- Consumer tiếp tục lắng nghe message cho đến khi nhấn `Ctrl+C`.

Ví dụ đầu ra Consumer:

```text
[*] Chờ thông điệp. Để thoát, nhấn CTRL+C
Đã nhận message: Xin chao tu ung dung Python AMQP - ...
Thời điểm nhận: 14:05:21
```