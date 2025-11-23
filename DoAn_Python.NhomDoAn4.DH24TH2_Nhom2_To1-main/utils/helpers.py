# ============================================================
# FILE: utils/helpers.py
# MỤC ĐÍCH: Các hàm tiện ích dùng chung cho toàn bộ ứng dụng
# ============================================================

def center_window(window, width, height):
    """
    CĂN GIỮA CỬA SỔ TRÊN MÀN HÌNH
    
    Tham số:
        window: Đối tượng cửa sổ Tkinter
        width: Chiều rộng cửa sổ
        height: Chiều cao cửa sổ
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def format_currency(amount):
    """
    FORMAT SỐ TIỀN THEO CHUẨN VIỆT NAM
    
    Tham số:
        amount: Số tiền (int hoặc float)
    
    Trả về:
        str: Số tiền đã format (vd: "1.234.567 đ")
    """
    try:
        amount = float(amount)
        if amount == 0:
            return "0 đ"
        return f"{amount:,.0f} đ".replace(',', '.')
    except (ValueError, TypeError):
        return "0 đ"


def format_number(number):
    """
    FORMAT SỐ VỚI DẤU PHÂN CÁCH HÀNG NGHÌN
    
    Tham số:
        number: Số cần format
    
    Trả về:
        str: Số đã format (vd: "1,234,567")
    """
    try:
        number = int(number)
        return f"{number:,}"
    except (ValueError, TypeError):
        return "0"


def validate_positive_number(value, field_name="Số"):
    """
    KIỂM TRA SỐ DƯƠNG HỢP LỆ
    
    Tham số:
        value: Giá trị cần kiểm tra
        field_name: Tên trường (để hiển thị lỗi)
    
    Trả về:
        (is_valid, message, parsed_value): 
            - is_valid: True/False
            - message: Thông báo lỗi (nếu có)
            - parsed_value: Giá trị đã parse (hoặc None)
    """
    try:
        num = float(value)
        if num <= 0:
            return False, f"{field_name} phải là số dương!", None
        return True, "", num
    except ValueError:
        return False, f"{field_name} không hợp lệ!", None


def validate_year(year_str):
    """
    KIỂM TRA NĂM HỢP LỆ (1800-2100)
    
    Tham số:
        year_str: Chuỗi năm
    
    Trả về:
        (is_valid, message): True/False và thông báo
    """
    try:
        year = int(year_str)
        if year < 1800 or year > 2100:
            return False, "Năm phải từ 1800 đến 2100!"
        return True, ""
    except ValueError:
        return False, "Năm không hợp lệ!"


def validate_not_empty(value, field_name="Trường"):
    """
    KIỂM TRA TRƯỜNG KHÔNG ĐƯỢC ĐỂ TRỐNG
    
    Tham số:
        value: Giá trị cần kiểm tra
        field_name: Tên trường
    
    Trả về:
        (is_valid, message): True/False và thông báo
    """
    if not value or not value.strip():
        return False, f"{field_name} không được để trống!"
    return True, ""


def get_stock_status(quantity):
    """
    XÁC ĐỊNH TRẠNG THÁI TỒN KHO
    Dựa vào số lượng để phân loại trạng thái
    
    Tham số:
        quantity: Số lượng tồn kho
    
    Trả về:
        (status, color, icon): 
            - status: Trạng thái ("Sắp hết"/"Cảnh báo"/"Tốt")
            - color: Mã màu hex
            - icon: Icon emoji
    """
    try:
        qty = int(quantity)
        if qty < 50:
            return "Sắp hết", "#F44336", "🔴"
        elif qty < 100:
            return "Cảnh báo", "#FF9800", "🟡"
        else:
            return "Tốt", "#4CAF50", "🟢"
    except (ValueError, TypeError):
        return "Không xác định", "#9E9E9E", "⚪"


def truncate_text(text, max_length=50):
    """
    CẮT NGẮN VĂN BẢN
    Thêm "..." nếu vượt quá độ dài
    
    Tham số:
        text: Văn bản cần cắt
        max_length: Độ dài tối đa
    
    Trả về:
        str: Văn bản đã cắt
    """
    if not text:
        return ""
    text = str(text)
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def calculate_profit(gia_mua, gia_ban, so_luong=1):
    """
    TÍNH LỢI NHUẬN
    Công thức: (Giá bán - Giá mua) × Số lượng
    
    Tham số:
        gia_mua: Giá mua vào
        gia_ban: Giá bán ra
        so_luong: Số lượng (mặc định 1)
    
    Trả về:
        float: Lợi nhuận
    """
    try:
        return (float(gia_ban) - float(gia_mua)) * int(so_luong)
    except (ValueError, TypeError):
        return 0.0


def calculate_profit_margin(gia_mua, gia_ban):
    """
    TÍNH TỶ SUẤT LỢI NHUẬN (%)
    Công thức: ((Giá bán - Giá mua) / Giá mua) × 100
    
    Tham số:
        gia_mua: Giá mua vào
        gia_ban: Giá bán ra
    
    Trả về:
        float: Tỷ suất lợi nhuận (%)
    """
    try:
        gia_mua = float(gia_mua)
        gia_ban = float(gia_ban)
        if gia_mua == 0:
            return 0.0
        return ((gia_ban - gia_mua) / gia_mua) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0


def format_phone_number(phone):
    """
    FORMAT SỐ ĐIỆN THOẠI
    Định dạng: 012-345-6789
    
    Tham số:
        phone: Số điện thoại
    
    Trả về:
        str: Số điện thoại đã format
    """
    phone = str(phone).replace(" ", "").replace("-", "")
    if len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone


def validate_email(email):
    """
    KIỂM TRA EMAIL HỢP LỆ
    Sử dụng regex để validate format email
    
    Tham số:
        email: Địa chỉ email
    
    Trả về:
        bool: True nếu hợp lệ
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def get_color_scheme():
    """
    TRẢ VỀ BẢNG MÀU CHUẨN
    Định nghĩa các màu dùng chung trong ứng dụng
    
    Trả về:
        dict: Bảng màu với các key như 'primary', 'success', etc.
    """
    return {
        'primary': '#1976D2',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'danger': '#F44336',
        'info': '#00BCD4',
        'light': '#F5F5F5',
        'dark': '#212121',
        'white': '#FFFFFF',
        'border': '#E0E0E0',
    }


