# ============================================================
# FILE: database/book_database.py
# MỤC ĐÍCH: Quản lý tất cả thao tác CSDL với SQL Server
# ============================================================

import time
from datetime import datetime

# ============================================================
# CLASS: DatabaseManager:
# ============================================================
class DatabaseManager:
    """
    Quản lý dữ liệu sách với SQL SERVER - Phiên bản đã sửa lỗi.
    
    ✅ Tất cả thao tác LƯU THẬT vào SQL Server
    ✅ Đã sửa lỗi commit/rollback với autocommit=False
    ✅ Xử lý đúng stored procedures
    """
    
    # KHỞI TẠO
    def __init__(self, conn):
        """Khởi tạo với SQL Server connection"""
        self.conn = conn
        self.cursor = conn.cursor() if conn else None
        
        if not self.cursor:
            print("⚠️  WARNING: Không có kết nối database!")
    
    # ============================================================
    # BOOK INFO OPERATIONS
    # ============================================================
    
    # METHOD: VIEW_ALL
    def view_all(self):
        """Xem tất cả sách từ SQL Server"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return []
        
        try:
            query = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia,
                    ISNULL(lv.TenLinhVuc, N'') AS TenLinhVuc,
                    ISNULL(s.LoaiSach, N'') AS LoaiSach,
                    ISNULL(nxb.TenNXB, N'') AS TenNXB,
                    ISNULL(s.GiaMua, 0) AS GiaMua,
                    ISNULL(s.GiaBia, 0) AS GiaBia,
                    ISNULL(s.LanTaiBan, 0) AS LanTaiBan,
                    ISNULL(s.NamXB, '') AS NamXB
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                LEFT JOIN LinhVuc lv ON s.IdLinhVuc = lv.Id
                LEFT JOIN NhaXuatBan nxb ON s.IdNhaXuatBan = nxb.Id
                ORDER BY s.Id
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            # Convert to list of lists
            result = []
            for row in rows:
                result.append([
                    row[0],  # Id
                    row[1],  # MaSach
                    row[2],  # TenSach
                    row[3],  # TenTacGia
                    row[4],  # TenLinhVuc
                    row[5],  # LoaiSach
                    row[6],  # TenNXB
                    float(row[7]),  # GiaMua
                    float(row[8]),  # GiaBia
                    int(row[9]),    # LanTaiBan
                    str(row[10])    # NamXB
                ])
            
            print(f"✅ Đã tải {len(result)} sách từ database")
            return result
            
        except Exception as e:
            print(f"❌ Lỗi view_all: {e}")
            return []
    
    # METHOD: SEARCH_FOR_SUGGESTION
    def search_for_suggestion(self, query):
        """Tìm kiếm sách (autocomplete)"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                WHERE s.MaSach LIKE ? 
                   OR s.TenSach LIKE ? 
                   OR tg.TenTacGia LIKE ?
                ORDER BY s.Id
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term, search_term))
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                result.append([row[0], row[1], row[2], row[3]])
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search: {e}")
            return []
    
    # METHOD: SEARCH_BOOK
    def search_book(self, query):
        """Tìm kiếm sách (đầy đủ thông tin)"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia,
                    ISNULL(lv.TenLinhVuc, N'') AS TenLinhVuc,
                    ISNULL(s.LoaiSach, N'') AS LoaiSach,
                    ISNULL(nxb.TenNXB, N'') AS TenNXB,
                    ISNULL(s.GiaMua, 0) AS GiaMua,
                    ISNULL(s.GiaBia, 0) AS GiaBia,
                    ISNULL(s.LanTaiBan, 0) AS LanTaiBan,
                    ISNULL(s.NamXB, '') AS NamXB
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                LEFT JOIN LinhVuc lv ON s.IdLinhVuc = lv.Id
                LEFT JOIN NhaXuatBan nxb ON s.IdNhaXuatBan = nxb.Id
                WHERE s.MaSach LIKE ? 
                   OR s.TenSach LIKE ? 
                   OR tg.TenTacGia LIKE ?
                ORDER BY s.Id
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term, search_term))
            rows = self.cursor.fetchall()
            
            result = []
            for row in rows:
                result.append([
                    row[0],  # Id
                    row[1],  # MaSach
                    row[2],  # TenSach
                    row[3],  # TenTacGia
                    row[4],  # TenLinhVuc
                    row[5],  # LoaiSach
                    row[6],  # TenNXB
                    float(row[7]),  # GiaMua
                    float(row[8]),  # GiaBia
                    int(row[9]),    # LanTaiBan
                    str(row[10])    # NamXB
                ])
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search_book: {e}")
            return []
    
    # METHOD: GET_BOOK_BY_ID
    def get_book_by_id(self, book_id):
        """Lấy thông tin sách theo ID"""
        if not self.cursor:
            return None
        
        try:
            query = """
                SELECT 
                    s.Id, s.MaSach, s.TenSach,
                    ISNULL(tg.TenTacGia, N'') AS TenTacGia,
                    ISNULL(lv.TenLinhVuc, N'') AS TenLinhVuc,
                    ISNULL(s.LoaiSach, N'') AS LoaiSach,
                    ISNULL(nxb.TenNXB, N'') AS TenNXB,
                    ISNULL(s.GiaMua, 0) AS GiaMua,
                    ISNULL(s.GiaBia, 0) AS GiaBia,
                    ISNULL(s.LanTaiBan, 0) AS LanTaiBan,
                    ISNULL(s.NamXB, '') AS NamXB
                FROM Sach s
                LEFT JOIN TacGia tg ON s.IdTacGia = tg.Id
                LEFT JOIN LinhVuc lv ON s.IdLinhVuc = lv.Id
                LEFT JOIN NhaXuatBan nxb ON s.IdNhaXuatBan = nxb.Id
                WHERE s.Id = ?
            """
            self.cursor.execute(query, (book_id,))
            row = self.cursor.fetchone()
            
            if row:
                return [
                    row[0], row[1], row[2], row[3], row[4],
                    row[5], row[6], float(row[7]), float(row[8]),
                    int(row[9]), str(row[10])
                ]
            return None
            
        except Exception as e:
            print(f"❌ Lỗi get_book_by_id: {e}")
            return None
    
    # METHOD: GET_INVENTORY_STATS
    def get_inventory_stats(self):
        """Thống kê sách"""
        if not self.cursor:
            return {'TotalCount': 0, 'TotalQuantity': 0, 'LowStockCount': 0, 'TotalValue': 0}
        
        try:
            # Tổng số sách
            self.cursor.execute("SELECT COUNT(*) FROM Sach")
            total_count = self.cursor.fetchone()[0]
            
            # Tổng tồn kho
            self.cursor.execute("SELECT ISNULL(SUM(SoLuongTon), 0) FROM TonKho")
            total_quantity = self.cursor.fetchone()[0]
            
            # Sách sắp hết (< 50)
            self.cursor.execute("SELECT COUNT(*) FROM TonKho WHERE SoLuongTon < 50")
            low_stock = self.cursor.fetchone()[0]
            
            # Giá trị kho
            self.cursor.execute("""
                SELECT ISNULL(SUM(tk.SoLuongTon * s.GiaMua), 0)
                FROM TonKho tk
                JOIN Sach s ON tk.IdSach = s.Id
            """)
            total_value = self.cursor.fetchone()[0]
            
            return {
                'TotalCount': total_count,
                'TotalQuantity': int(total_quantity),
                'LowStockCount': low_stock,
                'TotalValue': float(total_value)
            }
            
        except Exception as e:
            print(f"❌ Lỗi stats: {e}")
            return {'TotalCount': 0, 'TotalQuantity': 0, 'LowStockCount': 0, 'TotalValue': 0}
    
    def _get_or_create_id(self, table, name_column, name_value):
        """Helper: Lấy hoặc tạo ID cho bảng phụ"""
        if not name_value or not name_value.strip():
            return None
        
        try:
            # Tìm xem đã tồn tại chưa
            self.cursor.execute(f"SELECT Id FROM {table} WHERE {name_column} = ?", (name_value,))
            row = self.cursor.fetchone()
            
            if row:
                return row[0]
            
            # Chưa có → Thêm mới
            self.cursor.execute(f"INSERT INTO {table} ({name_column}) VALUES (?)", (name_value,))
            
            # ✅ SỬA: Commit sau mỗi insert vào bảng phụ
            self.conn.commit()
            
            # Lấy ID vừa insert
            self.cursor.execute("SELECT @@IDENTITY")
            new_id = int(self.cursor.fetchone()[0])
            print(f"   ➕ Đã tạo {table}: {name_value} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            print(f"❌ Lỗi _get_or_create_id [{table}]: {e}")
            self.conn.rollback()
            return None
    
    # METHOD: INSERT_BOOK_FULL
    def insert_book_full(self, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, lan_tai_ban,
                         nam_xb):
        """Thêm sách mới vào SQL Server"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return None
        
        try:
            # Lấy/Tạo ID cho các bảng phụ
            id_tac_gia = self._get_or_create_id('TacGia', 'TenTacGia', tac_gia)
            id_linh_vuc = self._get_or_create_id('LinhVuc', 'TenLinhVuc', linh_vuc)
            id_nxb = self._get_or_create_id('NhaXuatBan', 'TenNXB', nxb)
            
            # Insert sách
            query = """
                INSERT INTO Sach (MaSach, TenSach, IdTacGia, IdLinhVuc, IdNhaXuatBan, 
                                  LoaiSach, GiaMua, GiaBia, LanTaiBan, NamXB)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                ma_sach, ten_sach, id_tac_gia, id_linh_vuc, id_nxb,
                loai_sach, float(gia_mua), float(gia_bia), int(lan_tai_ban), nam_xb
            ))
            
            # Lấy ID vừa insert
            self.cursor.execute("SELECT @@IDENTITY")
            new_id = int(self.cursor.fetchone()[0])
            
            # Tự động tạo dòng tồn kho
            self.cursor.execute("""
                INSERT INTO TonKho (IdSach, SoLuongTon, ViTri)
                VALUES (?, 0, N'Chưa xác định')
            """, (new_id,))
            
            # ✅ SỬA: Commit transaction
            self.conn.commit()
            
            print(f"✅ Thêm sách mới ID {new_id}: {ma_sach} - {ten_sach}")
            return new_id
            
        except Exception as e:
            print(f"❌ Lỗi insert_book: {e}")
            # ✅ SỬA: Rollback khi có lỗi
            self.conn.rollback()
            return None
    
    # METHOD: UPDATE_BOOK_FULL
    def update_book_full(self, book_id, ma_sach, ten_sach, tac_gia, linh_vuc, loai_sach, nxb, gia_mua, gia_bia, 
                         lan_tai_ban, nam_xb):
        """Cập nhật thông tin sách"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return False
        
        try:
            # Lấy/Tạo ID cho các bảng phụ
            id_tac_gia = self._get_or_create_id('TacGia', 'TenTacGia', tac_gia)
            id_linh_vuc = self._get_or_create_id('LinhVuc', 'TenLinhVuc', linh_vuc)
            id_nxb = self._get_or_create_id('NhaXuatBan', 'TenNXB', nxb)
            
            # Update sách
            query = """
                UPDATE Sach 
                SET MaSach = ?, TenSach = ?, IdTacGia = ?, IdLinhVuc = ?, 
                    IdNhaXuatBan = ?, LoaiSach = ?, GiaMua = ?, GiaBia = ?, 
                    LanTaiBan = ?, NamXB = ?, NgayCapNhat = GETDATE()
                WHERE Id = ?
            """
            self.cursor.execute(query, (
                ma_sach, ten_sach, id_tac_gia, id_linh_vuc, id_nxb,
                loai_sach, float(gia_mua), float(gia_bia), int(lan_tai_ban), nam_xb,
                book_id
            ))
            
            # ✅ SỬA: Commit transaction
            self.conn.commit()
            
            print(f"✅ Cập nhật sách ID {book_id} thành công!")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi update_book: {e}")
            # ✅ SỬA: Rollback khi có lỗi
            self.conn.rollback()
            return False
    
    # METHOD: DELETE_BOOK
    def delete_book(self, book_id):
        """Xóa sách (CASCADE delete tồn kho tự động)"""
        if not self.cursor:
            print("❌ Không có kết nối database!")
            return False
        
        try:
            query = "DELETE FROM Sach WHERE Id = ?"
            self.cursor.execute(query, (book_id,))
            
            # ✅ SỬA: Commit transaction
            self.conn.commit()
            
            print(f"✅ Xóa sách ID {book_id} thành công!")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi delete_book: {e}")
            # ✅ SỬA: Rollback khi có lỗi
            self.conn.rollback()
            return False
    
    # ============================================================
    # INVENTORY OPERATIONS
    # ============================================================
    
    # METHOD: VIEW_INVENTORY
    def view_inventory(self):
        """Xem tồn kho"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    tk.IdSach,
                    s.MaSach,
                    s.TenSach,
                    tk.SoLuongTon,
                    ISNULL(tk.ViTri, N'Chưa xác định') AS ViTri
                FROM TonKho tk
                JOIN Sach s ON tk.IdSach = s.Id
                ORDER BY s.MaSach
            """
            self.cursor.execute(query)
            
            result = []
            for row in self.cursor.fetchall():
                result.append((row[0], row[1], row[2], row[3], row[4]))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi view_inventory: {e}")
            return []
    
    # METHOD: SEARCH_INVENTORY_FOR_SUGGESTION
    def search_inventory_for_suggestion(self, query):
        """Tìm kiếm trong kho"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    tk.IdSach, s.MaSach, s.TenSach, tk.SoLuongTon,
                    ISNULL(tk.ViTri, N'') AS ViTri
                FROM TonKho tk
                JOIN Sach s ON tk.IdSach = s.Id
                WHERE s.MaSach LIKE ? OR s.TenSach LIKE ?
                ORDER BY s.MaSach
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term))
            
            result = []
            for row in self.cursor.fetchall():
                result.append((row[0], row[1], row[2], row[3], row[4]))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search_inventory: {e}")
            return []
    
    # METHOD: ADD_STOCK
    def add_stock(self, book_id, quantity, note=""):
        """Nhập kho sử dụng stored procedure"""
        if not self.cursor:
            return False
        
        try:
            # ✅ SỬA: Gọi stored procedure
            self.cursor.execute("""
                EXEC sp_NhapKho 
                    @IdSach = ?, 
                    @SoLuong = ?, 
                    @NguoiThucHien = N'System',
                    @GhiChu = ?
            """, (book_id, quantity, note))
            
            # ✅ SỬA: Lấy kết quả từ SP (nếu có)
            try:
                result = self.cursor.fetchone()
                if result and result[0] == 1:
                    # SP trả về Success = 1
                    self.conn.commit()
                    print(f"✅ Nhập kho: +{quantity} quyển cho sách ID {book_id}")
                    return True
                else:
                    # SP trả về Success = 0 hoặc lỗi
                    message = result[1] if result and len(result) > 1 else "Lỗi không xác định"
                    print(f"❌ Nhập kho thất bại: {message}")
                    self.conn.rollback()
                    return False
            except:
                # Không có result set - commit luôn
                self.conn.commit()
                print(f"✅ Nhập kho: +{quantity} quyển cho sách ID {book_id}")
                return True
                
        except Exception as e:
            print(f"❌ Lỗi add_stock: {e}")
            self.conn.rollback()
            return False
    
    # METHOD: REMOVE_STOCK
    def remove_stock(self, book_id, quantity, note=""):
        """Xuất kho sử dụng stored procedure"""
        if not self.cursor:
            return False
        
        try:
            # ✅ SỬA: Gọi stored procedure
            self.cursor.execute("""
                EXEC sp_XuatKho 
                    @IdSach = ?, 
                    @SoLuong = ?, 
                    @NguoiThucHien = N'System',
                    @GhiChu = ?
            """, (book_id, quantity, note))
            
            # ✅ SỬA: Lấy kết quả từ SP
            try:
                result = self.cursor.fetchone()
                if result and result[0] == 1:
                    # SP trả về Success = 1
                    self.conn.commit()
                    print(f"✅ Xuất kho: -{quantity} quyển cho sách ID {book_id}")
                    return True
                else:
                    # SP trả về Success = 0 hoặc lỗi
                    message = result[1] if result and len(result) > 1 else "Không đủ hàng tồn kho"
                    print(f"❌ Xuất kho thất bại: {message}")
                    self.conn.rollback()
                    return False
            except:
                # Không có result set - commit luôn
                self.conn.commit()
                print(f"✅ Xuất kho: -{quantity} quyển cho sách ID {book_id}")
                return True
                
        except Exception as e:
            print(f"❌ Lỗi remove_stock: {e}")
            self.conn.rollback()
            return False
    
    # METHOD: UPDATE_INVENTORY
    def update_inventory(self, book_id, new_quantity, new_location):
        """Cập nhật tồn kho thủ công"""
        if not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                UPDATE TonKho 
                SET SoLuongTon = ?, ViTri = ?, NgayCapNhat = GETDATE()
                WHERE IdSach = ?
            """, (new_quantity, new_location, book_id))
            
            # ✅ SỬA: Commit transaction
            self.conn.commit()
            
            print(f"✅ Cập nhật tồn kho cho sách ID {book_id}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi update_inventory: {e}")
            self.conn.rollback()
            return False
    
    # METHOD: UPDATE_INVENTORY_QUANTITY
    def update_inventory_quantity(self, book_id, quantity_change, location, user):
        """
        Cập nhật số lượng tồn kho (dùng cho GUI)
        
        Args:
            book_id: ID sách
            quantity_change: Số lượng thay đổi (+ hoặc -)
            location: Vị trí kho mới
            user: Người thực hiện
        
        Returns:
            tuple: (success: bool, new_quantity hoặc error_message)
        """
        if not self.cursor:
            return False, "Không có kết nối database"
        
        try:
            # Lấy số lượng hiện tại
            self.cursor.execute("SELECT SoLuongTon FROM TonKho WHERE IdSach = ?", (book_id,))
            row = self.cursor.fetchone()
            
            if not row:
                return False, "Không tìm thấy tồn kho cho sách này"
            
            current_qty = row[0]
            new_qty = current_qty + quantity_change
            
            if new_qty < 0:
                return False, "Số lượng tồn không đủ để xuất"
            
            # Cập nhật tồn kho
            self.cursor.execute("""
                UPDATE TonKho 
                SET SoLuongTon = ?, ViTri = ?, NgayCapNhat = GETDATE()
                WHERE IdSach = ?
            """, (new_qty, location, book_id))
            
            # Ghi lịch sử
            loai_gd = "Nhập kho" if quantity_change > 0 else "Xuất kho"
            
            self.cursor.execute("SELECT GiaMua, GiaBia FROM Sach WHERE Id = ?", (book_id,))
            price_row = self.cursor.fetchone()
            gia = price_row[0] if quantity_change > 0 else price_row[1] if price_row else 0
            
            self.cursor.execute("""
                INSERT INTO LichSuGiaoDich (IdSach, LoaiGiaoDich, SoLuong, GiaTri, NguoiThucHien, GhiChu)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (book_id, loai_gd, abs(quantity_change), gia * abs(quantity_change), user, ""))
            
            # Commit
            self.conn.commit()
            
            print(f"✅ {loai_gd}: {abs(quantity_change)} quyển, tồn mới: {new_qty}")
            return True, new_qty
            
        except Exception as e:
            print(f"❌ Lỗi update_inventory_quantity: {e}")
            self.conn.rollback()
            return False, str(e)
    
    # METHOD: GET_TRANSACTIONS
    def get_transactions(self, book_id=None, limit=100):
        """Lấy lịch sử giao dịch"""
        if not self.cursor:
            return []
        
        try:
            if book_id:
                query = """
                    SELECT TOP (?) 
                        NgayGiaoDich, IdSach, LoaiGiaoDich, SoLuong, 
                        GiaTri, NguoiThucHien, GhiChu
                    FROM LichSuGiaoDich
                    WHERE IdSach = ?
                    ORDER BY NgayGiaoDich DESC
                """
                self.cursor.execute(query, (limit, book_id))
            else:
                query = """
                    SELECT TOP (?) 
                        NgayGiaoDich, IdSach, LoaiGiaoDich, SoLuong, 
                        GiaTri, NguoiThucHien, GhiChu
                    FROM LichSuGiaoDich
                    ORDER BY NgayGiaoDich DESC
                """
                self.cursor.execute(query, (limit,))
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi get_transactions: {e}")
            return []
    
    # ============================================================
    # BUSINESS / ORDER OPERATIONS
    # ============================================================
    
    # METHOD: GET_ALL_ORDERS
    def get_all_orders(self):
        """Lấy tất cả đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                ORDER BY NgayDat DESC, Id DESC
            """
            self.cursor.execute(query)
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi get_all_orders: {e}")
            return []
    
    # METHOD: SEARCH_ORDERS
    def search_orders(self, query):
        """Tìm kiếm đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                WHERE MaDonHang LIKE ? OR TenKhachHang LIKE ?
                ORDER BY NgayDat DESC
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term))
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search_orders: {e}")
            return []
    
    # METHOD: GET_ORDER_DETAILS
    def get_order_details(self, order_id):
        """Lấy chi tiết đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    ct.IdSach,
                    s.MaSach,
                    s.TenSach,
                    ct.SoLuong,
                    ct.DonGia,
                    ct.ThanhTien
                FROM ChiTietDonHang ct
                JOIN Sach s ON ct.IdSach = s.Id
                WHERE ct.IdDonHang = ?
            """
            self.cursor.execute(query, (order_id,))
            
            details = []
            for row in self.cursor.fetchall():
                details.append({
                    'BookID': row[0],
                    'BookCode': row[1],
                    'BookName': row[2],
                    'Quantity': row[3],
                    'UnitPrice': float(row[4]),
                    'Subtotal': float(row[5])
                })
            
            return details
            
        except Exception as e:
            print(f"❌ Lỗi get_order_details: {e}")
            return []
    
    # METHOD: UPDATE_ORDER_STATUS
    def update_order_status(self, order_id, new_status):
        """Cập nhật trạng thái đơn"""
        if not self.cursor:
            return False
        
        try:
            self.cursor.execute("""
                UPDATE DonHang 
                SET TrangThai = ?, NgayCapNhat = GETDATE()
                WHERE Id = ?
            """, (new_status, order_id))
            
            # ✅ SỬA: Commit transaction
            self.conn.commit()
            
            print(f"✅ Cập nhật trạng thái đơn {order_id}: {new_status}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi update_order_status: {e}")
            self.conn.rollback()
            return False
    
    # METHOD: GET_REVENUE_STATS
    def get_revenue_stats(self):
        """Thống kê doanh thu chi tiết"""
        if not self.cursor:
            return {
                'TotalOrders': 0,
                'CompletedOrders': 0,
                'ProcessingOrders': 0,
                'TotalRevenue': 0,
                'AvgRevenue': 0
            }
        
        try:
            query = """
                SELECT 
                    COUNT(*) AS TotalOrders,
                    SUM(CASE WHEN TrangThai = N'Hoàn thành' THEN 1 ELSE 0 END) AS Completed,
                    SUM(CASE WHEN TrangThai = N'Đang xử lý' THEN 1 ELSE 0 END) AS Processing,
                    ISNULL(SUM(CASE WHEN TrangThai = N'Hoàn thành' THEN TongTien ELSE 0 END), 0) AS Revenue
                FROM DonHang
            """
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            
            total = row[0] or 0
            completed = row[1] or 0
            processing = row[2] or 0
            revenue = float(row[3] or 0)
            avg = revenue / completed if completed > 0 else 0
            
            return {
                'TotalOrders': total,
                'CompletedOrders': completed,
                'ProcessingOrders': processing,
                'TotalRevenue': revenue,
                'AvgRevenue': avg
            }
            
        except Exception as e:
            print(f"❌ Lỗi get_revenue_stats: {e}")
            return {
                'TotalOrders': 0,
                'CompletedOrders': 0,
                'ProcessingOrders': 0,
                'TotalRevenue': 0,
                'AvgRevenue': 0
            }
    
    # METHOD: GET_TOP_SELLING_BOOKS
    def get_top_selling_books(self, limit=5):
        """Lấy sách bán chạy nhất"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT TOP (?)
                    s.Id,
                    s.MaSach,
                    s.TenSach,
                    SUM(ct.SoLuong) AS TotalSold,
                    SUM(ct.ThanhTien) AS TotalRevenue
                FROM ChiTietDonHang ct
                JOIN Sach s ON ct.IdSach = s.Id
                JOIN DonHang dh ON ct.IdDonHang = dh.Id
                WHERE dh.TrangThai = N'Hoàn thành'
                GROUP BY s.Id, s.MaSach, s.TenSach
                ORDER BY SUM(ct.SoLuong) DESC
            """
            self.cursor.execute(query, (limit,))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'BookID': row[0],
                    'BookCode': row[1],
                    'BookName': row[2],
                    'QuantitySold': int(row[3]),
                    'Revenue': float(row[4])
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Lỗi get_top_selling_books: {e}")
            return []
    
    # METHOD: CREATE_ORDER
    def create_order(self, customer_name, phone, email, address, order_items, created_by="System"):
        """
        Tạo đơn hàng mới
        
        Args:
            customer_name: Tên khách hàng
            phone: Số điện thoại
            email: Email
            address: Địa chỉ
            order_items: List of (book_id, quantity, unit_price)
            created_by: Người tạo đơn (username)
        
        Returns:
            tuple: (success: bool, order_code hoặc error_message)
        """
        if not self.cursor:
            return False, "Không có kết nối database"
        
        try:
            import datetime
            
            # Tạo mã đơn hàng
            self.cursor.execute("SELECT COUNT(*) FROM DonHang")
            count = self.cursor.fetchone()[0]
            order_code = f"DH{count + 1:04d}"
            
            # Tính tổng tiền
            total_amount = sum(qty * price for _, qty, price in order_items)
            
            # ✅ SỬA: Dùng created_by thay vì hardcode 'System'
            self.cursor.execute("""
                INSERT INTO DonHang (MaDonHang, TenKhachHang, SoDienThoai, Email, DiaChi, NgayDat, TongTien, 
                                     TrangThai, NguoiTao)
                VALUES (?, ?, ?, ?, ?, ?, ?, N'Đang xử lý', ?)
            """, (order_code, customer_name, phone, email, address, datetime.date.today(), total_amount, created_by))
            
            # Lấy ID đơn hàng vừa tạo
            self.cursor.execute("SELECT @@IDENTITY")
            order_id = int(self.cursor.fetchone()[0])
             
            # Insert chi tiết đơn hàng
            for book_id, quantity, unit_price in order_items:
                subtotal = quantity * unit_price
                self.cursor.execute("""
                    INSERT INTO ChiTietDonHang (IdDonHang, IdSach, SoLuong, DonGia, ThanhTien)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, book_id, quantity, unit_price, subtotal))
            
            # Commit
            self.conn.commit()
            
            print(f"✅ Tạo đơn hàng {order_code} thành công bởi {created_by}!")
            return True, order_code
            
        except Exception as e:
            print(f"❌ Lỗi create_order: {e}")
            self.conn.rollback()
            return False, str(e)
    
    # METHOD: GET_ORDER_BY_ID
    def get_order_by_id(self, order_id):
        """Lấy thông tin đơn hàng theo ID"""
        if not self.cursor:
            return None
        
        try:
            query = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                WHERE Id = ?
            """
            self.cursor.execute(query, (order_id,))
            row = self.cursor.fetchone()
            
            if row:
                return tuple(row)
            return None
            
        except Exception as e:
            print(f"❌ Lỗi get_order_by_id: {e}")
            return None
    
    # METHOD: DELETE_ORDER
    def delete_order(self, order_id):
        """Xóa/Hủy đơn hàng"""
        if not self.cursor:
            return False, "Không có kết nối database"
        
        try:
            # Cập nhật trạng thái thành "Đã hủy"
            self.cursor.execute("""
                UPDATE DonHang 
                SET TrangThai = N'Đã hủy', NgayCapNhat = GETDATE()
                WHERE Id = ?
            """, (order_id,))
            
            self.conn.commit()
            
            print(f"✅ Đã hủy đơn hàng ID {order_id}")
            return True, "Đã hủy đơn hàng"
            
        except Exception as e:
            print(f"❌ Lỗi delete_order: {e}")
            self.conn.rollback()
            return False, str(e)
    
    # METHOD: UPDATE_ORDER_STATUS
    def update_order_status(self, order_id, new_status):
        """Cập nhật trạng thái đơn hàng"""
        if not self.cursor:
            return False, "Không có kết nối database"
        
        try:
            self.cursor.execute("""
                UPDATE DonHang 
                SET TrangThai = ?, NgayCapNhat = GETDATE()
                WHERE Id = ?
            """, (new_status, order_id))
            
            self.conn.commit()
            
            print(f"✅ Cập nhật trạng thái đơn {order_id}: {new_status}")
            return True, f"Đã cập nhật trạng thái thành '{new_status}'"
            
        except Exception as e:
            print(f"❌ Lỗi update_order_status: {e}")
            self.conn.rollback()
            return False, str(e)
    
    # METHOD: GET_ALL_ORDERS
    def get_all_orders(self):
        """Lấy tất cả đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                ORDER BY NgayDat DESC, Id DESC
            """
            self.cursor.execute(query)
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi get_all_orders: {e}")
            return []
    
    # METHOD: FILTER_ORDERS_BY_STATUS
    def filter_orders_by_status(self, status):
        """Lọc đơn hàng theo trạng thái"""
        if not self.cursor:
            return []
        
        try:
            if status == "Tất cả":
                return self.get_all_orders()
            
            query = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                WHERE TrangThai = ?
                ORDER BY NgayDat DESC, Id DESC
            """
            self.cursor.execute(query, (status,))
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi filter_orders_by_status: {e}")
            return []
    
    # METHOD: SEARCH_ORDERS
    def search_orders(self, query):
        """Tìm kiếm đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            sql = """
                SELECT 
                    Id, MaDonHang, TenKhachHang, SoDienThoai, Email,
                    DiaChi, NgayDat, TongTien, TrangThai, NguoiTao
                FROM DonHang
                WHERE MaDonHang LIKE ? OR TenKhachHang LIKE ? OR SoDienThoai LIKE ?
                ORDER BY NgayDat DESC
            """
            search_term = f'%{query}%'
            self.cursor.execute(sql, (search_term, search_term, search_term))
            
            result = []
            for row in self.cursor.fetchall():
                result.append(tuple(row))
            
            return result
            
        except Exception as e:
            print(f"❌ Lỗi search_orders: {e}")
            return []
    
    # METHOD: GET_ORDER_DETAILS
    def get_order_details(self, order_id):
        """Lấy chi tiết đơn hàng"""
        if not self.cursor:
            return []
        
        try:
            query = """
                SELECT 
                    ct.IdSach,
                    s.MaSach,
                    s.TenSach,
                    ct.SoLuong,
                    ct.DonGia,
                    ct.ThanhTien
                FROM ChiTietDonHang ct
                JOIN Sach s ON ct.IdSach = s.Id
                WHERE ct.IdDonHang = ?
            """
            self.cursor.execute(query, (order_id,))
            
            details = []
            for row in self.cursor.fetchall():
                details.append({
                    'BookID': row[0],
                    'BookCode': row[1],
                    'BookName': row[2],
                    'Quantity': row[3],
                    'UnitPrice': float(row[4]),
                    'Subtotal': float(row[5])
                })
            
            return details
            
        except Exception as e:
            print(f"❌ Lỗi get_order_details: {e}")
            return []
    
    # METHOD: GET_REVENUE_STATS
    def get_revenue_stats(self):
        """Thống kê doanh thu chi tiết"""
        if not self.cursor:
            return {
                'TotalOrders': 0,
                'CompletedOrders': 0,
                'ProcessingOrders': 0,
                'CancelledOrders': 0,
                'TotalRevenue': 0,
                'CompletedRevenue': 0,
                'ProcessingRevenue': 0,
                'AvgRevenue': 0
            }
        
        try:
            # Tổng số đơn hàng
            self.cursor.execute("SELECT COUNT(*) FROM DonHang")
            total_orders = self.cursor.fetchone()[0]
            
            # Đơn hoàn thành
            self.cursor.execute("""
                SELECT COUNT(*), ISNULL(SUM(TongTien), 0) 
                FROM DonHang 
                WHERE TrangThai = N'Hoàn thành'
            """)
            row = self.cursor.fetchone()
            completed_orders = row[0]
            completed_revenue = float(row[1])
            
            # Đơn đang xử lý
            self.cursor.execute("""
                SELECT COUNT(*), ISNULL(SUM(TongTien), 0) 
                FROM DonHang 
                WHERE TrangThai = N'Đang xử lý'
            """)
            row = self.cursor.fetchone()
            processing_orders = row[0]
            processing_revenue = float(row[1])
            
            # Đơn đã hủy
            self.cursor.execute("SELECT COUNT(*) FROM DonHang WHERE TrangThai = N'Đã hủy'")
            cancelled_orders = self.cursor.fetchone()[0]
            
            # ✅ SỬA: Tổng doanh thu = CHỈ đơn hoàn thành
            # Không tính đơn "Đang xử lý" và "Đã hủy"
            total_revenue = completed_revenue
            
            # Doanh thu trung bình (trên đơn hoàn thành)
            avg_revenue = completed_revenue / completed_orders if completed_orders > 0 else 0
            
            return {
                'TotalOrders': total_orders,
                'CompletedOrders': completed_orders,
                'ProcessingOrders': processing_orders,
                'CancelledOrders': cancelled_orders,
                'TotalRevenue': total_revenue,  # ← CHỈ đơn hoàn thành
                'CompletedRevenue': completed_revenue,
                'ProcessingRevenue': processing_revenue,
                'AvgRevenue': avg_revenue
            }
            
        except Exception as e:
            print(f"❌ Lỗi get_revenue_stats: {e}")
            return {
                'TotalOrders': 0,
                'CompletedOrders': 0,
                'ProcessingOrders': 0,
                'CancelledOrders': 0,
                'TotalRevenue': 0,
                'CompletedRevenue': 0,
                'ProcessingRevenue': 0,
                'AvgRevenue': 0
            }

# Backward compatibility - import từ connection_manager
    # METHOD: GETDBCONNECTION
def getDbConnection():
    """Import connection từ connection_manager"""
    try:
        import sys
        from pathlib import Path
        root_dir = Path(__file__).parent.parent
        if str(root_dir) not in sys.path:
            sys.path.insert(0, str(root_dir))
        
        from connection_manager import getDbConnection as get_conn
        return get_conn()
    except:
        return None