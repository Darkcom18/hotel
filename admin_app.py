import streamlit as st
import pandas as pd
import os
from utils import create_qr_code, load_data, save_data

# Các đường dẫn file
QR_FILE = "data/qr_data.csv"
MENU_FILE = "data/menu_data.csv"
ORDERS_FILE = "data/orders_data.csv"
IMAGE_DIR = "data/food_images/"

# Tạo thư mục ảnh nếu chưa tồn tại
os.makedirs(IMAGE_DIR, exist_ok=True)

# Sidebar Tabs
st.sidebar.title("Quản trị Nhà Hàng")
tab = st.sidebar.radio("Chọn chức năng", ["Tạo mã QR", "Tạo menu đồ ăn/thức uống", "Xem menu hiện tại", "Danh sách QR Code đã tạo", "Xem danh sách đơn hàng"])

if tab == "Tạo mã QR":
    st.header("Tạo mã QR cho từng phòng")
    qr_data = load_data(QR_FILE)
    room_number = st.text_input("Nhập số phòng:")
    if st.button("Tạo QR Code"):
        if room_number:
            qr_url = f"https://<streamlit-cloud-url>/order?room={room_number}"  # Link tới Web đặt hàng
            qr_image = create_qr_code(qr_url)
            qr_data = pd.concat([qr_data, pd.DataFrame([[room_number, qr_url]], columns=["Phòng", "Link"])], ignore_index=True)
            save_data(qr_data, QR_FILE)
            st.image(qr_image, caption=f"QR Code - Phòng {room_number}")
            st.success(f"QR Code cho phòng {room_number} đã được tạo và lưu.")
        else:
            st.error("Vui lòng nhập số phòng.")

elif tab == "Tạo menu đồ ăn/thức uống":
    st.header("Cập nhật menu")
    menu_data = load_data(MENU_FILE)
    item_name = st.text_input("Tên món:")
    item_desc = st.text_input("Miêu tả món:")
    item_price = st.number_input("Giá món:", min_value=0.0)
    uploaded_image = st.file_uploader("Tải lên ảnh món ăn (tùy chọn)", type=["jpg", "png", "jpeg"])
    if st.button("Thêm món"):
        if item_name and item_desc and item_price > 0:
            image_path = ""
            if uploaded_image:
                image_path = os.path.join(IMAGE_DIR, uploaded_image.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_image.read())
            menu_data = pd.concat([menu_data, pd.DataFrame([[item_name, item_desc, item_price, image_path]], columns=['Món ăn', 'Miêu tả', 'Giá', 'Ảnh'])], ignore_index=True)
            save_data(menu_data, MENU_FILE)
            st.success("Thêm món thành công!")
        else:
            st.error("Vui lòng nhập đầy đủ thông tin món ăn.")

elif tab == "Xem menu hiện tại":
    st.header("Menu hiện tại")
    menu_data = load_data(MENU_FILE)
    if menu_data.empty:
        st.info("Chưa có món ăn nào trong menu.")
    else:
        for i, row in menu_data.iterrows():
            st.subheader(row['Món ăn'])
            st.write(f"Miêu tả: {row['Miêu tả']}")
            st.write(f"Giá: {row['Giá']} VND")
            if row['Ảnh']:
                st.image(row['Ảnh'], caption=row['Món ăn'])

elif tab == "Danh sách QR Code đã tạo":
    st.header("Danh sách QR Code đã tạo")
    qr_data = load_data(QR_FILE)

    if qr_data.empty:
        st.info("Chưa có QR Code nào được tạo.")
    else:
        for i, row in qr_data.iterrows():
            st.subheader(f"Phòng: {row['Phòng']}")
            st.write(f"Link: [Đặt hàng tại đây]({row['Link']})")  # Hiện link URL
            qr_image = create_qr_code(row['Link'])  # Tạo lại QR Code từ link
            st.image(qr_image, caption=f"QR Code - Phòng {row['Phòng']}")


elif tab == "Xem danh sách đơn hàng":
    st.header("Danh sách đơn hàng")
    orders_data = load_data(ORDERS_FILE)
    if orders_data.empty:
        st.info("Chưa có đơn hàng nào.")
    else:
        st.dataframe(orders_data)
