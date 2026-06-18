import streamlit as st

# Hàm xử lý logic tính thuế (Tách riêng để code khác biệt và chuyên nghiệp)
def tinh_thue_tncn(thu_nhap_vao, so_nguoi_pt):
    # Các hằng số giảm trừ và bảo hiểm
    GIAM_TRU_BT = 15500000
    GIAM_TRU_PT = so_nguoi_pt * 6200000
    TIEN_BAO_HIEM = thu_nhap_vao * 0.105
    
    tong_giam_tru = GIAM_TRU_BT + GIAM_TRU_PT + TIEN_BAO_HIEM
    thu_nhap_tinh_thue = max(0, thu_nhap_vao - tong_giam_tru)
    
    # Tính thuế lũy tiến bằng mảng cấu trúc (thay cho if-elif dài)
    cac_bac_thue = [
        (80000000, 18150000, 0.35),
        (52000000, 4750000, 0.30),
        (32000000, 1950000, 0.25),
        (18000000, 750000, 0.20),
        (10000000, 250000, 0.15),
        (5000000, 0, 0.10)
    ]
    
    thue_phai_nop = 0
    if thu_nhap_tinh_thue <= 5000000:
        thue_phai_nop = thu_nhap_tinh_thue * 0.05
    else:
        for moc, thue_goc, thue_suat in cac_bac_thue:
            if thu_nhap_tinh_thue > moc:
                thue_phai_nop = thue_goc + (thu_nhap_tinh_thue - moc) * thue_suat
                break
                
    thuc_linh = thu_nhap_vao - TIEN_BAO_HIEM - thue_phai_nop
    
    return {
        "gt_ban_than": GIAM_TRU_BT,
        "gt_phu_thuoc": GIAM_TRU_PT,
        "bh_bat_buoc": TIEN_BAO_HIEM,
        "tn_tinh_thue": thu_nhap_tinh_thue,
        "thue_tncn": thue_phai_nop,
        "thu_nhap_net": thuc_linh
    }

# --- GIAO DIỆN ỨNG DỤNG STREAMLIT ---
st.image("LOGO.jpeg")
st.title("💰 App tính Thuế Thu Nhập Cá Nhân _ Đề Tài 7 _ Nguyễn Thanh Phong")

# Khu vực nhập liệu
luong_truoc_thue = st.number_input(
    "Nhập thu nhập trước thuế (VNĐ)", 
    min_value=0.0, 
    value=20000000.0,
    step=500000.0
)

so_phu_thuoc = st.number_input(
    "Nhập số người phụ thuộc", 
    min_value=0, 
    value=0,
    step=1
)

# Xử lý khi nhấn nút
if st.button("Tính thuế", type="primary"):
    # Gọi hàm tính toán
    kq = tinh_thue_tncn(luong_truoc_thue, so_phu_thuoc)
    
    st.success("Kết quả tính toán chi tiết")
    
    # Hiển thị thông tin cơ bản bằng định dạng text mới
    st.markdown(f"🔹 **Thu nhập trước thuế:** {luong_truoc_thue:,.0f} VNĐ")
    st.markdown(f"🔹 **Giảm trừ bản thân:** {kq['gt_ban_than']:,.0f} VNĐ")
    st.markdown(f"🔹 **Giảm trừ người phụ thuộc:** {kq['gt_phu_thuoc']:,.0f} VNĐ")
    st.markdown(f"🔹 **Bảo hiểm bắt buộc (10.5%):** {kq['bh_bat_buoc']:,.0f} VNĐ")
    st.markdown(f"🔹 **Thu nhập tính thuế:** {kq['tn_tinh_thue']:,.0f} VNĐ")
    
    st.divider() # Vạch kẻ ngang phân cách
    
    # Tạo 2 cột để nhấn mạnh số tiền Thuế và số tiền Thực lĩnh cuối cùng
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🔴 Thuế TNCN phải nộp", value=f"{kq['thue_tncn']:,.0f} VNĐ")
    with col2:
        st.metric(label="🟢 Thu nhập sau thuế (Thực lĩnh)", value=f"{kq['thu_nhap_net']:,.0f} VNĐ")    )

    # Tính thuế lũy tiến từng phần
    tax = 0

    if thu_nhap_tinh_thue <= 5000000:
        tax = thu_nhap_tinh_thue * 0.05

    elif thu_nhap_tinh_thue <= 10000000:
        tax = 250000 + (thu_nhap_tinh_thue - 5000000) * 0.10

    elif thu_nhap_tinh_thue <= 18000000:
        tax = 750000 + (thu_nhap_tinh_thue - 10000000) * 0.15

    elif thu_nhap_tinh_thue <= 32000000:
        tax = 1950000 + (thu_nhap_tinh_thue - 18000000) * 0.20

    elif thu_nhap_tinh_thue <= 52000000:
        tax = 4750000 + (thu_nhap_tinh_thue - 32000000) * 0.25

    elif thu_nhap_tinh_thue <= 80000000:
        tax = 9750000 + (thu_nhap_tinh_thue - 52000000) * 0.30

    else:
        tax = 18150000 + (thu_nhap_tinh_thue - 80000000) * 0.35

    thu_nhap_sau_thue = thu_nhap - bao_hiem - tax

    st.success("Kết quả tính toán")

    st.write(f"📌 Thu nhập trước thuế: **{thu_nhap:,.0f} VNĐ**")
    st.write(f"📌 Giảm trừ bản thân: **{giam_tru_ban_than:,.0f} VNĐ**")
    st.write(f"📌 Giảm trừ người phụ thuộc: **{giam_tru_phu_thuoc:,.0f} VNĐ**")
    st.write(f"📌 Bảo hiểm bắt buộc (10.5%): **{bao_hiem:,.0f} VNĐ**")
    st.write(f"📌 Thu nhập tính thuế: **{thu_nhap_tinh_thue:,.0f} VNĐ**")
    st.write(f"📌 Thuế TNCN phải nộp: **{tax:,.0f} VNĐ**")
    st.write(f"📌 Thu nhập sau thuế: **{thu_nhap_sau_thue:,.0f} VNĐ**")
