import pandas as pd
import os
import qrcode
from io import BytesIO

def initialize_file(file_path, columns):
    """
    Tạo file CSV với các cột chỉ định nếu file chưa tồn tại.
    """
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

def load_data(file_path):
    """
    Load dữ liệu từ file CSV. Nếu file không tồn tại, trả về DataFrame rỗng.
    """
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def save_data(data, file_path):
    """
    Lưu DataFrame vào file CSV.
    """
    data.to_csv(file_path, index=False)

def create_qr_code(url):
    """
    Tạo mã QR từ URL và trả về dữ liệu ảnh dưới dạng byte.
    """
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()

def append_unique(data, file_path, unique_col):
    """
    Thêm dữ liệu mới vào file CSV, chỉ thêm nếu giá trị cột `unique_col` không trùng lặp.
    """
    existing_data = load_data(file_path)
    if not existing_data.empty:
        merged_data = pd.concat([existing_data, data]).drop_duplicates(subset=unique_col, keep="first")
    else:
        merged_data = data
    save_data(merged_data, file_path)
