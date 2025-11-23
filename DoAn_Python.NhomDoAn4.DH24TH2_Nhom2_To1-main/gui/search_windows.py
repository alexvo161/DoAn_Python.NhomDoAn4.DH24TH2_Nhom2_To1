# ============================================================
# FILE: gui/search_windows.py  
# MỤC ĐÍCH: Cửa sổ tìm kiếm sách và tồn kho
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
from utils.helpers import center_window

class SearchWindow:
    """Cửa sổ tìm kiếm sách - Dùng cho Book Manager"""
    
    def __init__(self, master, main_app_instance):
        self.master = master
        self.main_app = main_app_instance
        self.db = main_app_instance.db
        
        master.title("🔍 TÌM KIẾM SÁCH")
        master.transient(main_app_instance.master)
        master.grab_set()
        center_window(master, 700, 500)
        master.resizable(False, False)
        
        self.search_text = tk.StringVar()
        self.setup_widgets()
    
    def setup_widgets(self):
        # Styles
        style = ttk.Style()
        style.configure("SearchHeader.TLabel", 
            font=('Segoe UI', 14, 'bold'), 
            foreground="#1976D2")
        
        # Main frame
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Header
        ttk.Label(main_frame, 
            text="🔍 TÌM KIẾM NHANH", 
            style="SearchHeader.TLabel").pack(pady=(0, 15))
        
        # Search box
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(search_frame, 
            text="Nhập từ khóa (Mã sách, Tên sách, Tác giả):",
            font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        search_entry = ttk.Entry(search_frame, 
            textvariable=self.search_text,
            font=('Segoe UI', 11))
        search_entry.pack(fill='x', ipady=5)
        search_entry.focus()
        
        # Auto-search khi gõ
        self.search_text.trace_add("write", self.update_suggestions)
        self.master.bind('<Return>', lambda e: self.select_first_suggestion())
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        
        # Results tree
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        
        self.results_tree = ttk.Treeview(tree_frame,
            columns=("ID", "MaSach", "TenSach", "TacGia"),
            show='headings',
            height=12,
            yscrollcommand=scroll_y.set)
        
        scroll_y.config(command=self.results_tree.yview)
        
        # Columns
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("MaSach", text="Mã Sách")
        self.results_tree.heading("TenSach", text="Tên Sách")
        self.results_tree.heading("TacGia", text="Tác Giả")
        
        self.results_tree.column("ID", width=50, anchor='center')
        self.results_tree.column("MaSach", width=100, anchor='center')
        self.results_tree.column("TenSach", width=300, anchor='w')
        self.results_tree.column("TacGia", width=150, anchor='w')
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        
        self.results_tree.bind('<Double-1>', lambda e: self.select_first_suggestion())
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame,
            text="✅ Chọn",
            command=self.select_first_suggestion).pack(side='left', padx=5)
        
        ttk.Button(btn_frame,
            text="❌ Đóng",
            command=self.master.destroy).pack(side='left')
        
        # Status
        self.status_label = ttk.Label(main_frame,
            text="Nhập từ khóa để tìm kiếm...",
            font=('Segoe UI', 9),
            foreground="#666")
        self.status_label.pack(pady=(10, 0))
    
    def update_suggestions(self, *args):
        """Cập nhật gợi ý khi gõ"""
        query = self.search_text.get().strip()
        
        # Clear tree
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        if not query or len(query) < 2:
            self.status_label.config(text="Nhập ít nhất 2 ký tự...")
            return
        
        # Search
        try:
            results = self.db.search_for_suggestion(query)
            
            if results:
                for row in results:
                    book_id = row[0]
                    ma_sach = row[1]
                    ten_sach = row[2]
                    tac_gia = row[3]
                    
                    self.results_tree.insert('', 'end',
                        values=(book_id, ma_sach, ten_sach, tac_gia))
                
                self.status_label.config(
                    text=f"✅ Tìm thấy {len(results)} kết quả",
                    foreground="#4CAF50")
            else:
                self.status_label.config(
                    text="❌ Không tìm thấy kết quả",
                    foreground="#F44336")
        
        except Exception as e:
            self.status_label.config(
                text=f"Lỗi: {str(e)}",
                foreground="#F44336")
    
    def select_first_suggestion(self):
        """Chọn kết quả đầu tiên"""
        selection = self.results_tree.selection()
        
        if selection:
            item = self.results_tree.item(selection[0])
            values = item['values']
            book_id = values[0]
            
            # Load vào form chính
            book = self.db.get_book_by_id(book_id)
            if book:
                self.main_app.selected_book = book
                self.main_app.load_book_to_form(book)
                self.master.destroy()
        else:
            messagebox.showwarning("Cảnh báo", 
                "Vui lòng chọn một kết quả từ danh sách!")


