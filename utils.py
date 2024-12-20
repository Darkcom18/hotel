# import pandas as pd
# import os
# import qrcode
# from io import BytesIO
# from oauth2client.service_account import ServiceAccountCredentials
# import gspread
# import json

# # Đường dẫn đến file credentials.json (nếu sử dụng cục bộ)
# CREDENTIALS_FILE = "config/credentials.json"

# def initialize_file(file_path, columns):
#     """
#     Tạo file CSV với các cột chỉ định nếu file chưa tồn tại.
#     """
#     if not os.path.exists(file_path):
#         df = pd.DataFrame(columns=columns)
#         df.to_csv(file_path, index=False)

# def load_data(file_path):
#     """
#     Load dữ liệu từ file CSV. Nếu file không tồn tại, trả về DataFrame rỗng.
#     """
#     if os.path.exists(file_path):
#         try:
#             return pd.read_csv(file_path)
#         except pd.errors.EmptyDataError:
#             return pd.DataFrame()
#     return pd.DataFrame()

# def save_data(data, file_path):
#     """
#     Lưu DataFrame vào file CSV.
#     """
#     data.to_csv(file_path, index=False)

# def create_qr_code(url):
#     """
#     Tạo mã QR từ URL và trả về dữ liệu ảnh dưới dạng byte.
#     """
#     qr = qrcode.make(url)
#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")
#     return buffer.getvalue()

# def append_unique(data, file_path, unique_col):
#     """
#     Thêm dữ liệu mới vào file CSV, chỉ thêm nếu giá trị cột `unique_col` không trùng lặp.
#     """
#     existing_data = load_data(file_path)
#     if not existing_data.empty:
#         merged_data = pd.concat([existing_data, data]).drop_duplicates(subset=unique_col, keep="first")
#     else:
#         merged_data = data
#     save_data(merged_data, file_path)

# # Google Sheets Integration
# def connect_to_google_sheet(sheet_name):
#     """
#     Kết nối đến Google Sheets thông qua Google Sheets API.
#     Args:
#         sheet_name (str): Tên của Google Sheet.
#     Returns:
#         gspread.models.Spreadsheet: Đối tượng Google Sheet.
#     """
#     # Sử dụng file tạm từ Streamlit Secrets nếu chạy trên Streamlit Cloud
#     if os.getenv("STREAMLIT_ENV") == "production":
#         credentials_dict = json.loads(os.getenv("GCP_CREDENTIALS"))
#         temp_credentials_file = "temp_credentials.json"
#         with open(temp_credentials_file, "w") as f:
#             json.dump(credentials_dict, f)
#         creds = ServiceAccountCredentials.from_json_keyfile_name(temp_credentials_file, [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive",
#         ])
#         os.remove(temp_credentials_file)
#     else:
#         # Sử dụng file credentials.json cục bộ
#         creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, [
#             "https://spreadsheets.google.com/feeds",
#             "https://www.googleapis.com/auth/drive",
#         ])
    
#     client = gspread.authorize(creds)
#     return client.open(sheet_name)

# def read_google_sheet(sheet_name, worksheet_name):
#     """
#     Đọc dữ liệu từ một worksheet trong Google Sheet.
#     Args:
#         sheet_name (str): Tên của Google Sheet.
#         worksheet_name (str): Tên của worksheet cần đọc.
#     Returns:
#         pandas.DataFrame: Dữ liệu dưới dạng DataFrame.
#     """
#     sheet = connect_to_google_sheet(sheet_name)
#     worksheet = sheet.worksheet(worksheet_name)
#     data = worksheet.get_all_records()
#     return pd.DataFrame(data)

# def write_to_google_sheet(sheet_name, worksheet_name, df):
#     """
#     Ghi dữ liệu từ DataFrame vào một worksheet trong Google Sheet.
#     Args:
#         sheet_name (str): Tên của Google Sheet.
#         worksheet_name (str): Tên của worksheet cần ghi.
#         df (pandas.DataFrame): Dữ liệu cần ghi.
#     """
#     sheet = connect_to_google_sheet(sheet_name)
#     worksheet = sheet.worksheet(worksheet_name)
#     worksheet.clear()
#     worksheet.update([df.columns.values.tolist()] + df.values.tolist())
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO
import qrcode
import json
import streamlit as st

sheet_id = "1hxHrZKQftOE1zaPzsxlrUfK_Hs2MD8N-I5NOpTahDWU"

def connect_to_google_sheet(sheet_id):
    """
    Kết nối đến Google Sheets bằng Sheet ID.
    Args:
        sheet_id (str): ID của Google Sheet.
    Returns:
        gspread.models.Spreadsheet: Đối tượng Google Sheet.
    """
    try:
        credentials_dict = st.secrets["GCP_CREDENTIALS"]
        temp_credentials_file = "temp_credentials.json"
        with open(temp_credentials_file, "w") as f:
            json.dump(dict(credentials_dict), f)

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(temp_credentials_file, scope)
        client = gspread.authorize(creds)
        os.remove(temp_credentials_file)

        # Kết nối Google Sheet
        return client.open_by_key(sheet_id)

    except SpreadsheetNotFound:
        raise ValueError(f"Google Sheet với ID '{sheet_id}' không được tìm thấy. Kiểm tra Sheet ID và quyền truy cập.")

def read_google_sheet(sheet_id, worksheet_name):
    """
    Đọc dữ liệu từ một worksheet trong Google Sheet.
    Args:
        sheet_id (str): ID của Google Sheet.
        worksheet_name (str): Tên worksheet trong Google Sheet.
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu từ worksheet.
    """
    sheet = connect_to_google_sheet(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    data = worksheet.get_all_records()  # Lấy tất cả các bản ghi dưới dạng danh sách từ điển
    return pd.DataFrame(data)

def write_to_google_sheet(sheet_id, worksheet_name, df):
    """
    Ghi dữ liệu từ DataFrame vào một worksheet trong Google Sheet.
    Args:
        sheet_id (str): ID của Google Sheet.
        worksheet_name (str): Tên worksheet trong Google Sheet.
        df (pd.DataFrame): DataFrame chứa dữ liệu cần ghi.
    """
    sheet = connect_to_google_sheet(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    worksheet.clear()  # Xóa toàn bộ dữ liệu cũ
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())  # Cập nhật dữ liệu mới

def read_menu(sheet_id):
    """
    Đọc dữ liệu menu từ worksheet "menu".
    Args:
        sheet_id (str): ID của Google Sheet.
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu menu.
    """
    return read_google_sheet(sheet_id, "menu")

def write_menu(sheet_id, menu_df):
    """
    Ghi dữ liệu menu vào worksheet "menu".
    Args:
        sheet_id (str): ID của Google Sheet.
        menu_df (pd.DataFrame): DataFrame chứa dữ liệu menu cần ghi.
    """
    write_to_google_sheet(sheet_id, "menu", menu_df)
def read_orders(sheet_id):
    """
    Đọc dữ liệu đơn hàng từ worksheet "orders".
    Args:
        sheet_id (str): ID của Google Sheet.
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu đơn hàng.
    """
    return read_google_sheet(sheet_id, "orders")
def write_orders(sheet_id, orders_df):
    """
    Ghi dữ liệu đơn hàng vào worksheet "orders".
    Args:
        sheet_id (str): ID của Google Sheet.
        orders_df (pd.DataFrame): DataFrame chứa dữ liệu đơn hàng cần ghi.
    """
    write_to_google_sheet(sheet_id, "orders", orders_df)

def create_qr_code(url):
    """
    Tạo mã QR từ URL và trả về dữ liệu ảnh dưới dạng byte.
    """
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()
