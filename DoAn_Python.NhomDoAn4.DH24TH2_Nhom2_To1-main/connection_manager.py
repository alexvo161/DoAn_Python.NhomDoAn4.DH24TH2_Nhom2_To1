# ============================================================
# FILE: connection_manager.py
# MỤC ĐÍCH: Quản lý kết nối đến SQL Server Database
# ============================================================

import pyodbc

# ================================================================
# THÔNG TIN KẾT NỐI SQL SERVER
# ================================================================
SERVER_NAME = r'LAPTOP-H1KTCC7N'
DATABASE_NAME = 'QuanLySach'
DRIVER = '{ODBC Driver 17 for SQL Server}'

def getDbConnection(user=None, password=None):
    """
    TẠO VÀ TRẢ VỀ KẾT NỐI SQL SERVER
    
    Chức năng:
        - Hỗ trợ Windows Authentication (mặc định)
        - Hỗ trợ SQL Server Authentication (nếu có user/password)
        - Tắt autocommit để sử dụng transaction
        - Hỗ trợ UTF-8 cho tiếng Việt
    
    Tham số:
        user: Username SQL Server (tùy chọn)
        password: Password SQL Server (tùy chọn)
    
    Trả về:
        Connection object hoặc None nếu lỗi
    """
    try:
        utf8_setting = 'CharacterSet=UTF-8;'
        
        if user and password:
            # SQL Server Authentication
            conn_string = (
                f'DRIVER={DRIVER};'
                f'SERVER={SERVER_NAME};'
                f'DATABASE={DATABASE_NAME};'
                f'UID={user};'
                f'PWD={password};'
                f'{utf8_setting}'
            )
        else:
            # Windows Authentication
            conn_string = (
                f'DRIVER={DRIVER};'
                f'SERVER={SERVER_NAME};'
                f'DATABASE={DATABASE_NAME};'
                'Trusted_Connection=yes;'
                f'{utf8_setting}'
            )
        
        # Tạo kết nối
        conn = pyodbc.connect(conn_string)
        
        # Tắt autocommit để có thể rollback khi cần
        conn.autocommit = False
        
        print("✅ Kết nối SQL Server thành công!")
        return conn
        
    except Exception as e:
        print(f"❌ Lỗi kết nối CSDL SQL Server: {e}")
        return None