class InventorySearchWindow:
    """Cửa sổ tìm kiếm kho - Dùng cho Inventory Manager"""
    
    def __init__(self, master, main_app_instance, db):
        self.master = master
        self.main_app = main_app_instance
        self.db = db
        
        master.title("🔍 TÌM KIẾM TRONG KHO")
        master.transient(main_app_instance.master)
        master.grab_set()
        center_window(master, 700, 500)
        master.resizable(False, False)
        
        self.search_text = tk.StringVar()
        self.setup_widgets()
    
    def setup_widgets(self):
        # Styles
        style = ttk.Style()
        style.configure("SearchHeader.TLabel", 
            font=('Segoe UI', 14, 'bold'), 
            foreground="#FF9800")
        
        # Main frame
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Header
        ttk.Label(main_frame, 
            text="🔍 TÌM KIẾM TRONG KHO", 
            style="SearchHeader.TLabel").pack(pady=(0, 15))
        
        # Search box
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(search_frame, 
            text="Nhập từ khóa (Mã sách hoặc Tên sách):",
            font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        search_entry = ttk.Entry(search_frame, 
            textvariable=self.search_text,
            font=('Segoe UI', 11))
        search_entry.pack(fill='x', ipady=5)
        search_entry.focus()
        
        # Auto-search
        self.search_text.trace_add("write", self.update_suggestions)
        self.master.bind('<Return>', lambda e: self.select_and_close())
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        
        # Results tree
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        
        self.results_tree = ttk.Treeview(tree_frame,
            columns=("ID", "MaSach", "TenSach", "SoLuong", "ViTri"),
            show='headings',
            height=12,
            yscrollcommand=scroll_y.set)
        
        scroll_y.config(command=self.results_tree.yview)
        
        # Columns
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("MaSach", text="Mã Sách")
        self.results_tree.heading("TenSach", text="Tên Sách")
        self.results_tree.heading("SoLuong", text="SL Tồn")
        self.results_tree.heading("ViTri", text="Vị Trí")
        
        self.results_tree.column("ID", width=50, anchor='center')
        self.results_tree.column("MaSach", width=100, anchor='center')
        self.results_tree.column("TenSach", width=280, anchor='w')
        self.results_tree.column("SoLuong", width=80, anchor='center')
        self.results_tree.column("ViTri", width=90, anchor='center')
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        
        self.results_tree.bind('<Double-1>', lambda e: self.select_and_close())
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame,
            text="✅ Chọn",
            command=self.select_and_close).pack(side='left', padx=5)
        
        ttk.Button(btn_frame,
            text="❌ Đóng",
            command=self.master.destroy).pack(side='left')
        
        # Status
        self.status_label = ttk.Label(main_frame,
            text="Nhập từ khóa để tìm kiếm...",
            font=('Segoe UI', 9),
            foreground="#666")
        self.status_label.pack(pady=(10, 0))
    
    def update_suggestions(self, *args):
        """Cập nhật gợi ý"""
        query = self.search_text.get().strip()
        
        # Clear
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        if not query or len(query) < 2:
            self.status_label.config(text="Nhập ít nhất 2 ký tự...")
            return
        
        # Search
        try:
            results = self.db.search_inventory_for_suggestion(query)
            
            if results:
                for row in results:
                    book_id, ma_sach, ten_sach, so_luong, vi_tri = row
                    
                    self.results_tree.insert('', 'end',
                        values=(book_id, ma_sach, ten_sach, f"{so_luong:,}", vi_tri))
                
                self.status_label.config(
                    text=f"✅ Tìm thấy {len(results)} kết quả",
                    foreground="#4CAF50")
            else:
                self.status_label.config(
                    text="❌ Không tìm thấy kết quả",
                    foreground="#F44336")
        
        except Exception as e:
            self.status_label.config(
                text=f"Lỗi: {str(e)}",
                foreground="#F44336")
    
    def select_and_close(self):
        """Chọn và đóng"""
        selection = self.results_tree.selection()
        
        if not selection:
            # Nếu không chọn, lấy dòng đầu tiên
            children = self.results_tree.get_children()
            if children:
                self.results_tree.selection_set(children[0])
                selection = self.results_tree.selection()
            else:
                messagebox.showwarning("Cảnh báo", 
                    "⚠️ Vui lòng chọn một kết quả từ danh sách!")
                return
        
        item = self.results_tree.item(selection[0])
        values = item['values']
        
        # Load vào form inventory
        self.main_app.selected_inventory_record = (
            values[0],  # ID
            values[1],  # MaSach
            values[2],  # TenSach
            int(str(values[3]).replace(',', '')),  # SoLuong
            values[4]   # ViTri
        )
        
        # Highlight trong bảng chính
        for item_id in self.main_app.inventory_tree.get_children():
            item_values = self.main_app.inventory_tree.item(item_id)['values']
            if str(item_values[0]) == str(values[0]):
                self.main_app.inventory_tree.selection_set(item_id)
                self.main_app.inventory_tree.see(item_id)
                break
        
        self.master.destroy()
        
        # Hiển thị thông báo
        messagebox.showinfo("Đã chọn", 
            f"✅ Đã chọn: {values[2]}\n"
            f"📦 Tồn kho: {values[3]} quyển\n"
            f"📍 Vị trí: {values[4]}\n\n"
            f"💡 Bạn có thể click [➕ NHẬP KHO] hoặc [➖ XUẤT KHO]")