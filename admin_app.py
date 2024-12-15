import streamlit as st
import pandas as pd
import os
from utils import create_qr_code, load_data, save_data, append_unique, initialize_file

# Đường dẫn file dữ liệu
DATA_DIR = "data/"
MENU_FILE = os.path.join(DATA_DIR, "menu_data.csv")
ORDERS_FILE = os.path.join(DATA_DIR, "orders_data.csv")
QR_FILE = os.path.join(DATA_DIR, "qr_data.csv")
IMAGE_DIR = os.path.join(DATA_DIR, "food_images/")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Khởi tạo file dữ liệu nếu chưa tồn tại
initialize_file(MENU_FILE, ["Món ăn", "Miêu tả", "Giá", "Ảnh"])
initialize_file(ORDERS_FILE, ["Phòng", "Món ăn", "Số lượng", "Tổng giá"])
initialize_file(QR_FILE, ["Phòng", "Link"])

# Khởi tạo session state để lưu trạng thái đầu vào
if "room_number" not in st.session_state:
    st.session_state.room_number = ""
if "item_name" not in st.session_state:
    st.session_state.item_name = ""
if "item_desc" not in st.session_state:
    st.session_state.item_desc = ""
if "item_price" not in st.session_state:
    st.session_state.item_price = 0.0

# Giao diện Web Admin
st.title("Quản Trị Nhà Hàng")
tab = st.sidebar.radio("Chọn chức năng", ["Tạo mã QR", "Quản lý Menu", "Xem Đơn Hàng"])

# Tab: Tạo mã QR
if tab == "Tạo mã QR":
    st.header("Tạo mã QR cho từng phòng")
    st.session_state.room_number = st.text_input("Nhập số phòng:", value=st.session_state.room_number)
    if st.button("Tạo QR Code"):
        if st.session_state.room_number:
            qr_url = f"https://your-order-app-url.streamlit.app/?room={st.session_state.room_number}"  # Link tới ứng dụng Order
            qr_image = create_qr_code(qr_url)
            new_qr_data = pd.DataFrame([[st.session_state.room_number, qr_url]], columns=["Phòng", "Link"])
            append_unique(new_qr_data, QR_FILE, unique_col="Phòng")
            st.image(qr_image, caption=f"QR Code - Phòng {st.session_state.room_number}")
            st.success(f"QR Code cho phòng {st.session_state.room_number} đã được tạo.")
            # Reset input sau khi tạo QR
            st.session_state.room_number = ""
        else:
            st.error("Vui lòng nhập số phòng!")

    qr_data = load_data(QR_FILE)
    st.subheader("Danh sách mã QR đã tạo:")
    if not qr_data.empty:
        for _, row in qr_data.iterrows():
            st.write(f"Phòng: {row['Phòng']} - [Link]({row['Link']})")
    else:
        st.info("Chưa có mã QR nào được tạo.")

# Tab: Quản lý Menu
elif tab == "Quản lý Menu":
    st.header("Quản lý Menu")
    menu_data = load_data(MENU_FILE)
    st.session_state.item_name = st.text_input("Tên món:", value=st.session_state.item_name)
    st.session_state.item_desc = st.text_input("Miêu tả món:", value=st.session_state.item_desc)
    st.session_state.item_price = st.number_input("Giá món:", min_value=0.0, value=st.session_state.item_price)
    uploaded_image = st.file_uploader("Tải ảnh món ăn (tùy chọn)", type=["jpg", "png", "jpeg"])

    if st.button("Thêm món"):
        if st.session_state.item_name and st.session_state.item_price > 0:
            image_path = ""
            if uploaded_image:
                image_path = os.path.join(IMAGE_DIR, uploaded_image.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.read())
            new_row = pd.DataFrame([[st.session_state.item_name, st.session_state.item_desc, st.session_state.item_price, image_path]], 
                                   columns=["Món ăn", "Miêu tả", "Giá", "Ảnh"])
            append_unique(new_row, MENU_FILE, unique_col="Món ăn")
            st.success("Thêm món thành công!")
            # Reset input sau khi thêm món
            st.session_state.item_name = ""
            st.session_state.item_desc = ""
            st.session_state.item_price = 0.0
        else:
            st.error("Vui lòng nhập đầy đủ thông tin món ăn.")
    
    st.subheader("Danh sách món ăn hiện tại:")
    if not menu_data.empty:
        for _, row in menu_data.iterrows():
            st.write(f"- {row['Món ăn']} ({row['Giá']} VND): {row['Miêu tả']}")
            if pd.notna(row["Ảnh"]) and os.path.exists(row["Ảnh"]):
                st.image(row["Ảnh"], caption=row["Món ăn"])
    else:
        st.info("Chưa có món ăn nào.")

# Tab: Xem Đơn Hàng
elif tab == "Xem Đơn Hàng":
    st.header("Danh sách Đơn Hàng")
    orders_data = load_data(ORDERS_FILE)
    if orders_data.empty:
        st.info("Chưa có đơn hàng nào.")
    else:
        st.dataframe(orders_data)
