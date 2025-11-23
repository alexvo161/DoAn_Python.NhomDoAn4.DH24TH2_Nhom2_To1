import tkinter as tk
from tkinter import ttk, messagebox
from database.book_database import DatabaseManager
from utils.helpers import center_window, format_currency

class InventoryManagerApp:
    """ Ứng dụng quản lý kho sách """
    
    def __init__(self, master, main_menu_instance, db_conn):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("📦 HỆ THỐNG QUẢN LÝ KHO SÁCH ")
        
        # Biến điều khiển
        self.selected_inventory_record = None
        
        # Biến thống kê
        self.total_books_var = tk.StringVar(value="0")
        self.total_quantity_var = tk.StringVar(value="0")
        self.low_stock_var = tk.StringVar(value="0")
        self.total_value_var = tk.StringVar(value="0 đ")
        self.status_var = tk.StringVar(value="✅ Sẵn sàng")
        
        # Biến lọc
        self.filter_location_var = tk.StringVar(value="Tất cả")
        self.sort_by_var = tk.StringVar(value="Mã sách")
        
        # Colors
        self.colors = {
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
        
        self.setup_widgets()
    
    def setup_widgets(self):
        """Setup giao diện"""
        main_container = tk.Frame(self.master, bg=self.colors['light'], padx=20, pady=15)
        main_container.pack(fill='both', expand=True)
        
        # HEADER
        header_frame = tk.Frame(main_container, bg=self.colors['white'], padx=20, pady=15)
        header_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(header_frame,
            text="📦 QUẢN LÝ KHO SÁCH",
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['white']).pack(side='left')
        
        tk.Label(header_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 10),
            fg=self.colors['success'],
            bg=self.colors['white']).pack(side='right')
        
        # STATISTICS DASHBOARD
        stats_container = tk.Frame(main_container, bg=self.colors['light'])
        stats_container.pack(fill='x', pady=(0, 15))
        
        stat_cards = [
            ("📚", "Tổng đầu sách", self.total_books_var, self.colors['primary']),
            ("📦", "Tổng số lượng", self.total_quantity_var, self.colors['success']),
            ("⚠️", "Sách sắp hết", self.low_stock_var, self.colors['danger']),
            ("💰", "Giá trị kho", self.total_value_var, self.colors['warning'])
        ]
        
        for i, (icon, label, var, color) in enumerate(stat_cards):
            card = self.create_stat_card(stats_container, icon, label, var, color)
            card.grid(row=0, column=i, padx=8, sticky='ew')
            stats_container.columnconfigure(i, weight=1)
        
        # TOOLBAR
        toolbar_frame = tk.Frame(main_container, bg=self.colors['white'], padx=15, pady=12)
        toolbar_frame.pack(fill='x', pady=(0, 15))
        
        left_toolbar = tk.Frame(toolbar_frame, bg=self.colors['white'])
        left_toolbar.pack(side='left', fill='x', expand=True)
        
        tk.Label(left_toolbar,
            text="📍 Vị trí:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white']).pack(side='left', padx=(0, 8))
        
        location_combo = ttk.Combobox(left_toolbar,
            textvariable=self.filter_location_var,
            values=["Tất cả", "Kệ A1", "Kệ A2", "Kệ B1", "Kệ B2", "Kệ C1", "Kệ C2", "Kệ C3", "Kệ D1", "Kệ D2", "Kệ D3", "Kệ D4"],
            state='readonly',
            width=12,
            font=('Segoe UI', 10))
        location_combo.pack(side='left', padx=(0, 20))
        location_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filter())
        
        tk.Label(left_toolbar,
            text="🔽 Sắp xếp:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white']).pack(side='left', padx=(0, 8))
        
        sort_combo = ttk.Combobox(left_toolbar,
            textvariable=self.sort_by_var,
            values=["Mã sách", "Tên sách", "SL Tăng dần", "SL Giảm dần"],
            state='readonly',
            width=15,
            font=('Segoe UI', 10))
        sort_combo.pack(side='left')
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filter())
        
        right_toolbar = tk.Frame(toolbar_frame, bg=self.colors['white'])
        right_toolbar.pack(side='right')
        
        # Nút toolbar với tk.Button
        tk.Button(right_toolbar,
            text="🔍 Tìm kiếm",
            command=self.search_inventory_command,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2').pack(side='left', padx=4)
        
        tk.Button(right_toolbar,
            text="🔄 Làm mới",
            command=self.view_inventory_command,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['info'],
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2').pack(side='left', padx=4)
        
        # DATA TABLE
        table_container = tk.Frame(main_container, bg=self.colors['white'], padx=2, pady=2)
        table_container.pack(fill='both', expand=True, pady=(0, 15))
        
        # Treeview style
        style = ttk.Style()
        style.configure("Inventory.Treeview",
            font=('Segoe UI', 10),
            rowheight=35,
            borderwidth=0,
            fieldbackground=self.colors['white'])
        
        style.configure("Inventory.Treeview.Heading",
            font=('Segoe UI', 11, 'bold'),
            background=self.colors['primary'],
            foreground=self.colors['white'],
            borderwidth=0)
        
        style.map('Inventory.Treeview',
            background=[('selected', self.colors['info'])],
            foreground=[('selected', self.colors['white'])])
        
        scroll_y = ttk.Scrollbar(table_container, orient='vertical')
        scroll_x = ttk.Scrollbar(table_container, orient='horizontal')
        
        self.inventory_tree = ttk.Treeview(table_container,
            columns=("ID", "MaSach", "TenSach", "SoLuong", "ViTri", "TrangThai"),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse',
            style="Inventory.Treeview")
        
        scroll_y.config(command=self.inventory_tree.yview)
        scroll_x.config(command=self.inventory_tree.xview)
        
        columns_config = {
            "ID": (60, 'center', 'ID'),
            "MaSach": (100, 'center', 'Mã Sách'),
            "TenSach": (300, 'w', 'Tên Sách'),
            "SoLuong": (120, 'center', 'Số Lượng Tồn'),
            "ViTri": (120, 'center', 'Vị Trí Kho'),
            "TrangThai": (100, 'center', 'Trạng Thái')
        }
        
        for col, (width, anchor, heading) in columns_config.items():
            self.inventory_tree.heading(col, text=heading)
            self.inventory_tree.column(col, width=width, anchor=anchor)
        
        self.inventory_tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)
        
        self.inventory_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.inventory_tree.bind('<Double-1>', self.on_double_click)
        
        # ACTION BUTTONS - DÙNG TK.BUTTON ĐỂ TRÁNH LỖI STYLE
        action_frame = tk.Frame(main_container, bg=self.colors['light'])
        action_frame.pack(fill='x')
        
        # Button config
        btn_config = {
            'font': ('Segoe UI', 11, 'bold'),
            'bd': 0,
            'cursor': 'hand2',
            'pady': 12
        }
        
        tk.Button(action_frame,
            text="➕ NHẬP KHO",
            command=self.open_stock_in_popup,
            bg=self.colors['success'],
            fg='white',
            **btn_config).pack(side='left', padx=8, expand=True, fill='x')
        
        tk.Button(action_frame,
            text="➖ XUẤT KHO",
            command=self.open_stock_out_popup,
            bg=self.colors['danger'],
            fg='white',
            **btn_config).pack(side='left', padx=8, expand=True, fill='x')
        
        tk.Button(action_frame,
            text="↩️ QUAY LẠI MENU",
            command=self.return_to_menu,
            bg='#757575',
            fg='white',
            **btn_config).pack(side='left', padx=8, expand=True, fill='x')
    
    def create_stat_card(self, parent, icon, label, value_var, color):
        """Tạo card thống kê"""
        card = tk.Frame(parent, bg=self.colors['white'], relief='solid', borderwidth=1)
        card_inner = tk.Frame(card, bg=self.colors['white'], padx=15, pady=12)
        card_inner.pack(fill='both', expand=True)
        
        tk.Label(card_inner,
            text=icon,
            font=('Segoe UI', 24),
            bg=self.colors['white'],
            fg=color).pack()
        
        tk.Label(card_inner,
            textvariable=value_var,
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=color).pack()
        
        tk.Label(card_inner,
            text=label,
            font=('Segoe UI', 9),
            bg=self.colors['white'],
            fg='#666666').pack()
        
        return card
    
    def update_statistics(self):
        """Cập nhật thống kê"""
        stats = self.db.get_inventory_stats()
        
        self.total_books_var.set(str(stats.get('TotalCount', 0)))
        self.total_quantity_var.set(f"{stats.get('TotalQuantity', 0):,}")
        self.low_stock_var.set(str(stats.get('LowStockCount', 0)))
        self.total_value_var.set(format_currency(stats.get('TotalValue', 0)))
    
    def populate_tree_with_colors(self, data):
        """Hiển thị dữ liệu với màu sắc"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        for row in data:
            book_id, ma_sach, ten_sach, so_luong, vi_tri = row
            
            if so_luong < 50:
                status = "🔴 Sắp hết"
                tag = 'danger'
            elif so_luong < 100:
                status = "🟡 Cảnh báo"
                tag = 'warning'
            else:
                status = "🟢 Tốt"
                tag = 'success'
            
            self.inventory_tree.insert('', 'end',
                values=(book_id, ma_sach, ten_sach, f"{so_luong:,}", vi_tri, status),
                tags=(tag,))
        
        self.inventory_tree.tag_configure('danger', foreground=self.colors['danger'])
        self.inventory_tree.tag_configure('warning', foreground=self.colors['warning'])
        self.inventory_tree.tag_configure('success', foreground=self.colors['success'])
    
    def view_inventory_command(self):
        """Xem tồn kho"""
        self.status_var.set("⏳ Đang tải...")
        self.master.update()
        
        try:
            data = self.db.view_inventory()
            self.populate_tree_with_colors(data)
            self.update_statistics()
            self.status_var.set(f"✅ Đã tải {len(data)} sản phẩm")
        except Exception as e:
            self.status_var.set(f"❌ Lỗi: {str(e)}")
    
    def apply_filter(self):
        """Áp dụng lọc"""
        location = self.filter_location_var.get()
        
        if location == "Tất cả":
            data = self.db.view_inventory()
        else:
            # Lọc theo vị trí
            all_data = self.db.view_inventory()
            data = [row for row in all_data if row[4] == location]
        
        self.populate_tree_with_colors(data)
        self.status_var.set(f"✅ Hiển thị {len(data)} sản phẩm")
    
    def on_tree_select(self, event):
        """Khi chọn dòng"""
        selection = self.inventory_tree.selection()
        if selection:
            item = self.inventory_tree.item(selection[0])
            values = item['values']
            
            self.selected_inventory_record = (
                values[0], values[1], values[2],
                int(str(values[3]).replace(',', '')), values[4]
            )
    
    def on_double_click(self, event):
        """Double click xem chi tiết"""
        if not self.selected_inventory_record:
            return
        
        book = self.db.get_book_by_id(self.selected_inventory_record[0])
        if book:
            self.show_detail_popup(self.selected_inventory_record, book)
    
    def show_detail_popup(self, inv_record, book):
        """Hiển thị popup chi tiết"""
        popup = tk.Toplevel(self.master)
        popup.title("📋 Thông tin chi tiết")
        popup.transient(self.master)
        popup.grab_set()
        center_window(popup, 500, 450)
        popup.resizable(False, False)
        
        # Header
        header = tk.Frame(popup, bg=self.colors['primary'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="📋 CHI TIẾT SÁCH TRONG KHO",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg=self.colors['primary']).pack()
        
        # Content
        content = tk.Frame(popup, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        info_items = [
            ("📚 Mã sách:", inv_record[1]),
            ("📖 Tên sách:", inv_record[2]),
            ("✍️ Tác giả:", book[3]),
            ("📂 Lĩnh vực:", book[4]),
            ("📚 Loại sách:", book[5]),
            ("🏢 Nhà xuất bản:", book[6]),
            ("💵 Giá mua:", format_currency(book[7])),
            ("💰 Giá bìa:", format_currency(book[8])),
            ("📦 Số lượng tồn:", f"{inv_record[3]:,} quyển"),
            ("📍 Vị trí kho:", inv_record[4]),
        ]
        
        for label, value in info_items:
            row_frame = tk.Frame(content, bg='white')
            row_frame.pack(fill='x', pady=5)
            
            tk.Label(row_frame,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg='#555',
                width=18,
                anchor='w').pack(side='left')
            
            tk.Label(row_frame,
                text=value,
                font=('Segoe UI', 10),
                bg='white',
                fg='#000',
                anchor='w').pack(side='left', fill='x', expand=True)
        
        # Footer
        footer = tk.Frame(popup, bg='white', pady=15)
        footer.pack(fill='x')
        
        tk.Button(footer,
            text="✅ Đóng",
            command=popup.destroy,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['info'],
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack()
    
    def search_inventory_command(self):
        """Tìm kiếm - POPUP ĐƠN GIẢN"""
        search_popup = tk.Toplevel(self.master)
        search_popup.title("🔍 Tìm kiếm trong kho")
        search_popup.transient(self.master)
        search_popup.grab_set()
        center_window(search_popup, 900, 550)
        
        # Header
        header = tk.Frame(search_popup, bg=self.colors['warning'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="🔍 TÌM KIẾM TRONG KHO",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=self.colors['warning']).pack()
        
        # Search input
        search_frame = tk.Frame(search_popup, bg='white', padx=20, pady=15)
        search_frame.pack(fill='x')
        
        tk.Label(search_frame,
            text="Nhập từ khóa (Mã sách hoặc Tên sách):",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame,
            textvariable=search_var,
            font=('Segoe UI', 12),
            bd=2,
            relief='solid')
        search_entry.pack(fill='x', ipady=8)
        search_entry.focus()
        
        # Results table
        results_container = tk.Frame(search_popup, bg='white', padx=20, pady=10)
        results_container.pack(fill='both', expand=True)
        
        scroll_y = ttk.Scrollbar(results_container, orient='vertical')
        
        results_tree = ttk.Treeview(results_container,
            columns=("ID", "MaSach", "TenSach", "SoLuong", "ViTri"),
            show='headings',
            yscrollcommand=scroll_y.set,
            selectmode='browse',
            style="Inventory.Treeview")
        
        scroll_y.config(command=results_tree.yview)
        
        results_tree.heading("ID", text="ID")
        results_tree.heading("MaSach", text="Mã Sách")
        results_tree.heading("TenSach", text="Tên Sách")
        results_tree.heading("SoLuong", text="SL Tồn")
        results_tree.heading("ViTri", text="Vị Trí")
        
        results_tree.column("ID", width=60, anchor='center')
        results_tree.column("MaSach", width=100, anchor='center')
        results_tree.column("TenSach", width=350, anchor='w')
        results_tree.column("SoLuong", width=100, anchor='center')
        results_tree.column("ViTri", width=100, anchor='center')
        
        results_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        
        def do_search(*args):
            """Thực hiện tìm kiếm"""
            keyword = search_var.get().strip()
            
            # Xóa kết quả cũ
            for item in results_tree.get_children():
                results_tree.delete(item)
            
            if not keyword:
                return
            
            # Tìm kiếm
            data = self.db.view_inventory()
            results = [row for row in data 
                      if keyword.lower() in str(row[1]).lower() 
                      or keyword.lower() in str(row[2]).lower()]
            
            # Hiển thị kết quả
            for row in results:
                results_tree.insert('', 'end', values=row)
        
        def select_and_close():
            """Chọn và đóng"""
            selection = results_tree.selection()
            
            if not selection:
                children = results_tree.get_children()
                if children:
                    results_tree.selection_set(children[0])
                    selection = results_tree.selection()
                else:
                    messagebox.showwarning("Cảnh báo", 
                        "⚠️ Vui lòng chọn một kết quả!")
                    return
            
            item = results_tree.item(selection[0])
            values = item['values']
            
            # Load vào main app
            self.selected_inventory_record = (
                values[0], values[1], values[2],
                int(str(values[3]).replace(',', '')), values[4]
            )
            
            # Highlight trong bảng chính
            for item_id in self.inventory_tree.get_children():
                item_values = self.inventory_tree.item(item_id)['values']
                if str(item_values[0]) == str(values[0]):
                    self.inventory_tree.selection_set(item_id)
                    self.inventory_tree.see(item_id)
                    break
            
            search_popup.destroy()
            
            messagebox.showinfo("Đã chọn",
                f"✅ Đã chọn: {values[2]}\n"
                f"📦 Tồn kho: {values[3]} quyển\n"
                f"📍 Vị trí: {values[4]}\n\n"
                f"💡 Bạn có thể click [➕ NHẬP KHO] hoặc [➖ XUẤT KHO]")
        
        # Bind events
        search_var.trace_add('write', do_search)
        results_tree.bind('<Double-1>', lambda e: select_and_close())
        
        # Buttons
        btn_frame = tk.Frame(search_popup, bg='white', padx=20, pady=15)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame,
            text="✅ Chọn",
            command=select_and_close,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame,
            text="❌ Đóng",
            command=search_popup.destroy,
            font=('Segoe UI', 10, 'bold'),
            bg='#757575',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack(side='left', padx=5)
        
        tk.Label(btn_frame,
            text="💡 Gõ từ khóa để tìm kiếm",
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#666').pack(side='right')
    
    def open_stock_in_popup(self):
        """Mở popup nhập kho"""
        if not self.selected_inventory_record:
            messagebox.showwarning("Cảnh báo",
                "⚠️ Vui lòng chọn sách từ danh sách trước!")
            return
        
        StockInPopup(self.master, self, self.selected_inventory_record, self.db)
    
    def open_stock_out_popup(self):
        """Mở popup xuất kho"""
        if not self.selected_inventory_record:
            messagebox.showwarning("Cảnh báo",
                "⚠️ Vui lòng chọn sách từ danh sách trước!")
            return
        
        StockOutPopup(self.master, self, self.selected_inventory_record, self.db)
    
    def return_to_menu(self):
        """Quay lại menu"""
        self.master.withdraw()
        self.main_menu.master.deiconify()


# ========== POPUP NHẬP KHO ==========
class StockInPopup:
    """Popup nhập kho"""
    
    def __init__(self, parent, main_app, inv_record, db):
        self.main_app = main_app
        self.inv_record = inv_record
        self.db = db
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("➕ Nhập kho")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 550, 750)
        self.popup.resizable(False, True)
        
        self.quantity_var = tk.StringVar(value="0")
        self.location_var = tk.StringVar(value=inv_record[4])
        self.note_var = tk.StringVar()
        self.new_total_var = tk.StringVar(value=f"{inv_record[3]:,}")
        
        self.setup_ui()
        self.quantity_var.trace_add('write', self.calculate_new_total)
    
    def setup_ui(self):
        """Setup UI"""
        colors = self.main_app.colors
        
        # Header
        header = tk.Frame(self.popup, bg=colors['success'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="➕ NHẬP KHO",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['success']).pack()
        
        # Content
        content = tk.Frame(self.popup, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        # Info
        info_frame = tk.LabelFrame(content,
            text=" 📚 Thông tin sách ",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['primary'],
            padx=15,
            pady=10)
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(info_frame,
            text=f"Mã sách: {self.inv_record[1]}",
            font=('Segoe UI', 10),
            bg='white',
            anchor='w').pack(fill='x')
        
        tk.Label(info_frame,
            text=f"Tên sách: {self.inv_record[2]}",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['dark'],
            anchor='w').pack(fill='x', pady=5)
        
        tk.Label(info_frame,
            text=f"Tồn hiện tại: {self.inv_record[3]:,} quyển",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=colors['warning'],
            anchor='w').pack(fill='x')
        
        # Form
        form_frame = tk.LabelFrame(content,
            text=" ➕ Thông tin nhập kho ",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['success'],
            padx=15,
            pady=10)
        form_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(form_frame,
            text="Số lượng nhập:",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        quantity_entry = tk.Entry(form_frame,
            textvariable=self.quantity_var,
            font=('Segoe UI', 12),
            bd=2,
            relief='solid')
        quantity_entry.pack(fill='x', ipady=8, pady=(0, 15))
        quantity_entry.focus()
        
        tk.Label(form_frame,
            text="Vị trí kho:",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        location_combo = ttk.Combobox(form_frame,
            textvariable=self.location_var,
            values=["Kệ A1", "Kệ A2", "Kệ B1", "Kệ B2", "Kệ C1", "Kệ C2", "Kệ C3", "Kệ D1", "Kệ D2", "Kệ D3", "Kệ D4"],
            font=('Segoe UI', 11),
            state='normal')
        location_combo.pack(fill='x', ipady=5, pady=(0, 15))
        
        tk.Label(form_frame,
            text="Ghi chú:",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        tk.Entry(form_frame,
            textvariable=self.note_var,
            font=('Segoe UI', 10),
            bd=2,
            relief='solid').pack(fill='x', ipady=6)
        
        # Result
        result_frame = tk.Frame(content, bg='#E8F5E9', padx=15, pady=12, relief='solid', bd=1)
        result_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(result_frame,
            text="📊 Tồn kho sau khi nhập:",
            font=('Segoe UI', 10, 'bold'),
            bg='#E8F5E9',
            fg=colors['success']).pack(anchor='w')
        
        self.result_label = tk.Label(result_frame,
            textvariable=self.new_total_var,
            font=('Segoe UI', 18, 'bold'),
            bg='#E8F5E9',
            fg=colors['success'])
        self.result_label.pack(anchor='w')
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame,
            text="✅ XÁC NHẬN NHẬP KHO",
            command=self.confirm_stock_in,
            font=('Segoe UI', 11, 'bold'),
            bg=colors['success'],
            fg='white',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2').pack(side='left', padx=(0, 10), expand=True, fill='x')
        
        tk.Button(btn_frame,
            text="❌ HỦY",
            command=self.popup.destroy,
            font=('Segoe UI', 11, 'bold'),
            bg='#757575',
            fg='white',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2').pack(side='left', expand=True, fill='x')
    
    def calculate_new_total(self, *args):
        """Tính tổng"""
        try:
            quantity = int(self.quantity_var.get() or 0)
            if quantity < 0:
                quantity = 0
            new_total = self.inv_record[3] + quantity
            self.new_total_var.set(f"{self.inv_record[3]:,} + {quantity:,} = {new_total:,} quyển")
        except:
            self.new_total_var.set(f"{self.inv_record[3]:,} quyển")
    
    def confirm_stock_in(self):
        """Xác nhận"""
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Lỗi", "❌ Số lượng phải lớn hơn 0!")
                return
            
            location = self.location_var.get().strip()
            if not location:
                messagebox.showerror("Lỗi", "❌ Vui lòng chọn vị trí kho!")
                return
            
            if not messagebox.askyesno("Xác nhận",
                f"Bạn có chắc muốn nhập {quantity:,} quyển vào kho?\n\n"
                f"📚 {self.inv_record[2]}\n"
                f"📦 Tồn hiện tại: {self.inv_record[3]:,}\n"
                f"➕ Nhập thêm: {quantity:,}\n"
                f"📊 Tồn mới: {self.inv_record[3] + quantity:,}"):
                return
            
            success, result = self.db.update_inventory_quantity(
                self.inv_record[0], quantity, location, "Admin")
            
            if success:
                messagebox.showinfo("Thành công",
                    f"✅ Đã nhập {quantity:,} quyển vào kho!\n"
                    f"📦 Tồn kho mới: {result:,} quyển")
                self.popup.destroy()
                self.main_app.view_inventory_command()
            else:
                messagebox.showerror("Lỗi", f"❌ {result}")
        
        except ValueError:
            messagebox.showerror("Lỗi", "❌ Số lượng không hợp lệ!")


# ========== POPUP XUẤT KHO ==========
class StockOutPopup:
    """Popup xuất kho"""
    
    def __init__(self, parent, main_app, inv_record, db):
        self.main_app = main_app
        self.inv_record = inv_record
        self.db = db
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("➖ Xuất kho")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 550, 750)
        self.popup.resizable(False, True)
        
        self.quantity_var = tk.StringVar(value="0")
        self.location_var = tk.StringVar(value=inv_record[4])
        self.note_var = tk.StringVar()
        self.new_total_var = tk.StringVar(value=f"{inv_record[3]:,}")
        
        self.setup_ui()
        self.quantity_var.trace_add('write', self.calculate_new_total)
    
    def setup_ui(self):
        """Setup UI"""
        colors = self.main_app.colors
        
        header = tk.Frame(self.popup, bg=colors['danger'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="➖ XUẤT KHO",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['danger']).pack()
        
        content = tk.Frame(self.popup, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        info_frame = tk.LabelFrame(content,
            text=" 📚 Thông tin sách ",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['primary'],
            padx=15,
            pady=10)
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(info_frame,
            text=f"Mã sách: {self.inv_record[1]}",
            font=('Segoe UI', 10),
            bg='white').pack(fill='x')
        
        tk.Label(info_frame,
            text=f"Tên sách: {self.inv_record[2]}",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['dark']).pack(fill='x', pady=5)
        
        tk.Label(info_frame,
            text=f"Tồn hiện tại: {self.inv_record[3]:,} quyển",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=colors['warning']).pack(fill='x')
        
        form_frame = tk.LabelFrame(content,
            text=" ➖ Thông tin xuất kho ",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['danger'],
            padx=15,
            pady=10)
        form_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(form_frame,
            text="Số lượng xuất:",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        quantity_entry = tk.Entry(form_frame,
            textvariable=self.quantity_var,
            font=('Segoe UI', 12),
            bd=2,
            relief='solid')
        quantity_entry.pack(fill='x', ipady=8, pady=(0, 15))
        quantity_entry.focus()
        
        tk.Label(form_frame,
            text="Ghi chú:",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        tk.Entry(form_frame,
            textvariable=self.note_var,
            font=('Segoe UI', 10),
            bd=2,
            relief='solid').pack(fill='x', ipady=6)
        
        result_frame = tk.Frame(content, bg='#FFEBEE', padx=15, pady=12, relief='solid', bd=1)
        result_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(result_frame,
            text="📊 Tồn kho sau khi xuất:",
            font=('Segoe UI', 10, 'bold'),
            bg='#FFEBEE',
            fg=colors['danger']).pack(anchor='w')
        
        self.result_label = tk.Label(result_frame,
            textvariable=self.new_total_var,
            font=('Segoe UI', 18, 'bold'),
            bg='#FFEBEE',
            fg=colors['danger'])
        self.result_label.pack(anchor='w')
        
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame,
            text="✅ XÁC NHẬN XUẤT KHO",
            command=self.confirm_stock_out,
            font=('Segoe UI', 11, 'bold'),
            bg=colors['danger'],
            fg='white',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2').pack(side='left', padx=(0, 10), expand=True, fill='x')
        
        tk.Button(btn_frame,
            text="❌ HỦY",
            command=self.popup.destroy,
            font=('Segoe UI', 11, 'bold'),
            bg='#757575',
            fg='white',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2').pack(side='left', expand=True, fill='x')
    
    def calculate_new_total(self, *args):
        """Tính tổng"""
        try:
            quantity = int(self.quantity_var.get() or 0)
            if quantity < 0:
                quantity = 0
            new_total = self.inv_record[3] - quantity
            if new_total < 0:
                self.new_total_var.set(f"❌ Không đủ hàng!")
                self.result_label.config(fg='red')
            else:
                self.new_total_var.set(f"{self.inv_record[3]:,} - {quantity:,} = {new_total:,} quyển")
                self.result_label.config(fg=self.main_app.colors['danger'])
        except:
            self.new_total_var.set(f"{self.inv_record[3]:,} quyển")
    
    def confirm_stock_out(self):
        """Xác nhận"""
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Lỗi", "❌ Số lượng phải lớn hơn 0!")
                return
            
            if quantity > self.inv_record[3]:
                messagebox.showerror("Lỗi",
                    f"❌ Số lượng xuất ({quantity:,}) lớn hơn tồn kho ({self.inv_record[3]:,})!")
                return
            
            if not messagebox.askyesno("Xác nhận",
                f"Bạn có chắc muốn xuất {quantity:,} quyển khỏi kho?\n\n"
                f"📚 {self.inv_record[2]}\n"
                f"📦 Tồn hiện tại: {self.inv_record[3]:,}\n"
                f"➖ Xuất ra: {quantity:,}\n"
                f"📊 Tồn còn: {self.inv_record[3] - quantity:,}"):
                return
            
            success, result = self.db.update_inventory_quantity(
                self.inv_record[0], -quantity, self.location_var.get(), "Admin")
            
            if success:
                messagebox.showinfo("Thành công",
                    f"✅ Đã xuất {quantity:,} quyển khỏi kho!\n"
                    f"📦 Tồn kho còn: {result:,} quyển")
                self.popup.destroy()
                self.main_app.view_inventory_command()
            else:
                messagebox.showerror("Lỗi", f"❌ {result}")
        
        except ValueError:
            messagebox.showerror("Lỗi", "❌ Số lượng không hợp lệ!")