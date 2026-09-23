import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ================= 1. CẤU HÌNH TRANG VÀ BIẾN MẶC ĐỊNH =================
st.set_page_config(page_title="Sơ Đồ Lớp Học", layout="wide", page_icon="🏫")

MAT_KHAU_QUAN_TRI = "admin123"
NGAY_BAT_DAU = datetime(2026, 9, 23)
FILE_DATA = "danh_sach_lop.csv"

# ================= 2. KHỞI TẠO DỮ LIỆU =================
def tao_du_lieu_mau():
    danh_sach = []
    id_hs = 1
    for day in range(1, 5):         
        for hang in range(1, 7):    
            for cho in [1, 2]:      
                if id_hs <= 45:
                    ten = f"Học sinh {id_hs}"
                    avt = f"https://api.dicebear.com/7.x/avataaars/svg?seed={id_hs}"
                else:
                    ten = "Ghế Trống"
                    avt = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"
                danh_sach.append({
                    "Ten": ten, "Day_Doc": day, "Hang_Ngang": hang,
                    "Cho_Ngoi": cho, "Avatar_URL": avt
                })
                id_hs += 1
    return pd.DataFrame(danh_sach)

if os.path.exists(FILE_DATA):
    df = pd.read_csv(FILE_DATA)
else:
    df = tao_du_lieu_mau()
    df.to_csv(FILE_DATA, index=False)

# ================= 3. THUẬT TOÁN ĐỔI CHỖ =================
hom_nay = datetime.now()
so_lan_doi = (hom_nay - NGAY_BAT_DAU).days // 14
df_hien_tai = df.copy()

if so_lan_doi > 0:
    # Hàng 6 tiến lên Hàng 1, các hàng khác lùi xuống
    df_hien_tai['Hang_Ngang'] = (df_hien_tai['Hang_Ngang'] + so_lan_doi - 1) % 6 + 1

# ================= 4. GIAO DIỆN WEB =================
st.title("🏫 SƠ ĐỒ LỚP HỌC (45 THÀNH VIÊN)")
st.caption(f"📅 Trạng thái: Đã tự động đổi chỗ **{so_lan_doi}** lần. (Hàng cuối lên bục giảng, các hàng khác lùi 1 bước)")
st.write("---")

tab_sodo, tab_quanly = st.tabs(["🗺️ Hiển thị Sơ đồ Lớp", "⚙️ Quản lý & Chỉnh sửa"])

# ----------------- TAB 1: HIỂN THỊ SƠ ĐỒ -----------------
with tab_sodo:
    st.markdown("BỤC GIẢNG / BÀN GIÁO VIÊN", unsafe_allow_html=True)

# Hàm vẽ 1 cụm 4 học sinh (đã thay bằng use_container_width)
def ve_cum_4_hoc_sinh(hs_day_a, hs_day_b, title):
    with st.container(border=True):
        st.markdown(f"{title}", unsafe_allow_html=True)

        # CHIA LÀM 5 CỘT: 2 chỗ Bàn 1 -- khoảng hở nhỏ -- 2 chỗ Bàn 2
        c1, c2, gap, c3, c4 = st.columns([1, 1, 0.3, 1, 1])
        
        def get_hs(hs_list, cho):
            hs = next((x for x in hs_list if x['Cho_Ngoi'] == cho), None)
            if hs and hs['Ten'] != "Ghế Trống":
                return hs['Ten'], hs['Avatar_URL']
            return "Trống", "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"

        t1, a1 = get_hs(hs_day_a, 1)
        t2, a2 = get_hs(hs_day_a, 2)
        t3, a3 = get_hs(hs_day_b, 1)
        t4, a4 = get_hs(hs_day_b, 2)

        # ----- BÀN 1 (Bên Trái Cụm) -----
        with c1:
            st.image(a1, use_container_width=True)
            st.caption(f"**{t1}**")
        with c2:
            st.image(a2, use_container_width=True)
            st.caption(f"**{t2}**")
            
        # Cột 'gap' ở giữa bị bỏ trống để tạo ranh giới 2 cái bàn
        
        # ----- BÀN 2 (Bên Phải Cụm) -----
        with c3:
            st.image(a3, use_container_width=True)
            st.caption(f"**{t3}**")
        with c4:
            st.image(a4, use_container_width=True)
            st.caption(f"**{t4}**")

# In ra sơ đồ theo từng hàng ngang (1 đến 6)
for h in range(1, 7):
    # Chia lớp thành 2 Cụm Lớn (Trái và Phải)
    col_trai, col_phai = st.columns(2)
    hs_hang = df_hien_tai[df_hien_tai['Hang_Ngang'] == h]
    
    with col_trai:
        # Gộp Dãy 1 và Dãy 2 thành CỤM TRÁI
        hs_d1 = hs_hang[hs_hang['Day_Doc'] == 1].to_dict('records')
        hs_d2 = hs_hang[hs_hang['Day_Doc'] == 2].to_dict('records')
        ve_cum_4_hoc_sinh(hs_d1, hs_d2, f"HÀNG {h} - CỤM TRÁI")
        
    with col_phai:
        # Gộp Dãy 3 và Dãy 4 thành CỤM PHẢI
        hs_d3 = hs_hang[hs_hang['Day_Doc'] == 3].to_dict('records')
        hs_d4 = hs_hang[hs_hang['Day_Doc'] == 4].to_dict('records')
        ve_cum_4_hoc_sinh(hs_d3, hs_d4, f"HÀNG {h} - CỤM PHẢI")
# ----------------- TAB 2: QUẢN LÝ -----------------

mk = st.text_input("🔑 Nhập mật khẩu quản trị:", type="password")

if mk == MAT_KHAU_QUAN_TRI:
    st.success("✅ Đã mở khóa chỉnh sửa!")
    df_moi = st.data_editor(
        df,
        column_config={
            "Ten": st.column_config.TextColumn("👤 Tên Học Sinh", width="medium"),
            "Day_Doc": st.column_config.NumberColumn("🏢 Dãy dọc (1-4)", min_value=1, max_value=4),
            "Hang_Ngang": st.column_config.NumberColumn("🪑 Hàng/Bàn (1-6)", min_value=1, max_value=6),
            "Cho_Ngoi": st.column_config.NumberColumn("Vị trí (1=Trái, 2=Phải)", min_value=1, max_value=2),
            "Avatar_URL": st.column_config.TextColumn("🖼️ Link Avatar", width="large"),
        },
        hide_index=True, num_rows="fixed", height=600
    )
    if st.button("💾 LƯU MỌI THAY ĐỔI"):
        df_moi.to_csv(FILE_DATA, index=False)
        st.success("🎉 Đã lưu! Hãy làm mới trang web (nhấn phím F5) để xem sơ đồ mới.")
elif mk != "":
    st.error("❌ Sai mật khẩu!")