# gui/book_manager.py - Quản lý thông tin sách
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import N, E, S, W
from database.book_database import DatabaseManager
from utils.helpers import center_window
from gui.search_windows import SearchWindow

class BookManagerApp:
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("📚 HỆ THỐNG QUẢN LÝ THÔNG TIN SÁCH")
        self.apply_styles()
        self.selected_book = None
        # Biến điều khiển
        self.book_id_text = tk.StringVar()
        self.book_name_text = tk.StringVar()
        self.author_text = tk.StringVar()
        self.field_text = tk.StringVar()
        self.book_type_text = tk.StringVar()
        self.publisher_name_text = tk.StringVar()
        self.buy_price_text = tk.StringVar(value="0.0")
        self.cover_price_text = tk.StringVar(value="0.0")
        self.reprint_text = tk.StringVar(value="0")
        self.publish_year_text = tk.StringVar()
        # Biến cho khu vực Thông tin Tổng quan
        self.total_books_var = tk.StringVar(value="Đang tải...")
        self.status_var = tk.StringVar(value="Kết nối CSDL: Đã sẵn sàng (Mockup)")
        self.BOOK_TYPES = ["Sách Nước Ngoài", "Sách Trong Nước"]
        self.setup_widgets()
        self.view_command()
    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#2196F3", foreground="white", 
                         padding=[5, 5])
        style.configure("Treeview",
            font=('Arial', 10),
            rowheight=25,
            bordercolor="#E0E0E0",
            borderwidth=1,
            relief="flat",
            fieldbackground="#F5F5F5"
        )
        style.map('Treeview', background=[('selected', '#4CAF50')])
        style.configure("TLabel", font=('Arial', 10))
        style.configure("Input.TLabel", font=('Arial', 10, 'bold'), foreground="#333333")
        style.configure("TEntry", font=('Arial', 11), padding=2)
        style.configure("TCombobox", font=('Arial', 11), padding=2)
        style.configure("TSeparator", background="#CCCCCC")
        # --- ĐIỀU CHỈNH FONT/PADDING CHO TẤT CẢ CÁC NÚT ĐỂ ĐỒNG BỘ VÀ CĂN CHỈNH KÝ HIỆU ---
        style.configure("Unified.TButton", font=('Arial', 11, 'bold'), padding=(10, 8), foreground="white")
        style.configure("Add.Unified.TButton", background="#4CAF50")
        style.map("Add.Unified.TButton", background=[('active', '#43A047')])
        style.configure("Update.Unified.TButton", background="#2196F3")
        style.map("Update.Unified.TButton", background=[('active', '#1E88E5')])
        style.configure("Delete.Unified.TButton", background="#F44336")
        style.map("Delete.Unified.TButton", background=[('active', '#E53935')])
        style.configure("Search.Unified.TButton", background="#FFC107")
        style.map("Search.Unified.TButton", background=[('active', '#FFB300')])
        style.configure("View.Unified.TButton", background="#9E9E9E")
        style.map("View.Unified.TButton", background=[('active', '#757575')])
        style.configure("Clear.Unified.TButton", background="#BDBDBD")
        style.map("Clear.Unified.TButton", background=[('active', '#A0A0A0')])
        style.configure("Logout.Unified.TButton", background="#795548")
        style.map("Logout.Unified.TButton", background=[('active', '#6D4C41')])
        # --- KẾT THÚC ĐIỀU CHỈNH ---
    def setup_widgets(self):
        # 1. PanedWindow Chính
        main_pane = ttk.PanedWindow(self.master, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        # 1A. Khu vực Điều khiển và Nhập liệu/Thông tin (Control Frame)
        control_frame = ttk.Frame(main_pane, padding="10")
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=0)
        control_frame.grid_rowconfigure(0, weight=0)
        control_frame.grid_rowconfigure(1, weight=1)
        main_pane.add(control_frame, weight=0)
        # --- KHU VỰC 1: NHẬP LIỆU ---
        input_group = ttk.LabelFrame(control_frame, text=" CHI TIẾT SÁCH ", padding="15")
        input_group.grid(row=0, column=0, sticky=N+E+S+W, padx=(0, 10), pady=(0, 5))
        input_group.grid_columnconfigure(1, weight=1)
        input_group.grid_columnconfigure(3, weight=1)
        input_data = [
            ("MÃ SÁCH:", self.book_id_text, 0, 0),
            ("TÊN SÁCH:", self.book_name_text, 0, 2),
            ("TÁC GIẢ:", self.author_text, 1, 0),
            ("LĨNH VỰC:", self.field_text, 1, 2),
            ("LOẠI SÁCH:", self.book_type_text, 2, 0, True),
            ("NXB:", self.publisher_name_text, 2, 2),
            ("GIÁ MUA:", self.buy_price_text, 3, 0),
            ("GIÁ BÌA:", self.cover_price_text, 3, 2),
            ("LẦN TÁI BẢN:", self.reprint_text, 4, 0),
            ("NĂM XB:", self.publish_year_text, 4, 2)
        ]
        for text, var, row, col, *is_combo in input_data:
            ttk.Label(input_group, text=text, style="Input.TLabel").grid(row=row, column=col, sticky=W, 
                                                                         padx=10, pady=5)
            if is_combo and is_combo[0]:
                ttk.Combobox(input_group, textvariable=var, values=self.BOOK_TYPES, state="readonly",
                             width=30).grid(row=row, column=col+1, padx=(0, 10), pady=5, sticky='ew')
            else:
                ttk.Entry(input_group, textvariable=var, width=35).grid(row=row, column=col+1,  
                                                                        padx=(0, 10), pady=5, sticky='ew')
        # --- KHU VỰC 2: BUTTONS ---
        button_group = ttk.Frame(control_frame, padding="10")
        button_group.grid(row=0, column=1, rowspan=2, sticky=N+S, padx=(10, 0))
        button_group.grid_columnconfigure(0, weight=1)
        
        buttons_info = [
            ("➕ THÊM MỚI", self.add_command, "Add.Unified.TButton"),
            ("🔄 CẬP NHẬT", self.update_command, "Update.Unified.TButton"),
            ("❌ XÓA SÁCH", self.delete_command, "Delete.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("🔍 TÌM KIẾM", self.search_command, "Search.Unified.TButton"),
            ("🔄 TẢI LẠI", self.view_command, "View.Unified.TButton"), 
            ("🧹 XÓA FORM", self.clear_form, "Clear.Unified.TButton"),
            ("---", None, "TSeparator"),
            ("⬅️ QUAY LẠI MENU", self.main_menu.close_book_manager, "Logout.Unified.TButton")
        ]

        row_index = 0
        for text, command, style_name in buttons_info:
            if text == "---":
                ttk.Separator(button_group, orient='horizontal').grid(row=row_index, column=0, sticky='ew', pady=10)
            else:
                ttk.Button(button_group, text=text, command=command, style=style_name).grid(row=row_index, column=0, 
                                                                                            padx=5, pady=4, sticky='ew')
            row_index += 1
        # --- KHU VỰC 3: THÔNG TIN TỔNG QUAN (Giữ nguyên) ---
        info_group = ttk.LabelFrame(control_frame, text=" THÔNG TIN TỔNG QUAN ", padding="15")
        info_group.grid(row=1, column=0, sticky=N+E+S+W, padx=(0, 10), pady=(5, 0))
        info_group.columnconfigure(1, weight=1)
        ttk.Label(info_group, text="Tổng số đầu sách:", style="Input.TLabel").grid(row=0, column=0, sticky=W, 
                                                                                   padx=10, pady=5)
        ttk.Label(info_group, textvariable=self.total_books_var, font=('Arial', 12, 'bold'), 
                  foreground="#F44336").grid(row=0, column=1, sticky=W, padx=10, pady=5)
        ttk.Label(info_group, textvariable=self.status_var, font=('Arial', 9), 
                  foreground="#666666").grid(row=1, column=0, columnspan=2, sticky=W, padx=10, pady=(5, 0))
        # 1B. Khu vực Bảng hiển thị (Treeview)
        list_frame = ttk.Frame(main_pane, padding="10")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        main_pane.add(list_frame, weight=1)
        # CỘT CSDL trả về: (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, 
        # NamXB)
        all_column_ids = ["ID", "MaSach", "TenSach", "TenTacGia", "TenLinhVuc", "LoaiSach", "TenNXB", "GiaMua", 
                          "GiaBia", "LanTaiBan", "NamXB"]
        self.books_list = ttk.Treeview(list_frame, columns=all_column_ids, show='headings', style="Treeview")

        # Cấu hình cột
        column_configs = [
            ("ID", 50, 'center'), ("MaSach", 80, 'center'), ("TenSach", 250, 'w'), ("TenTacGia", 150, 'w'),
            ("TenLinhVuc", 100, 'w'), ("LoaiSach", 100, 'w'), ("TenNXB", 120, 'w'), ("GiaMua", 80, 'e'),
            ("GiaBia", 80, 'e'), ("LanTaiBan", 60, 'center'), ("NamXB", 60, 'center')
        ]

        for col_id, width, anchor in column_configs:
            self.books_list.column(col_id, width=width, anchor=anchor)
            self.books_list.heading(col_id, text=col_id.replace("NamXB", "Năm XB").replace("LanTaiBan", "Tái Bản").replace("TenNXB", "Tên NXB").replace("GiaMua", "Giá Mua").replace("GiaBia", "Giá Bìa").replace("TenLinhVuc", "Lĩnh Vực").replace("TenTacGia", "Tác Giả").replace("TenSach", "Tên Sách").replace("MaSach", "Mã Sách"), anchor='center')
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_list.yview)
        self.books_list.configure(yscrollcommand=vsb.set)
        self.books_list.grid(row=0, column=0, sticky=N+E+S+W)
        vsb.grid(row=0, column=1, sticky='ns')

        self.books_list.bind('<ButtonRelease-1>', self.get_selected_row)

    def fill_form_with_data(self, row_data):
        # row_data: (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
        self.selected_book = row_data
        self.book_id_text.set(row_data[1] if row_data[1] is not None else "")
        self.book_name_text.set(row_data[2] if row_data[2] is not None else "")
        self.author_text.set(row_data[3] if row_data[3] is not None else "")
        self.field_text.set(row_data[4] if row_data[4] is not None else "")
        self.book_type_text.set(row_data[5] if row_data[5] is not None else "")
        self.publisher_name_text.set(row_data[6] if row_data[6] is not None else "")
        self.buy_price_text.set(row_data[7] if row_data[7] is not None else "0.0")
        self.cover_price_text.set(row_data[8] if row_data[8] is not None else "0.0")
        self.reprint_text.set(row_data[9] if row_data[9] is not None else "0")
        self.publish_year_text.set(row_data[10] if row_data[10] is not None else "")

    def select_row_by_db_id(self, db_id_to_select):
        # Hàm này được gọi từ cửa sổ tìm kiếm để chọn dòng tương ứng trong treeview chính
        db_id_to_select = str(db_id_to_select)
        found_item = None

        # Xóa chọn cũ
        if self.books_list.selection():
            self.books_list.selection_remove(self.books_list.selection())
        for item in self.books_list.get_children():
            # Giá trị đầu tiên trong values là Id sách
            if str(self.books_list.item(item, 'values')[0]) == db_id_to_select:
                found_item = item
                break

        if found_item:
            self.books_list.selection_set(found_item)
            self.books_list.focus(found_item)
            self.books_list.see(found_item)
            self.books_list.bind('<ButtonRelease-1>', self.get_selected_row)
    def clear_form(self):
        self.book_id_text.set("")
        self.book_name_text.set("")
        self.author_text.set("")

        self.field_text.set("")
        self.book_type_text.set("")
        self.publisher_name_text.set("")
        self.buy_price_text.set("0.0")
        self.cover_price_text.set("0.0")
        self.reprint_text.set("0")
        self.publish_year_text.set("")
        self.selected_book = None
        if self.books_list.selection():
            self.books_list.selection_remove(self.books_list.selection())
    def get_selected_row(self, event):
        selected_item = self.books_list.focus()

        if not selected_item:
            self.books_list.selection_remove(self.books_list.selection())
            self.clear_form()
            return

        self.books_list.selection_remove(self.books_list.selection())
        self.books_list.selection_set(selected_item)

        values = self.books_list.item(selected_item, 'values')
        # values: (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
        self.fill_form_with_data(values)
    
    # --- START CHANGE ---
    def view_command(self):
        # Tải lại danh sách sách từ DB và cập nhật thông tin tổng quan
        try:
            # THÊM MỚI: Reset form (xóa input và bỏ chọn)
            self.clear_form()

            # Xóa dữ liệu cũ
            for item in self.books_list.get_children():
                self.books_list.delete(item)

            data = self.db.view_all()

            # CỘT CSDL trả về: (Id, MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB)
            for row in data:
                self.books_list.insert('', tk.END, values=row)

            stats = self.db.get_inventory_stats()

            self.total_books_var.set(f"{stats['TotalCount']} đầu sách")
            self.status_var.set("Tải lại dữ liệu hoàn tất.") # Đổi text status

        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}")
            self.total_books_var.set("LỖI KẾT NỐI!")
            self.status_var.set("Kết nối CSDL: Lỗi")
    # --- END CHANGE ---

    def get_all_input_values(self):
        # Trả về tuple các giá trị theo thứ tự: MaSach, TenSach, TenTacGia, TenLinhVuc, LoaiSach, TenNXB, GiaMua, GiaBia, LanTaiBan, NamXB (10 giá trị)
        return (
            self.book_id_text.get().strip(), self.book_name_text.get().strip(), self.author_text.get().strip(),
            self.field_text.get().strip(), self.book_type_text.get().strip(), self.publisher_name_text.get().strip(),
            self.buy_price_text.get().strip(), self.cover_price_text.get().strip(), self.reprint_text.get().strip(),
            self.publish_year_text.get().strip()
        )

    def validate_input(self, values):
        if not all(values[:6]):
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đủ thông tin cơ bản: Mã, Tên, Tác giả, Lĩnh vực, Loại, NXB.")
            return False

        try:
            float(values[6]) # GiaMua
            float(values[7]) # GiaBia
            int(values[8]) # LanTaiBan
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Giá mua/Giá bìa phải là số, Lần tái bản phải là số nguyên.")
            return False
        return True
    def add_command(self):
        values = self.get_all_input_values()
        if not self.validate_input(values): return

        try:
            new_id = self.db.insert_book_full(*values)
            self.view_command()
            
            # self.fill_form_with_data(self.db.get_book_by_id(new_id))
            messagebox.showinfo("Thành công", f"Đã thêm sách: {values[1]}")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi thêm sách: {e}")

    def update_command(self):
        if not self.selected_book:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sách để cập nhật.")
            return
        book_db_id = self.selected_book[0]
        values = self.get_all_input_values()
        if not self.validate_input(values): return
        try:
            self.db.update_book_full(book_db_id, *values)
            self.view_command()
            messagebox.showinfo("Thành công", f"Đã cập nhật sách ID {book_db_id}.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi cập nhật sách: {e}")

    def delete_command(self):
        if not self.selected_book:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một sách để xóa.")
            return

        if not messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc muốn xóa sách '{self.selected_book[2]}' ({self.selected_book[1]})?"):
            return

        try:
            self.db.delete_book(self.selected_book[0])
            self.clear_form()
            self.view_command()
            messagebox.showinfo("Thành công", "Đã xóa sách khỏi hệ thống.")
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi xóa sách: {e}")

    def search_command(self):
        search_window = tk.Toplevel(self.master)
        SearchWindow(search_window, self)
# ----------------------------------------------------
#               CLASS CỬA SỔ QUẢN LÝ KHO SÁCH
# ----------------------------------------------------
