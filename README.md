# BUỔI THỰC HÀNH 2: LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

## Bài 1: Gửi và nhận message cơ bản qua queue

### 1. Mục tiêu
Làm quen với mô hình Producer → Queue → Consumer sử dụng RabbitMQ và Python Pika.

### 2. Môi trường
- RabbitMQ Broker: `localhost:5672`
- Virtual Host: `/`
- Queue: `iot_lab_queue`
- Thư viện Python: `pika`

### 3. Cách chạy chương trình

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

### 4. Kết quả

- Producer hiển thị thông báo gửi message thành công.
- Consumer nhận message từ queue và in nội dung cùng thời điểm nhận.
- Consumer tiếp tục lắng nghe message cho đến khi nhấn `Ctrl+C`.

Ví dụ đầu ra Consumer:

```text
[*] Chờ thông điệp. Để thoát, nhấn CTRL+C
Đã nhận message: Xin chao tu ung dung Python AMQP - ...
Thời điểm nhận: 14:05:21
```

## Bài 2. Mô phỏng cảm biến IoT gửi dữ liệu môi trường

### 1. Broker sử dụng

- Message Broker: RabbitMQ
- Giao thức: AMQP
- Thư viện Python: `pika`
- Địa chỉ: `localhost`
- Cổng: `5672`
- Queue: `sensor_data_queue`

### 2. Cách chạy chương trình

Mở 2 terminal riêng trong thư mục dự án và kích hoạt môi trường Python đã cài Pika.

**Terminal 1 - Chạy Consumer:**

```bat
python monitor_consumer_bai2.py
```

**Terminal 2 - Chạy Producer:**

```bat
python sensor_producer_bai2.py
```

Producer mô phỏng 3 cảm biến tại phòng khách, phòng ngủ và nhà bếp, sinh ngẫu nhiên nhiệt độ (20–40°C), độ ẩm (20–90%) và gửi dữ liệu JSON vào queue `sensor_data_queue` mỗi giây.

Consumer nhận và giải mã dữ liệu JSON, hiển thị thời gian nhận, mã cảm biến, vị trí, nhiệt độ và độ ẩm. Chương trình cảnh báo khi nhiệt độ > 35°C hoặc độ ẩm < 40°C.

Nhấn `Ctrl+C` trong Terminal tương ứng để dừng chương trình.

### 3. Kết quả đạt được

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

# Bài 3: Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange

## 1. Mục tiêu

Mô phỏng hệ thống IoT gửi cảnh báo liên tục qua RabbitMQ, định tuyến cảnh báo bằng Direct Exchange và Topic Exchange, đồng thời ghi log cảnh báo ra file.

## 2. Công nghệ sử dụng

- Python
- RabbitMQ
- Thư viện `pika`
- Thư viện `logging` có sẵn trong Python

## 3. Các file chương trình

- `alert_producer_bai3.py`: Gửi ba loại cảnh báo `info`, `warning`, `critical` liên tục, mỗi đợt cách nhau 5 giây.
- `warning_consumer_bai3.py`: Nhận cảnh báo `warning` qua Direct Exchange; đồng thời nhận tất cả cảnh báo qua Topic Exchange và ghi log.
- `critical_consumer_bai3.py`: Chỉ nhận cảnh báo `critical` qua Direct Exchange.
- `alerts.log`: File log được tạo tự động khi có cảnh báo được ghi lại.

## 4. Exchange và định tuyến

### Direct Exchange

Tên exchange: `iot_alert_exchange`

- Routing key `warning` được chuyển đến `warning_queue`.
- Routing key `critical` được chuyển đến `critical_queue`.
- Cảnh báo `info` không được hai queue trên nhận.

### Topic Exchange

Tên exchange: `iot_all_alerts_exchange`

- Queue: `all_alerts_queue`
- Binding key: `#`

Binding key `#` cho phép queue nhận tất cả routing key, bao gồm `info`, `warning` và `critical`. Chức năng này được tích hợp trong `warning_consumer_bai3.py` để chương trình chỉ cần ba file Python.

## 5. Cài đặt

Đảm bảo RabbitMQ đang chạy trên máy và có thể kết nối tại `localhost:5672`.

Mở terminal tại thư mục bài tập, kích hoạt môi trường ảo nếu có:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cài đặt thư viện cần thiết:

```powershell
python -m pip install pika
```

## 6. Cách chạy chương trình

Mở ba terminal riêng trong VS Code và chạy theo thứ tự:

**Terminal 1 — Warning Consumer và All Alerts Consumer**

```powershell
python warning_consumer_bai3.py
```

**Terminal 2 — Critical Consumer**

```powershell
python critical_consumer_bai3.py
```

**Terminal 3 — Producer**

