# import streamlit as st
# from utils import load_data, save_data

# MENU_FILE = "data/menu_data.csv"
# ORDERS_FILE = "data/orders_data.csv"

# # Lấy số phòng từ URL
# query_params = st.experimental_get_query_params()
# room_number = query_params.get("room", [""])[0]

# if not room_number:
#     st.error("Không tìm thấy thông tin phòng. Vui lòng quét lại mã QR hoặc liên hệ quản lý.")
# else:
#     st.title("Đặt hàng Nhà Hàng")
#     st.write(f"Phòng: {room_number}")
#     # Tiếp tục logic hiển thị menu và đặt hàng...

#     menu_data = load_data(MENU_FILE)
#     if menu_data.empty:
#         st.info("Hiện tại chưa có món ăn nào.")
#     else:
#         st.subheader("Menu")
#         orders = []
#         for _, row in menu_data.iterrows():
#             st.subheader(row['Món ăn'])
#             st.write(f"Miêu tả: {row['Miêu tả']}")
#             st.write(f"Giá: {row['Giá']} VND")
#             if pd.notna(row['Ảnh']) and os.path.isfile(row['Ảnh']):
#                 st.image(row['Ảnh'], caption=row['Món ăn'])
#             quantity = st.number_input(f"Số lượng {row['Món ăn']}:", min_value=0, key=row['Món ăn'])
#             if quantity > 0:
#                 orders.append({"Phòng": room_number, "Món ăn": row['Món ăn'], "Số lượng": quantity, "Tổng giá": quantity * row['Giá']})

#         if st.button("Gửi Đơn Hàng"):
#             new_order = pd.DataFrame(orders)
#             append_unique(new_order, ORDERS_FILE, unique_col=["Phòng", "Món ăn"])  # Tránh đơn hàng trùng lặp
#             st.success("Đơn hàng đã được gửi thành công!")
import streamlit as st
from utils import read_google_sheet, write_to_google_sheet
import pandas as pd

# Tên Google Sheet
SHEET_NAME = "Hotel Data"

# Lấy số phòng từ URL
query_params = st.experimental_get_query_params()
room_number = query_params.get("room", [""])[0]

if not room_number:
    st.error("Không tìm thấy thông tin phòng. Vui lòng quét lại mã QR hoặc liên hệ quản lý.")
else:
    st.title("Đặt hàng Nhà Hàng")
    st.write(f"Phòng: {room_number}")

    # Đọc menu từ Google Sheets
    menu_data = read_google_sheet(SHEET_NAME, "menu")
    if menu_data.empty:
        st.info("Hiện tại chưa có món ăn nào.")
    else:
        st.subheader("Menu")
        orders = []
        for _, row in menu_data.iterrows():
            st.subheader(row['Món ăn'])
            st.write(f"Miêu tả: {row['Miêu tả']}")
            st.write(f"Giá: {row['Giá']} VND")
            if row['Ảnh']:
                st.image(row['Ảnh'], caption=row['Món ăn'])

            # Nhập số lượng đặt món
            quantity = st.number_input(f"Số lượng {row['Món ăn']}:", min_value=0, step=1, key=row['Món ăn'])
            if quantity > 0:
                orders.append({
                    "Phòng": room_number,
                    "Món ăn": row['Món ăn'],
                    "Số lượng": quantity,
                    "Tổng giá": quantity * row['Giá']
                })

        # Gửi đơn hàng
        if st.button("Gửi Đơn Hàng"):
            if orders:
                new_order = pd.DataFrame(orders)
                orders_data = read_google_sheet(SHEET_NAME, "orders")
                orders_data = pd.concat([orders_data, new_order], ignore_index=True)
                write_to_google_sheet(SHEET_NAME, "orders", orders_data)
                st.success("Đơn hàng đã được gửi thành công!")
            else:
                st.warning("Vui lòng chọn ít nhất một món để đặt hàng.")