def show_loading_message(parent, message="Đang xử lý..."):
    """
    HIỂN THỊ LOADING MESSAGE
    Tạo label loading để thông báo đang xử lý
    
    Tham số:
        parent: Widget cha
        message: Thông báo
    
    Trả về:
        Label: Widget label (để có thể destroy sau)
    """
    import tkinter as tk
    loading = tk.Label(parent,
        text=f"⏳ {message}",
        font=('Segoe UI', 11),
        bg='#FFF8E1',
        fg='#F57C00',
        padx=20,
        pady=10)
    return loading


def confirm_action(title, message):
    """
    HIỂN THỊ DIALOG XÁC NHẬN
    Hỏi người dùng Yes/No
    
    Tham số:
        title: Tiêu đề dialog
        message: Nội dung
    
    Trả về:
        bool: True nếu chọn Yes
    """
    from tkinter import messagebox
    return messagebox.askyesno(title, message)


def show_success(message):
    """HIỂN THỊ THÔNG BÁO THÀNH CÔNG"""
    from tkinter import messagebox
    messagebox.showinfo("Thành công", f"✅ {message}")


def show_error(message):
    """HIỂN THỊ THÔNG BÁO LỖI"""
    from tkinter import messagebox
    messagebox.showerror("Lỗi", f"❌ {message}")


def show_warning(message):
    """HIỂN THỊ CẢNH BÁO"""
    from tkinter import messagebox
    messagebox.showwarning("Cảnh báo", f"⚠️ {message}")


def show_info(message):
    """HIỂN THỊ THÔNG TIN"""
    from tkinter import messagebox
    messagebox.showinfo("Thông tin", f"ℹ️ {message}")