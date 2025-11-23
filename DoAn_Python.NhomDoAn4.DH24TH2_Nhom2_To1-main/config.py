# ============================================================
# FILE: config.py
# MỤC ĐÍCH: Cấu hình toàn bộ hệ thống (database, bảo mật, giao diện, nghiệp vụ)
# ============================================================

# ================================================================
# CẤU HÌNH DATABASE
# ================================================================
DB_TYPE = "sqlserver"

# ================================================================
# CẤU HÌNH BẢO MẬT
# ================================================================
PASSWORD_MIN_LENGTH = 6
SALT_LENGTH = 32
SESSION_TIMEOUT = 30

# ================================================================
# CẤU HÌNH GIAO DIỆN
# ================================================================
WINDOW_THEME = "clam"

# Bảng màu chuẩn
COLORS = {
    'primary': '#1976D2',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'info': '#00BCD4',
    'purple': '#9C27B0',
    'light': '#F5F5F5',
    'dark': '#212121',
    'white': '#FFFFFF',
    'border': '#E0E0E0',
}

# Cấu hình font
FONT_FAMILY = 'Segoe UI'
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 10
FONT_SIZE_MEDIUM = 11
FONT_SIZE_LARGE = 12
FONT_SIZE_TITLE = 16
FONT_SIZE_HEADER = 18

# ================================================================
# CẤU HÌNH NGHIỆP VỤ
# ================================================================

# Ngưỡng cảnh báo kho hàng
LOW_STOCK_THRESHOLD = 50
CRITICAL_STOCK_THRESHOLD = 20

# Trạng thái đơn hàng
ORDER_STATUSES = ["Đang xử lý", "Hoàn thành", "Đã hủy"]
DEFAULT_ORDER_STATUS = "Đang xử lý"

# Vị trí kho
DEFAULT_LOCATIONS = [
    "Kệ A1", "Kệ A2", 
    "Kệ B1", "Kệ B2", 
    "Kệ C1", "Kệ C2", "Kệ C3",
    "Kệ D1", "Kệ D2", "Kệ D3", "Kệ D4"
]

# Loại sách
BOOK_TYPES = ["Sách Nước Ngoài", "Sách Trong Nước"]

# ================================================================
# CẤU HÌNH LOGGING & DEBUG
# ================================================================
DEBUG_MODE = True
LOG_LEVEL = "INFO"

# ================================================================
# CẤU HÌNH HIỂN THỊ
# ================================================================
DEFAULT_TREE_HEIGHT = 15
RECORDS_PER_PAGE = 50

# ================================================================
# THÔNG TIN ỨNG DỤNG
# ================================================================
APP_NAME = "Hệ Thống Quản Lý Sách"
APP_VERSION = "2.0"
APP_AUTHOR = "Development Team"

WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# ================================================================
# CẤU HÌNH BÁO CÁO & EXPORT
# ================================================================
EXPORT_FORMATS = ["Excel", "PDF", "CSV"]

REPORT_TYPES = [
    "Báo cáo tồn kho",
    "Báo cáo doanh thu",
    "Báo cáo nhập xuất",
    "Báo cáo sách bán chạy"
]

# ================================================================
# CẤU HÌNH EMAIL (TÙY CHỌN - CHO TÍNH NĂNG TƯƠNG LAI)
# ================================================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USE_TLS = True
SMTP_USERNAME = ""
SMTP_PASSWORD = ""

# ================================================================
# CẤU HÌNH BACKUP (TÙY CHỌN)
# ================================================================
AUTO_BACKUP = False
BACKUP_INTERVAL_DAYS = 7
BACKUP_PATH = "./backups/"