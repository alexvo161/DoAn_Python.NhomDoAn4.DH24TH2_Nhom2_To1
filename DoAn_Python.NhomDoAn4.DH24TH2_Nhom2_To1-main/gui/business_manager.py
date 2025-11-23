import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database.book_database import DatabaseManager
from utils.helpers import center_window, format_currency

class BusinessManagerApp:
    """Ứng dụng quản lý kinh doanh - Đơn hàng & Doanh thu"""
    
    def __init__(self, master, main_menu_instance, db_conn, user_info=None):
        self.db = DatabaseManager(db_conn)
        self.master = master
        self.main_menu = main_menu_instance
        master.title("💼 HỆ THỐNG QUẢN LÝ KINH DOANH")
        
        # ✅ THÊM: Lưu thông tin user
        self.user_info = user_info if user_info else {'username': 'System', 'full_name': 'System'}
        self.username = self.user_info.get('username', 'System')
        
        # Biến điều khiển
        self.selected_order = None
        
        # Biến thống kê
        self.total_orders_var = tk.StringVar(value="0")
        self.total_revenue_var = tk.StringVar(value="0 đ")
        self.completed_var = tk.StringVar(value="0")
        self.processing_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="✅ Sẵn sàng")
        
        # Biến lọc
        self.filter_status_var = tk.StringVar(value="Tất cả")
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        self.end_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        
        # Colors
        self.colors = {
            'primary': '#1976D2',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'danger': '#F44336',
            'info': '#00BCD4',
            'purple': '#9C27B0',
            'light': '#F5F5F5',
            'dark': '#212121',
            'white': '#FFFFFF',
        }
        
        self.setup_widgets()
        self.load_orders()
    
    def setup_widgets(self):
        """Setup giao diện"""
        main_container = tk.Frame(self.master, bg=self.colors['light'], padx=20, pady=15)
        main_container.pack(fill='both', expand=True)
        
        # HEADER
        header_frame = tk.Frame(main_container, bg=self.colors['white'], padx=20, pady=15)
        header_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(header_frame,
            text="💼 QUẢN LÝ KINH DOANH",
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
            ("📦", "Tổng đơn hàng", self.total_orders_var, self.colors['primary']),
            ("💰", "Doanh thu", self.total_revenue_var, self.colors['purple']),
            ("✅", "Hoàn thành", self.completed_var, self.colors['success']),
            ("⏳", "Đang xử lý", self.processing_var, self.colors['warning'])
        ]
        
        for i, (icon, label, var, color) in enumerate(stat_cards):
            card = self.create_stat_card(stats_container, icon, label, var, color)
            card.grid(row=0, column=i, padx=8, sticky='ew')
            stats_container.columnconfigure(i, weight=1)
        
        # FILTER TOOLBAR
        toolbar_frame = tk.Frame(main_container, bg=self.colors['white'], padx=15, pady=12)
        toolbar_frame.pack(fill='x', pady=(0, 15))
        
        left_toolbar = tk.Frame(toolbar_frame, bg=self.colors['white'])
        left_toolbar.pack(side='left', fill='x', expand=True)
        
        # Date filter
        tk.Label(left_toolbar,
            text="🗓️ Từ ngày:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white']).pack(side='left', padx=(0, 5))
        
        tk.Entry(left_toolbar,
            textvariable=self.start_date_var,
            font=('Segoe UI', 10),
            width=12,
            bd=2,
            relief='solid').pack(side='left', padx=(0, 15))
        
        tk.Label(left_toolbar,
            text="→ Đến:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white']).pack(side='left', padx=(0, 5))
        
        tk.Entry(left_toolbar,
            textvariable=self.end_date_var,
            font=('Segoe UI', 10),
            width=12,
            bd=2,
            relief='solid').pack(side='left', padx=(0, 20))
        
        # Status filter
        tk.Label(left_toolbar,
            text="📊 Trạng thái:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['white']).pack(side='left', padx=(0, 8))
        
        status_combo = ttk.Combobox(left_toolbar,
            textvariable=self.filter_status_var,
            values=["Tất cả", "Hoàn thành", "Đang xử lý", "Đã hủy"],
            state='readonly',
            width=12,
            font=('Segoe UI', 10))
        status_combo.pack(side='left')
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filter())
        
        # Action buttons
        right_toolbar = tk.Frame(toolbar_frame, bg=self.colors['white'])
        right_toolbar.pack(side='right')
        
        tk.Button(right_toolbar,
            text="🔍 Tìm kiếm",
            command=self.search_orders,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2').pack(side='left', padx=4)
        
        tk.Button(right_toolbar,
            text="📊 Báo cáo",
            command=self.show_report,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['purple'],
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2').pack(side='left', padx=4)
        
        tk.Button(right_toolbar,
            text="🔄 Làm mới",
            command=self.load_orders,
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
        style.configure("Business.Treeview",
            font=('Segoe UI', 10),
            rowheight=35,
            borderwidth=0,
            fieldbackground=self.colors['white'])
        
        style.configure("Business.Treeview.Heading",
            font=('Segoe UI', 11, 'bold'),
            background=self.colors['primary'],
            foreground=self.colors['white'],
            borderwidth=0)
        
        style.map('Business.Treeview',
            background=[('selected', self.colors['info'])],
            foreground=[('selected', self.colors['white'])])
        
        scroll_y = ttk.Scrollbar(table_container, orient='vertical')
        scroll_x = ttk.Scrollbar(table_container, orient='horizontal')
        
        self.orders_tree = ttk.Treeview(table_container,
            columns=("ID", "MaDH", "NgayDat", "KhachHang", "SoDT", "TongTien", "TrangThai"),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse',
            style="Business.Treeview")
        
        scroll_y.config(command=self.orders_tree.yview)
        scroll_x.config(command=self.orders_tree.xview)
        
        columns_config = {
            "ID": (50, 'center', 'ID'),
            "MaDH": (100, 'center', 'Mã Đơn Hàng'),
            "NgayDat": (110, 'center', 'Ngày Đặt'),
            "KhachHang": (200, 'w', 'Khách Hàng'),
            "SoDT": (120, 'center', 'Số Điện Thoại'),
            "TongTien": (120, 'e', 'Tổng Tiền'),
            "TrangThai": (120, 'center', 'Trạng Thái')
        }
        
        for col, (width, anchor, heading) in columns_config.items():
            self.orders_tree.heading(col, text=heading)
            self.orders_tree.column(col, width=width, anchor=anchor)
        
        self.orders_tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)
        
        self.orders_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.orders_tree.bind('<Double-1>', self.on_double_click)
        
        # ACTION BUTTONS
        action_frame = tk.Frame(main_container, bg=self.colors['light'])
        action_frame.pack(fill='x')
        
        btn_config = {
            'font': ('Segoe UI', 11, 'bold'),
            'bd': 0,
            'cursor': 'hand2',
            'pady': 12
        }
        
        tk.Button(action_frame,
            text="➕ TẠO ĐƠN MỚI",
            command=self.create_order,
            bg=self.colors['success'],
            fg='white',
            **btn_config).pack(side='left', padx=5, expand=True, fill='x')
        
        tk.Button(action_frame,
            text="📝 SỬA ĐƠN",
            command=self.edit_order,
            bg=self.colors['warning'],
            fg='white',
            **btn_config).pack(side='left', padx=5, expand=True, fill='x')
        
        tk.Button(action_frame,
            text="🗑️ HỦY ĐƠN",
            command=self.cancel_order,
            bg=self.colors['danger'],
            fg='white',
            **btn_config).pack(side='left', padx=5, expand=True, fill='x')
        
        tk.Button(action_frame,
            text="📊 CHI TIẾT",
            command=self.show_order_detail,
            bg=self.colors['info'],
            fg='white',
            **btn_config).pack(side='left', padx=5, expand=True, fill='x')
        
        tk.Button(action_frame,
            text="↩️ QUAY LẠI MENU",
            command=self.return_to_menu,
            bg='#757575',
            fg='white',
            **btn_config).pack(side='left', padx=5, expand=True, fill='x')
    
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
    
    def load_orders(self):
        """Tải danh sách đơn hàng"""
        self.status_var.set("⏳ Đang tải...")
        self.master.update()
        
        try:
            orders = self.db.get_all_orders()
            self.populate_tree(orders)
            self.update_statistics()
            self.status_var.set(f"✅ Đã tải {len(orders)} đơn hàng")
        except Exception as e:
            self.status_var.set(f"❌ Lỗi: {str(e)}")
    
    def populate_tree(self, orders):
        """Hiển thị danh sách đơn hàng"""
        # Xóa dữ liệu cũ
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Thêm dữ liệu mới
        for order in orders:
            order_id, code, customer, phone, email, address, date, amount, status, created_by = order
            
            # Màu sắc theo trạng thái
            if status == 'Hoàn thành':
                tag = 'success'
                status_text = '✅ Hoàn thành'
            elif status == 'Đang xử lý':
                tag = 'warning'
                status_text = '⏳ Đang xử lý'
            elif status == 'Đã hủy':
                tag = 'danger'
                status_text = '❌ Đã hủy'
            else:
                tag = 'info'
                status_text = f'📦 {status}'
            
            self.orders_tree.insert('', 'end',
                values=(order_id, code, date, customer, phone, format_currency(amount), status_text),
                tags=(tag,))
        
        # Configure tags
        self.orders_tree.tag_configure('success', foreground=self.colors['success'])
        self.orders_tree.tag_configure('warning', foreground=self.colors['warning'])
        self.orders_tree.tag_configure('danger', foreground=self.colors['danger'])
        self.orders_tree.tag_configure('info', foreground=self.colors['info'])
    
    def update_statistics(self):
        """Cập nhật thống kê"""
        stats = self.db.get_revenue_stats()
        
        self.total_orders_var.set(str(stats.get('TotalOrders', 0)))
        self.total_revenue_var.set(format_currency(stats.get('TotalRevenue', 0)))
        self.completed_var.set(str(stats.get('CompletedOrders', 0)))
        self.processing_var.set(str(stats.get('ProcessingOrders', 0)))
    
    def apply_filter(self):
        """Áp dụng lọc"""
        status = self.filter_status_var.get()
        orders = self.db.filter_orders_by_status(status)
        self.populate_tree(orders)
        self.status_var.set(f"✅ Hiển thị {len(orders)} đơn hàng")
    
    def on_tree_select(self, event):
        """Khi chọn dòng"""
        selection = self.orders_tree.selection()
        if selection:
            item = self.orders_tree.item(selection[0])
            values = item['values']
            self.selected_order = values[0]  # Lưu ID
    
    def on_double_click(self, event):
        """Double click xem chi tiết"""
        if self.selected_order:
            self.show_order_detail()
    
    def create_order(self):
        """Tạo đơn hàng mới"""
        CreateOrderPopup(self.master, self, self.db)
    
    def edit_order(self):
        """Sửa đơn hàng"""
        if not self.selected_order:
            messagebox.showwarning("Cảnh báo",
                "⚠️ Vui lòng chọn đơn hàng cần sửa!")
            return
        
        order = self.db.get_order_by_id(self.selected_order)
        if order:
            EditOrderPopup(self.master, self, self.db, order)
    
    def cancel_order(self):
        """Hủy đơn hàng"""
        if not self.selected_order:
            messagebox.showwarning("Cảnh báo",
                "⚠️ Vui lòng chọn đơn hàng cần hủy!")
            return
        
        order = self.db.get_order_by_id(self.selected_order)
        if not order:
            return
        
        if order[8] == 'Đã hủy':
            messagebox.showinfo("Thông báo",
                "ℹ️ Đơn hàng này đã được hủy trước đó!")
            return
        
        if messagebox.askyesno("Xác nhận hủy đơn",
            f"Bạn có chắc muốn hủy đơn hàng?\n\n"
            f"📝 Mã đơn: {order[1]}\n"
            f"👤 Khách hàng: {order[2]}\n"
            f"💰 Tổng tiền: {format_currency(order[7])}"):
            
            success, msg = self.db.delete_order(self.selected_order)
            if success:
                messagebox.showinfo("Thành công",
                    "✅ Đã hủy đơn hàng thành công!")
                self.load_orders()
            else:
                messagebox.showerror("Lỗi", f"❌ {msg}")
    
    def show_order_detail(self):
        """Hiển thị chi tiết đơn hàng"""
        if not self.selected_order:
            messagebox.showwarning("Cảnh báo",
                "⚠️ Vui lòng chọn đơn hàng để xem chi tiết!")
            return
        
        order = self.db.get_order_by_id(self.selected_order)
        if order:
            OrderDetailPopup(self.master, self.db, order)
    
    def search_orders(self):
        """Tìm kiếm đơn hàng"""
        SearchOrderPopup(self.master, self, self.db)
    
    def show_report(self):
        """Hiển thị báo cáo"""
        ReportPopup(self.master, self.db)
    
    def return_to_menu(self):
        """Quay lại menu"""
        self.master.withdraw()
        self.main_menu.master.deiconify()


# ========== POPUP TẠO ĐƠN HÀNG ==========
class CreateOrderPopup:
    """Popup tạo đơn hàng mới"""
    
    def __init__(self, parent, main_app, db):
        self.main_app = main_app
        self.db = db
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("➕ Tạo đơn hàng mới")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 700, 650)
        self.popup.resizable(False, False)
        
        # Biến
        self.customer_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.total_var = tk.StringVar(value="0 đ")
        
        # Giỏ hàng: [(book_id, book_code, book_name, quantity, unit_price, subtotal), ...]
        self.cart_items = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        colors = self.main_app.colors
        
        # Header
        header = tk.Frame(self.popup, bg=colors['success'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="➕ TẠO ĐƠN HÀNG MỚI",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['success']).pack()
        
        # Content
        content = tk.Frame(self.popup, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        # Customer info
        customer_frame = tk.LabelFrame(content,
            text=" 👤 Thông tin khách hàng ",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['primary'],
            padx=15,
            pady=10)
        customer_frame.pack(fill='x', pady=(0, 15))
        
        # Tên khách hàng
        tk.Label(customer_frame,
            text="Tên khách hàng: *",
            font=('Segoe UI', 10),
            bg='white').grid(row=0, column=0, sticky='w', pady=5)
        
        tk.Entry(customer_frame,
            textvariable=self.customer_name_var,
            font=('Segoe UI', 10),
            width=40,
            bd=2,
            relief='solid').grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Số điện thoại
        tk.Label(customer_frame,
            text="Số điện thoại: *",
            font=('Segoe UI', 10),
            bg='white').grid(row=1, column=0, sticky='w', pady=5)
        
        tk.Entry(customer_frame,
            textvariable=self.phone_var,
            font=('Segoe UI', 10),
            width=40,
            bd=2,
            relief='solid').grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Email
        tk.Label(customer_frame,
            text="Email:",
            font=('Segoe UI', 10),
            bg='white').grid(row=2, column=0, sticky='w', pady=5)
        
        tk.Entry(customer_frame,
            textvariable=self.email_var,
            font=('Segoe UI', 10),
            width=40,
            bd=2,
            relief='solid').grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Địa chỉ
        tk.Label(customer_frame,
            text="Địa chỉ:",
            font=('Segoe UI', 10),
            bg='white').grid(row=3, column=0, sticky='w', pady=5)
        
        tk.Entry(customer_frame,
            textvariable=self.address_var,
            font=('Segoe UI', 10),
            width=40,
            bd=2,
            relief='solid').grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Books selection
        books_frame = tk.LabelFrame(content,
            text=" 📚 Chọn sách ",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg=colors['success'],
            padx=15,
            pady=10)
        books_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        tk.Button(books_frame,
            text="🔍 Tìm và thêm sách",
            command=self.select_books,
            font=('Segoe UI', 10, 'bold'),
            bg=colors['warning'],
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2').pack(pady=(0, 10))
        
        # Cart list
        self.cart_frame = tk.Frame(books_frame, bg='white')
        self.cart_frame.pack(fill='both', expand=True)
        
        tk.Label(self.cart_frame,
            text="📦 Giỏ hàng trống",
            font=('Segoe UI', 10, 'italic'),
            bg='white',
            fg='#999').pack(pady=20)
        
        # Total
        total_frame = tk.Frame(content, bg='#E8F5E9', padx=15, pady=12, relief='solid', bd=1)
        total_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(total_frame,
            text="💰 Tổng tiền:",
            font=('Segoe UI', 12, 'bold'),
            bg='#E8F5E9',
            fg=colors['success']).pack(side='left')
        
        tk.Label(total_frame,
            textvariable=self.total_var,
            font=('Segoe UI', 18, 'bold'),
            bg='#E8F5E9',
            fg=colors['success']).pack(side='right')
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame,
            text="✅ TẠO ĐƠN HÀNG",
            command=self.confirm_create,
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
    
    def select_books(self):
        """Chọn sách"""
        SelectBooksPopup(self.popup, self, self.db)
    
    def add_to_cart(self, book_id, book_code, book_name, quantity, unit_price):
        """Thêm sách vào giỏ"""
        # Kiểm tra đã có trong giỏ chưa
        for i, item in enumerate(self.cart_items):
            if item[0] == book_id:
                # Cập nhật số lượng
                new_qty = item[3] + quantity
                new_subtotal = new_qty * unit_price
                self.cart_items[i] = (book_id, book_code, book_name, new_qty, unit_price, new_subtotal)
                self.update_cart_display()
                return
        
        # Thêm mới
        subtotal = quantity * unit_price
        self.cart_items.append((book_id, book_code, book_name, quantity, unit_price, subtotal))
        self.update_cart_display()
    
    def remove_from_cart(self, index):
        """Xóa khỏi giỏ"""
        if 0 <= index < len(self.cart_items):
            del self.cart_items[index]
            self.update_cart_display()
    
    def update_cart_display(self):
        """Cập nhật hiển thị giỏ hàng"""
        # Xóa frame cũ
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        
        if not self.cart_items:
            tk.Label(self.cart_frame,
                text="📦 Giỏ hàng trống",
                font=('Segoe UI', 10, 'italic'),
                bg='white',
                fg='#999').pack(pady=20)
            self.total_var.set("0 đ")
            return
        
        # Hiển thị các item
        for i, (book_id, code, name, qty, price, subtotal) in enumerate(self.cart_items):
            item_frame = tk.Frame(self.cart_frame, bg='#f9f9f9', pady=8, padx=10)
            item_frame.pack(fill='x', pady=2)
            
            tk.Label(item_frame,
                text=f"{i+1}. {name} ({code})",
                font=('Segoe UI', 10, 'bold'),
                bg='#f9f9f9',
                anchor='w').pack(side='left', fill='x', expand=True)
            
            tk.Label(item_frame,
                text=f"x{qty}",
                font=('Segoe UI', 10),
                bg='#f9f9f9').pack(side='left', padx=10)
            
            tk.Label(item_frame,
                text=format_currency(subtotal),
                font=('Segoe UI', 10, 'bold'),
                bg='#f9f9f9',
                fg=self.main_app.colors['success']).pack(side='left', padx=10)
            
            tk.Button(item_frame,
                text="❌",
                command=lambda idx=i: self.remove_from_cart(idx),
                font=('Segoe UI', 8),
                bg=self.main_app.colors['danger'],
                fg='white',
                bd=0,
                cursor='hand2').pack(side='left')
        
        # Tính tổng
        total = sum(item[5] for item in self.cart_items)
        self.total_var.set(format_currency(total))
    
    def confirm_create(self):
        """Xác nhận tạo đơn"""
        # Validate
        if not self.customer_name_var.get().strip():
            messagebox.showerror("Lỗi", "❌ Vui lòng nhập tên khách hàng!")
            return
        
        if not self.phone_var.get().strip():
            messagebox.showerror("Lỗi", "❌ Vui lòng nhập số điện thoại!")
            return
        
        if not self.cart_items:
            messagebox.showerror("Lỗi", "❌ Vui lòng chọn ít nhất 1 sách!")
            return
        
        # Prepare order items
        order_items = [(item[0], item[3], item[4]) for item in self.cart_items]
        
        # Create order
        success, result = self.db.create_order(
            self.customer_name_var.get().strip(),
            self.phone_var.get().strip(),
            self.email_var.get().strip(),
            self.address_var.get().strip(),
            order_items,
            self.main_app.username  # <- Username
        )
        
        if success:
            messagebox.showinfo("Thành công",
                f"✅ Đã tạo đơn hàng thành công!\n"
                f"📝 Mã đơn: {result}")
            self.popup.destroy()
            self.main_app.load_orders()
        else:
            messagebox.showerror("Lỗi", f"❌ {result}")


# ========== POPUP CHỌN SÁCH ==========
class SelectBooksPopup:
    """Popup chọn sách để thêm vào đơn"""
    
    def __init__(self, parent, order_popup, db):
        self.order_popup = order_popup
        self.db = db
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("🔍 Chọn sách")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 800, 500)
        
        self.setup_ui()
        self.load_books()
    
    def setup_ui(self):
        """Setup UI"""
        colors = self.order_popup.main_app.colors
        
        # Header
        header = tk.Frame(self.popup, bg=colors['warning'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="🔍 CHỌN SÁCH",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['warning']).pack()
        
        # Search
        search_frame = tk.Frame(self.popup, bg='white', padx=20, pady=10)
        search_frame.pack(fill='x')
        
        self.search_var = tk.StringVar()
        tk.Entry(search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            bd=2,
            relief='solid').pack(fill='x', ipady=5)
        
        self.search_var.trace_add('write', lambda *args: self.search_books())
        
        # Books list
        list_frame = tk.Frame(self.popup, bg='white', padx=20, pady=10)
        list_frame.pack(fill='both', expand=True)
        
        scroll_y = ttk.Scrollbar(list_frame, orient='vertical')
        
        style = ttk.Style()
        style.configure("Select.Treeview",
            font=('Segoe UI', 10),
            rowheight=30)
        
        self.books_tree = ttk.Treeview(list_frame,
            columns=("ID", "Code", "Name", "Price", "Stock"),
            show='headings',
            yscrollcommand=scroll_y.set,
            style="Select.Treeview")
        
        scroll_y.config(command=self.books_tree.yview)
        
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Code", text="Mã Sách")
        self.books_tree.heading("Name", text="Tên Sách")
        self.books_tree.heading("Price", text="Giá Bìa")
        self.books_tree.heading("Stock", text="Tồn Kho")
        
        self.books_tree.column("ID", width=50, anchor='center')
        self.books_tree.column("Code", width=100, anchor='center')
        self.books_tree.column("Name", width=300, anchor='w')
        self.books_tree.column("Price", width=100, anchor='e')
        self.books_tree.column("Stock", width=80, anchor='center')
        
        self.books_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        
        self.books_tree.bind('<Double-1>', lambda e: self.select_book())
        
        # Quantity
        qty_frame = tk.Frame(self.popup, bg='white', padx=20, pady=10)
        qty_frame.pack(fill='x')
        
        tk.Label(qty_frame,
            text="Số lượng:",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(side='left', padx=(0, 10))
        
        self.qty_var = tk.StringVar(value="1")
        tk.Entry(qty_frame,
            textvariable=self.qty_var,
            font=('Segoe UI', 11),
            width=10,
            bd=2,
            relief='solid').pack(side='left')
        
        # Buttons
        btn_frame = tk.Frame(self.popup, bg='white', padx=20, pady=15)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame,
            text="✅ Thêm vào giỏ",
            command=self.select_book,
            font=('Segoe UI', 10, 'bold'),
            bg=colors['success'],
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame,
            text="❌ Đóng",
            command=self.popup.destroy,
            font=('Segoe UI', 10, 'bold'),
            bg='#757575',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack(side='left', padx=5)
    
    def load_books(self):
        """Load danh sách sách"""
        books = self.db.view_all()
        inventory = self.db.view_inventory()
        
        # Map inventory
        inv_map = {inv[0]: inv[3] for inv in inventory}  # {book_id: quantity}
        
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        for book in books:
            book_id = book[0]
            stock = inv_map.get(book_id, 0)
            
            self.books_tree.insert('', 'end',
                values=(book_id, book[1], book[2], format_currency(book[8]), stock))
    
    def search_books(self):
        """Tìm kiếm sách"""
        keyword = self.search_var.get().lower()
        
        if not keyword:
            self.load_books()
            return
        
        books = self.db.search_book(keyword)
        inventory = self.db.view_inventory()
        inv_map = {inv[0]: inv[3] for inv in inventory}
        
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        for book in books:
            book_id = book[0]
            stock = inv_map.get(book_id, 0)
            
            self.books_tree.insert('', 'end',
                values=(book_id, book[1], book[2], format_currency(book[8]), stock))
    
    def select_book(self):
        """Chọn sách"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng chọn sách!")
            return
        
        item = self.books_tree.item(selection[0])
        values = item['values']
        
        try:
            quantity = int(self.qty_var.get())
            if quantity <= 0:
                messagebox.showerror("Lỗi", "❌ Số lượng phải lớn hơn 0!")
                return
            
            # Kiểm tra tồn kho
            stock = int(values[4])
            if quantity > stock:
                messagebox.showerror("Lỗi",
                    f"❌ Không đủ hàng trong kho!\n"
                    f"Tồn kho: {stock} quyển\n"
                    f"Bạn muốn: {quantity} quyển")
                return
            
            # Parse price
            price_str = values[3].replace('đ', '').replace('.', '').replace(',', '').strip()
            unit_price = float(price_str)
            
            # Add to cart
            self.order_popup.add_to_cart(
                values[0],  # book_id
                values[1],  # book_code
                values[2],  # book_name
                quantity,
                unit_price
            )
            
            messagebox.showinfo("Thành công",
                f"✅ Đã thêm {quantity} quyển '{values[2]}' vào giỏ!")
            
        except ValueError:
            messagebox.showerror("Lỗi", "❌ Số lượng không hợp lệ!")


# ========== POPUP CHI TIẾT ĐƠN HÀNG ==========
class OrderDetailPopup:
    """Popup xem chi tiết đơn hàng"""
    
    def __init__(self, parent, db, order):
        self.db = db
        self.order = order
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("📋 Chi tiết đơn hàng")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 650, 700)
        self.popup.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        colors = {
            'primary': '#1976D2',
            'success': '#4CAF50',
            'info': '#00BCD4'
        }
        
        # Header
        header = tk.Frame(self.popup, bg=colors['primary'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="📋 CHI TIẾT ĐƠN HÀNG",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg=colors['primary']).pack()
        
        # Main container with scrollbar
        main_container = tk.Frame(self.popup, bg='white')
        main_container.pack(fill='both', expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        content = tk.Frame(scrollable_frame, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        order_id, code, customer, phone, email, address, date, amount, status, created_by = self.order
        
        # Order info
        info_items = [
            ("📝 Mã đơn hàng:", code),
            ("📅 Ngày tạo:", date),
            ("👤 Khách hàng:", customer),
            ("📞 Số điện thoại:", phone),
            ("📧 Email:", email or "(Không có)"),
            ("🏠 Địa chỉ:", address or "(Không có)"),
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
                anchor='w').pack(side='left', fill='x', expand=True)
        
        # Separator
        tk.Frame(content, height=2, bg='#eee').pack(fill='x', pady=15)
        
        # Order details
        tk.Label(content,
            text="📚 Danh sách sách:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=colors['primary']).pack(anchor='w', pady=(0, 10))
        
        details = self.db.get_order_details(order_id)
        
        details_frame = tk.Frame(content, bg='#f9f9f9', relief='solid', bd=1)
        details_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        for i, detail in enumerate(details, 1):
            item_frame = tk.Frame(details_frame, bg='white', pady=8, padx=15)
            item_frame.pack(fill='x', pady=1)
            
            tk.Label(item_frame,
                text=f"{i}. {detail['BookName']} ({detail['BookCode']})",
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                anchor='w').pack(fill='x')
            
            detail_text = f"   SL: {detail['Quantity']}  |  Đơn giá: {format_currency(detail['UnitPrice'])}  |  Thành tiền: {format_currency(detail['Subtotal'])}"
            tk.Label(item_frame,
                text=detail_text,
                font=('Segoe UI', 9),
                bg='white',
                fg='#666',
                anchor='w').pack(fill='x')
        
        # Total
        total_frame = tk.Frame(content, bg='#E8F5E9', padx=15, pady=12, relief='solid', bd=1)
        total_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(total_frame,
            text="💰 Tổng tiền:",
            font=('Segoe UI', 12, 'bold'),
            bg='#E8F5E9',
            fg=colors['success']).pack(side='left')
        
        tk.Label(total_frame,
            text=format_currency(amount),
            font=('Segoe UI', 18, 'bold'),
            bg='#E8F5E9',
            fg=colors['success']).pack(side='right')
        
        # Status
        status_frame = tk.Frame(content, bg='white')
        status_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(status_frame,
            text="📊 Trạng thái:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            width=18,
            anchor='w').pack(side='left')
        
        if status == 'Hoàn thành':
            status_text = '✅ Hoàn thành'
            status_color = colors['success']
        elif status == 'Đang xử lý':
            status_text = '⏳ Đang xử lý'
            status_color = '#FF9800'
        elif status == 'Đã hủy':
            status_text = '❌ Đã hủy'
            status_color = '#F44336'
        else:
            status_text = f'📦 {status}'
            status_color = colors['info']
        
        tk.Label(status_frame,
            text=status_text,
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=status_color).pack(side='left')
        
        # Creator info
        tk.Label(content,
            text=f"👤 Người tạo: {created_by}",
            font=('Segoe UI', 9, 'italic'),
            bg='white',
            fg='#999').pack(anchor='w', pady=(5, 0))
        
        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Footer with button
        footer = tk.Frame(self.popup, bg='white', pady=15)
        footer.pack(fill='x')
        
        tk.Button(footer,
            text="✅ Đóng",
            command=self.popup.destroy,
            font=('Segoe UI', 11, 'bold'),
            bg=colors['info'],
            fg='white',
            bd=0,
            padx=40,
            pady=10,
            cursor='hand2').pack()



# ========== POPUP SỬA ĐƠN HÀNG ==========
class EditOrderPopup:
    """Popup sửa đơn hàng"""
    
    def __init__(self, parent, main_app, db, order):
        self.main_app = main_app
        self.db = db
        self.order = order
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("📝 Sửa đơn hàng")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 500, 400)
        
        self.status_var = tk.StringVar(value=order[8])
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        colors = self.main_app.colors
        
        # Header
        header = tk.Frame(self.popup, bg=colors['warning'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="📝 SỬA ĐƠN HÀNG",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['warning']).pack()
        
        # Content
        content = tk.Frame(self.popup, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        tk.Label(content,
            text=f"Đơn hàng: {self.order[1]}",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg=colors['primary']).pack(pady=(0, 10))
        
        tk.Label(content,
            text=f"Khách hàng: {self.order[2]}",
            font=('Segoe UI', 10),
            bg='white').pack(pady=(0, 20))
        
        # Status
        tk.Label(content,
            text="Trạng thái:",
            font=('Segoe UI', 11, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 10))
        
        statuses = ["Đang xử lý", "Hoàn thành", "Đã hủy"]
        
        for status in statuses:
            tk.Radiobutton(content,
                text=status,
                variable=self.status_var,
                value=status,
                font=('Segoe UI', 10),
                bg='white').pack(anchor='w', pady=5)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x', pady=(30, 0))
        
        tk.Button(btn_frame,
            text="✅ Cập nhật",
            command=self.confirm_update,
            font=('Segoe UI', 11, 'bold'),
            bg=colors['success'],
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2').pack(side='left', padx=(0, 10), expand=True, fill='x')
        
        tk.Button(btn_frame,
            text="❌ Hủy",
            command=self.popup.destroy,
            font=('Segoe UI', 11, 'bold'),
            bg='#757575',
            fg='white',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2').pack(side='left', expand=True, fill='x')
    
    def confirm_update(self):
        """Xác nhận cập nhật"""
        new_status = self.status_var.get()
        
        if new_status == self.order[8]:
            messagebox.showinfo("Thông báo", "ℹ️ Trạng thái không thay đổi!")
            return
        
        success, msg = self.db.update_order_status(self.order[0], new_status)
        
        if success:
            messagebox.showinfo("Thành công",
                f"✅ Đã cập nhật trạng thái thành '{new_status}'!")
            self.popup.destroy()
            self.main_app.load_orders()
        else:
            messagebox.showerror("Lỗi", f"❌ {msg}")


# ========== POPUP TÌM KIẾM ĐƠN HÀNG ==========
class SearchOrderPopup:
    """Popup tìm kiếm đơn hàng"""
    
    def __init__(self, parent, main_app, db):
        self.main_app = main_app
        self.db = db
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("🔍 Tìm kiếm đơn hàng")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 900, 500)
        
        self.search_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        colors = self.main_app.colors
        
        # Header
        header = tk.Frame(self.popup, bg=colors['warning'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="🔍 TÌM KIẾM ĐƠN HÀNG",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['warning']).pack()
        
        # Search
        search_frame = tk.Frame(self.popup, bg='white', padx=20, pady=15)
        search_frame.pack(fill='x')
        
        tk.Label(search_frame,
            text="Nhập từ khóa (Mã đơn, Tên khách, SĐT):",
            font=('Segoe UI', 10, 'bold'),
            bg='white').pack(anchor='w', pady=(0, 5))
        
        search_entry = tk.Entry(search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 12),
            bd=2,
            relief='solid')
        search_entry.pack(fill='x', ipady=8)
        search_entry.focus()
        
        # Results
        results_container = tk.Frame(self.popup, bg='white', padx=20, pady=10)
        results_container.pack(fill='both', expand=True)
        
        scroll_y = ttk.Scrollbar(results_container, orient='vertical')
        
        self.results_tree = ttk.Treeview(results_container,
            columns=("ID", "Code", "Date", "Customer", "Phone", "Amount", "Status"),
            show='headings',
            yscrollcommand=scroll_y.set,
            style="Business.Treeview")
        
        scroll_y.config(command=self.results_tree.yview)
        
        columns = [
            ("ID", 50, 'center'),
            ("Code", 100, 'center'),
            ("Date", 110, 'center'),
            ("Customer", 150, 'w'),
            ("Phone", 120, 'center'),
            ("Amount", 120, 'e'),
            ("Status", 120, 'center')
        ]
        
        for col, width, anchor in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=width, anchor=anchor)
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        
        self.search_var.trace_add('write', lambda *args: self.do_search())
        self.results_tree.bind('<Double-1>', lambda e: self.select_order())
        
        # Buttons
        btn_frame = tk.Frame(self.popup, bg='white', padx=20, pady=15)
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame,
            text="✅ Chọn",
            command=self.select_order,
            font=('Segoe UI', 10, 'bold'),
            bg=colors['success'],
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame,
            text="❌ Đóng",
            command=self.popup.destroy,
            font=('Segoe UI', 10, 'bold'),
            bg='#757575',
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2').pack(side='left', padx=5)
    
    def do_search(self):
        """Thực hiện tìm kiếm"""
        keyword = self.search_var.get().strip()
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        if not keyword:
            return
        
        results = self.db.search_orders(keyword)
        
        for order in results:
            order_id, code, customer, phone, email, address, date, amount, status, created_by = order
            
            if status == 'Hoàn thành':
                status_text = '✅ Hoàn thành'
            elif status == 'Đang xử lý':
                status_text = '⏳ Đang xử lý'
            else:
                status_text = f'❌ {status}'
            
            self.results_tree.insert('', 'end',
                values=(order_id, code, date, customer, phone, format_currency(amount), status_text))
    
    def select_order(self):
        """Chọn đơn"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng chọn đơn hàng!")
            return
        
        item = self.results_tree.item(selection[0])
        values = item['values']
        
        self.main_app.selected_order = values[0]
        
        # Highlight trong bảng chính
        for item_id in self.main_app.orders_tree.get_children():
            item_values = self.main_app.orders_tree.item(item_id)['values']
            if str(item_values[0]) == str(values[0]):
                self.main_app.orders_tree.selection_set(item_id)
                self.main_app.orders_tree.see(item_id)
                break
        
        self.popup.destroy()
        
        messagebox.showinfo("Đã chọn",
            f"✅ Đã chọn đơn hàng: {values[1]}\n"
            f"💡 Bạn có thể xem chi tiết, sửa hoặc hủy đơn")


# ========== POPUP BÁO CÁO ==========
class ReportPopup:
    """Popup báo cáo doanh thu"""
    
    def __init__(self, parent, db):
        self.db = db
        
        self.popup = tk.Toplevel(parent)
        self.popup.title("📈 Báo cáo doanh thu")
        self.popup.transient(parent)
        self.popup.grab_set()
        center_window(self.popup, 700, 650)
        
        self.setup_ui()
        self.load_report()
    
    def setup_ui(self):
        """Setup UI"""
        colors = {
            'primary': '#1976D2',
            'success': '#4CAF50',
            'purple': '#9C27B0'
        }
        
        # Header
        header = tk.Frame(self.popup, bg=colors['purple'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header,
            text="📈 BÁO CÁO DOANH THU",
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=colors['purple']).pack()
        
        # Content
        self.content = tk.Frame(self.popup, bg='white', padx=30, pady=20)
        self.content.pack(fill='both', expand=True)
    
    def load_report(self):
        """Load báo cáo"""
        stats = self.db.get_revenue_stats()
        top_books = self.db.get_top_selling_books(5)
        
        colors = {
            'primary': '#1976D2',
            'success': '#4CAF50',
            'purple': '#9C27B0',
            'warning': '#FF9800'
        }
        
        # Statistics
        tk.Label(self.content,
            text="📊 THỐNG KÊ TỔNG QUAN",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg=colors['primary']).pack(anchor='w', pady=(0, 15))
        
        stats_frame = tk.Frame(self.content, bg='#f9f9f9', relief='solid', bd=1, padx=20, pady=15)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stat_items = [
            ("📦 Tổng đơn hàng:", f"{stats['TotalOrders']} đơn"),
            ("✅ Đơn hoàn thành:", f"{stats['CompletedOrders']} đơn ({stats['CompletedOrders']/stats['TotalOrders']*100 if stats['TotalOrders'] > 0 else 0:.0f}%)"),
            ("⏳ Đơn đang xử lý:", f"{stats['ProcessingOrders']} đơn ({stats['ProcessingOrders']/stats['TotalOrders']*100 if stats['TotalOrders'] > 0 else 0:.0f}%)"),
            ("💰 Tổng doanh thu:", format_currency(stats['TotalRevenue'])),
            ("📊 Doanh thu TB/đơn:", format_currency(stats['AvgRevenue'])),
        ]
        
        for label, value in stat_items:
            row = tk.Frame(stats_frame, bg='#f9f9f9')
            row.pack(fill='x', pady=3)
            
            tk.Label(row,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='#f9f9f9',
                width=20,
                anchor='w').pack(side='left')
            
            tk.Label(row,
                text=value,
                font=('Segoe UI', 10),
                bg='#f9f9f9',
                fg=colors['success']).pack(side='left')
        
        # Top books
        tk.Label(self.content,
            text="📚 SÁCH BÁN CHẠY",
            font=('Segoe UI', 13, 'bold'),
            bg='white',
            fg=colors['primary']).pack(anchor='w', pady=(10, 15))
        
        # Container với scrollbar
        books_container = tk.Frame(self.content, bg='white')
        books_container.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(books_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(books_container, orient='vertical', command=canvas.yview)
        books_frame = tk.Frame(canvas, bg='white')
        
        books_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=books_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for i, book in enumerate(top_books, 1):
            book_frame = tk.Frame(books_frame, bg='#f9f9f9', pady=10, padx=15)
            book_frame.pack(fill='x', pady=2)
            
            tk.Label(book_frame,
                text=f"{i}. {book['BookName']} ({book['BookCode']})",
                font=('Segoe UI', 10, 'bold'),
                bg='#f9f9f9',
                anchor='w').pack(fill='x')
            
            tk.Label(book_frame,
                text=f"   Đã bán: {book['QuantitySold']} quyển  |  Doanh thu: {format_currency(book['Revenue'])}",
                font=('Segoe UI', 9),
                bg='#f9f9f9',
                fg='#666',
                anchor='w').pack(fill='x')
        
        # Button
        tk.Button(self.content,
            text="✅ Đóng",
            command=self.popup.destroy,
            font=('Segoe UI', 11, 'bold'),
            bg=colors['success'],
            fg='white',
            bd=0,
            padx=40,
            pady=12,
            cursor='hand2').pack(pady=(20, 0))