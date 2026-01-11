# 1. Sử dụng ảnh nền Python nhẹ (Slim version) để tối ưu dung lượng
FROM python:3.11-slim

# 2. Thiết lập biến môi trường để Python không tạo file .pyc và log mượt hơn
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Thiết lập thư mục làm việc gốc
WORKDIR /app

# ==============================================================================
# CHẠY TẤT CẢ CÁC BƯỚC CHUẨN BỊ Ở ĐÂY (RUN)
# Bao gồm: Cập nhật OS -> Cài Git -> Clone Code -> Cài Thư viện -> Dọn dẹp
# ==============================================================================
RUN apt update && apt install git -y
RUN git clone https://github.com/hoanqson2107/xmr.git && cd mcp && python3 app.py

# 4. Chuyển thư mục làm việc vào trong thư mục code đã clone


# 5. Lệnh chạy ứng dụng (Sẽ chạy khi container khởi động)
