import pandas as pd
import qrcode
from io import BytesIO
from PIL import Image

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()

def save_data(data, file_path):
    data.to_csv(file_path, index=False)

def create_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()
