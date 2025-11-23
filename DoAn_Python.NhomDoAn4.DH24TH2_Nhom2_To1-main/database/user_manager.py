#=============================================================
# FILE: database/user_manager.py
# MỤC ĐÍCH: Quản lý người dùng (đăng ký, đăng nhập, xác thực)
# ============================================================

import hashlib
import os
import sys
from pathlib import Path

# Thêm đường dẫn để import connection_manager
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from connection_manager import getDbConnection

class UserManager:
    """
    CLASS QUẢN LÝ NGƯỜI DÙNG
    - Đăng ký tài khoản mới
    - Đăng nhập và xác thực
    - Đổi mật khẩu
    - Quản lý trạng thái tài khoản (khóa/mở khóa)
    """
    
    def __init__(self):
        """Khởi tạo UserManager và kiểm tra kết nối database"""
        self.PASSWORD_MIN_LENGTH = 6
        self.SALT_LENGTH = 32
        
        conn = self.get_connection()
        if conn:
            print("✅ UserManager: Kết nối SQL Server thành công")
            conn.close()
        else:
            print("⚠️  UserManager: Không thể kết nối SQL Server")
    
    def get_connection(self):
        """Lấy kết nối database từ connection_manager"""
        try:
            return getDbConnection()
        except Exception as e:
            print(f"❌ Lỗi kết nối database: {e}")
            return None
    
    def hash_password(self, password, salt=None):
        """
        MÃ HÓA MẬT KHẨU
        Sử dụng SHA-256 với salt để bảo mật
        
        Tham số:
            password: Mật khẩu gốc
            salt: Chuỗi salt (tự động tạo nếu None)
        
        Trả về:
            (password_hash, salt): Hash và salt đã mã hóa
        """
        if salt is None:
            salt = os.urandom(self.SALT_LENGTH).hex()
        
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt
    
    def register_user(self, username, password, full_name="", email="", role="user"):
        """
        ĐĂNG KÝ TÀI KHOẢN MỚI
        
        Tham số:
            username: Tên đăng nhập
            password: Mật khẩu
            full_name: Họ tên đầy đủ
            email: Email
            role: Vai trò (user/admin)
        
        Trả về:
            (success, message): True/False và thông báo
        """
        # Kiểm tra độ dài mật khẩu
        if len(password) < self.PASSWORD_MIN_LENGTH:
            return False, f"Mật khẩu phải có ít nhất {self.PASSWORD_MIN_LENGTH} ký tự"
        
        # Kiểm tra username không rỗng
        if not username or not username.strip():
            return False, "Tên đăng nhập không được để trống"
        
        conn = self.get_connection()
        if not conn:
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = conn.cursor()
            
            # Kiểm tra username đã tồn tại
            cursor.execute("SELECT Id FROM Users WHERE Username = ?", (username,))
            if cursor.fetchone():
                return False, "Tên đăng nhập đã tồn tại"
            
            # Mã hóa mật khẩu
            password_hash, salt = self.hash_password(password)
            
            # Tạo user mới qua Stored Procedure
            cursor.execute("""
                EXEC sp_CreateUser 
                    @Username = ?, 
                    @PasswordHash = ?, 
                    @Salt = ?,
                    @FullName = ?,
                    @Email = ?,
                    @Role = ?
            """, (username, password_hash, salt, full_name if full_name else username, email, role))
            
            result = cursor.fetchone()
            
            if result and result[0] == 1:
                conn.commit()
                print(f"✅ Đã đăng ký user: {username}")
                return True, "Đăng ký thành công"
            else:
                message = result[1] if result else "Lỗi không xác định"
                return False, message
        
        except Exception as e:
            print(f"❌ Lỗi đăng ký: {e}")
            return False, f"Lỗi: {str(e)}"
        
        finally:
            if conn:
                conn.close()
    
    def login(self, username, password):
        """
        ĐĂNG NHẬP HỆ THỐNG
        Xác thực thông tin đăng nhập và trả về thông tin user
        
        Tham số:
            username: Tên đăng nhập
            password: Mật khẩu
        
        Trả về:
            (success, result): 
                - success=True: result là dict chứa thông tin user
                - success=False: result là thông báo lỗi
        """
        conn = self.get_connection()
        if not conn:
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = conn.cursor()
            
            # Lấy thông tin user từ database
            cursor.execute("EXEC sp_GetUserByUsername @Username = ?", (username,))
            result = cursor.fetchone()
            
            if result is None:
                return False, "Tên đăng nhập không tồn tại"
            
            # Parse kết quả
            user_id = result[0]
            stored_username = result[1]
            stored_hash = result[2]
            salt = result[3]
            full_name = result[4] if result[4] else username
            email = result[5]
            role = result[6]
            created_at = result[7]
            last_login = result[8]
            is_active = result[9]
            
            # Kiểm tra tài khoản có bị khóa
            if not is_active:
                return False, "Tài khoản đã bị khóa"
            
            # Xác thực mật khẩu
            password_hash, _ = self.hash_password(password, salt)
            
            if password_hash == stored_hash:
                # Cập nhật thời gian đăng nhập
                cursor.execute("EXEC sp_UpdateLastLogin @UserId = ?", (user_id,))
                conn.commit()
                
                print(f"✅ Đăng nhập thành công: {username} ({role})")
                
                # Trả về thông tin user
                return True, {
                    "user_id": user_id,
                    "username": stored_username,
                    "full_name": full_name,
                    "email": email,
                    "role": role,
                    "created_at": created_at,
                    "last_login": last_login
                }
            else:
                return False, "Mật khẩu không đúng"
        
        except Exception as e:
            print(f"❌ Lỗi đăng nhập: {e}")
            return False, f"Lỗi đăng nhập: {str(e)}"
        
        finally:
            if conn:
                conn.close()
    
    def check_username_exists(self, username):
        """
        KIỂM TRA USERNAME ĐÃ TỒN TẠI
        
        Tham số:
            username: Tên đăng nhập cần kiểm tra
        
        Trả về:
            bool: True nếu đã tồn tại
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT Id FROM Users WHERE Username = ?', (username,))
            result = cursor.fetchone()
            return result is not None
        
        except Exception as e:
            print(f"❌ Lỗi check username: {e}")
            return False
        
        finally:
            if conn:
                conn.close()
    
    def change_password(self, username, old_password, new_password):
        """
        ĐỔI MẬT KHẨU
        
        Tham số:
            username: Tên đăng nhập
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới
        
        Trả về:
            (success, message): True/False và thông báo
        """
        # Xác thực mật khẩu cũ
        success, result = self.login(username, old_password)
        if not success:
            return False, "Mật khẩu cũ không đúng"
        
        # Kiểm tra độ dài mật khẩu mới
        if len(new_password) < self.PASSWORD_MIN_LENGTH:
            return False, f"Mật khẩu mới phải có ít nhất {self.PASSWORD_MIN_LENGTH} ký tự"
        
        conn = self.get_connection()
        if not conn:
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = conn.cursor()
            
            # Tạo hash mới
            password_hash, salt = self.hash_password(new_password)
            
            # Cập nhật mật khẩu trong database
            cursor.execute("""
                UPDATE Users 
                SET PasswordHash = ?, Salt = ?
                WHERE Username = ?
            """, (password_hash, salt, username))
            
            conn.commit()
            print(f"✅ Đã đổi mật khẩu cho user: {username}")
            return True, "Đổi mật khẩu thành công"
        
        except Exception as e:
            print(f"❌ Lỗi đổi mật khẩu: {e}")
            return False, f"Lỗi: {str(e)}"
        
        finally:
            if conn:
                conn.close()
    
    def get_all_users(self):
        """
        LẤY DANH SÁCH TẤT CẢ USER (CHO ADMIN)
        
        Trả về:
            list: Danh sách users
        """
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    Id, Username, FullName, Email, Role, 
                    CreatedAt, LastLogin, IsActive
                FROM Users
                ORDER BY CreatedAt DESC
            """)
            
            users = cursor.fetchall()
            return users
        
        except Exception as e:
            print(f"❌ Lỗi get all users: {e}")
            return []
        
        finally:
            if conn:
                conn.close()
    
    def deactivate_user(self, user_id):
        """
        KHÓA TÀI KHOẢN USER
        
        Tham số:
            user_id: ID của user
        
        Trả về:
            (success, message): True/False và thông báo
        """
        conn = self.get_connection()
        if not conn:
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Users SET IsActive = 0 WHERE Id = ?", (user_id,))
            conn.commit()
            
            return True, "Đã khóa tài khoản"
        
        except Exception as e:
            print(f"❌ Lỗi deactivate user: {e}")
            return False, f"Lỗi: {str(e)}"
        
        finally:
            if conn:
                conn.close()
    
    def activate_user(self, user_id):
        """
        MỞ KHÓA TÀI KHOẢN USER
        
        Tham số:
            user_id: ID của user
        
        Trả về:
            (success, message): True/False và thông báo
        """
        conn = self.get_connection()
        if not conn:
            return False, "Không thể kết nối đến database"
        
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Users SET IsActive = 1 WHERE Id = ?", (user_id,))
            conn.commit()
            
            return True, "Đã mở khóa tài khoản"
        
        except Exception as e:
            print(f"❌ Lỗi activate user: {e}")
            return False, f"Lỗi: {str(e)}"
        
        finally:
            if conn:
                conn.close()