```powershell
python alert_producer_bai3.py
```

Khởi động hai consumer trước producer để các queue được khai báo và bind trước khi gửi cảnh báo.

Producer gửi ba cảnh báo trong mỗi đợt, sau đó chờ 5 giây rồi tiếp tục gửi đợt mới. Nhấn `Ctrl+C` trong terminal Producer để dừng việc gửi. Có thể nhấn `Ctrl+C` trong từng terminal consumer để dừng consumer.

## 7. Kết quả mong đợi

- Warning Consumer nhận cảnh báo có routing key `warning`.
- Critical Consumer nhận cảnh báo có routing key `critical`.
- Consumer nhận tất cả cảnh báo xử lý đủ ba mức `info`, `warning` và `critical`.
- Các cảnh báo nhận bởi chức năng All Alerts được ghi nối tiếp vào `alerts.log`, bao gồm thời gian, mức cảnh báo và nội dung.
- Hệ thống tiếp tục mô phỏng cho đến khi người dùng dừng chương trình.

## 8. Lưu ý

- RabbitMQ cần hoạt động trong lúc chạy chương trình.
- File `alerts.log` được tạo tự động trong thư mục làm việc khi có cảnh báo được ghi log.
- Queue được khai báo durable và message được đánh dấu persistent để hỗ trợ tính bền vững của dữ liệu.
## 9. Kết quả chạy chương trình

### 9.1. Warning Consumer và All Alerts Consumer

Chạy lệnh:

```powershell
python .\warning_consumer_bai3.py
```

Kết quả:

```text
Warning Consumer dang cho canh bao warning...
All Alerts Consumer dang cho moi canh bao qua Topic Exchange...
Log duoc ghi vao alerts.log. Nhan Ctrl+C de dung.

[ALL ALERTS] [INFO] He thong IoT khoi dong
[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
[ALL ALERTS] [WARNING] Nhiet do phong may vuot nguong warning
[ALL ALERTS] [CRITICAL] Cam bien kho lanh mat ket noi critical

[ALL ALERTS] [INFO] He thong IoT khoi dong
[ALL ALERTS] [WARNING] Nhiet do phong may vuot nguong warning
[ALL ALERTS] [CRITICAL] Cam bien kho lanh mat ket noi critical
```

Consumer hoạt động liên tục, nhận cảnh báo `warning` qua Direct Exchange và nhận cả ba mức `info`, `warning`, `critical` qua Topic Exchange. Các cảnh báo nhận qua Topic Exchange được ghi vào file `alerts.log`.

### 9.2. Critical Consumer

Chạy lệnh:

```powershell
python .\critical_consumer_bai3.py
```

Kết quả:

```text
Critical Consumer dang cho canh bao critical...
Nhan Ctrl+C de dung chuong trinh.

[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

Critical Consumer chỉ nhận các cảnh báo có routing key `critical`, không nhận cảnh báo `info` hoặc `warning`.

### 9.3. Producer

Chạy lệnh:

```powershell
python .\alert_producer_bai3.py
```

Kết quả:

```text
Ket noi RabbitMQ thanh cong!

========== DOT CANH BAO 1 ==========
[Producer] Da gui [info]: He thong IoT khoi dong
[Producer] Da gui [warning]: Nhiet do phong may vuot nguong warning
[Producer] Da gui [critical]: Cam bien kho lanh mat ket noi critical
Cho 5 giay truoc dot tiep theo...

========== DOT CANH BAO 2 ==========
[Producer] Da gui [info]: He thong IoT khoi dong
[Producer] Da gui [warning]: Nhiet do phong may vuot nguong warning
[Producer] Da gui [critical]: Cam bien kho lanh mat ket noi critical
Cho 5 giay truoc dot tiep theo...
```

Producer gửi ba loại cảnh báo trong mỗi đợt và chờ 5 giây trước khi gửi đợt tiếp theo. Chương trình tiếp tục hoạt động cho đến khi người dùng nhấn `Ctrl+C`.

### 9.4. Đánh giá kết quả

- **Direct Exchange:** Định tuyến cảnh báo đến đúng queue theo routing key.
- **Topic Exchange:** Sử dụng binding key `#` để nhận tất cả các loại cảnh báo.
- **Consumer:** Xử lý các message liên tục và xác nhận sau khi xử lý bằng `basic_ack()`.
- **Ghi log:** Lưu thời gian, mức cảnh báo và nội dung cảnh báo vào `alerts.log`.
- **Mô phỏng IoT:** Producer tự động phát sinh các cảnh báo mẫu theo chu kỳ 5 giây.

Kết quả cho thấy hệ thống đáp ứng yêu cầu định tuyến cảnh báo, nhận thông báo liên tục và ghi log trong quá trình mô phỏng.
