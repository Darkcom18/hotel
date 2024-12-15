import streamlit as st
import pandas as pd
from utils import load_data, save_data

# Các đường dẫn file
MENU_FILE = "data/menu_data.csv"
ORDERS_FILE = "data/orders_data.csv"

# Lấy số phòng từ QR Code
query_params = st.experimental_get_query_params()
room_number = query_params.get("room", [""])[0]

st.title("Đặt hàng Nhà Hàng")
st.write(f"Phòng: {room_number}")

# Hiển thị menu
menu_data = load_data(MENU_FILE)
if menu_data.empty:
    st.info("Hiện tại chưa có món ăn nào.")
else:
    st.subheader("Menu")
    orders = []
    for i, row in menu_data.iterrows():
        st.subheader(row['Món ăn'])
        st.write(f"Miêu tả: {row['Miêu tả']}")
        st.write(f"Giá: {row['Giá']} VND")
        if row['Ảnh']:
            st.image(row['Ảnh'], caption=row['Món ăn'])
        quantity = st.number_input(f"Số lượng {row['Món ăn']}:", min_value=0, key=f"quantity_{i}")
        if quantity > 0:
            orders.append({"Phòng": room_number, "Món ăn": row['Món ăn'], "Số lượng": quantity, "Tổng giá": quantity * row['Giá']})
    if st.button("Gửi đơn hàng"):
        if orders:
            orders_data = load_data(ORDERS_FILE)
            orders_data = pd.concat([orders_data, pd.DataFrame(orders)], ignore_index=True)
            save_data(orders_data, ORDERS_FILE)
            st.success("Đặt hàng thành công!")
        else:
            st.error("Vui lòng chọn ít nhất một món ăn.")
