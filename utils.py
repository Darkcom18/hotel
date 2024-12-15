import pandas as pd
import qrcode
from io import BytesIO
from PIL import Image

import pandas as pd
import os

def load_data(file_path):
    """
    Hàm load dữ liệu từ file CSV. Nếu file không tồn tại, trả về DataFrame rỗng.
    """
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def save_data(data, file_path):
    """
    Hàm lưu dữ liệu vào file CSV.
    """
    data.to_csv(file_path, index=False)

def save_data(data, file_path):
    data.to_csv(file_path, index=False)

def create_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()
