# gui/register_window.py - Cửa sổ đăng ký
import tkinter as tk
from tkinter import ttk, messagebox
from database.user_manager import UserManager

class RegisterWindow:
    def __init__(self, master, login_window_instance):
        self.master = master
        self.login_window = login_window_instance
        self.user_manager = UserManager()
        
        master.title("📝 Đăng Ký Tài Khoản")
        master.geometry("500x600")
        self.center_window(500, 600)
        master.resizable(False, False)
        master.grab_set()  # Modal window
        
        # Biến điều khiển
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        self.full_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        
        self.setup_styles()
        self.setup_widgets()
    
    def center_window(self, w, h):
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.master.geometry(f'{w}x{h}+{x}+{y}')
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("RegisterHeader.TLabel", font=('Arial', 20, 'bold'), foreground="#4CAF50")
        style.configure("TLabel", font=('Arial', 11))
        style.configure("TEntry", font=('Arial', 11))
        style.configure("Register.TButton", font=('Arial', 12, 'bold'), padding=10, background="#4CAF50", foreground="white")
        style.map("Register.TButton", background=[('active', '#43A047')])
        style.configure("Cancel.TButton", font=('Arial', 11), padding=8, background="#9E9E9E", foreground="white")
        style.map("Cancel.TButton", background=[('active', '#757575')])
    
    def setup_widgets(self):
        main_frame = ttk.Frame(self.master, padding="30 20 30 20")
        main_frame.pack(expand=True, fill='both')
        
        # Header
        ttk.Label(main_frame, text="🎯 TẠO TÀI KHOẢN MỚI", style="RegisterHeader.TLabel").pack(pady=(0, 30))
        
        # Form đăng ký
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill='x', pady=10)
        
        fields = [
            ("👤 Tên đăng nhập:", self.username_var, False),
            ("🔒 Mật khẩu:", self.password_var, True),
            ("🔒 Nhập lại mật khẩu:", self.confirm_password_var, True),
            ("📛 Họ và tên:", self.full_name_var, False),
            ("📧 Email:", self.email_var, False),
        ]
        
        for i, (label_text, var, is_password) in enumerate(fields):
            # Label
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky='w', pady=10, padx=(0, 10))
            
            # Entry
            entry = ttk.Entry(form_frame, textvariable=var, width=30, font=('Arial', 11))
            if is_password:
                entry.config(show='*')
            entry.grid(row=i, column=1, sticky='ew', pady=10)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Ghi chú
        note_frame = ttk.Frame(main_frame)
        note_frame.pack(fill='x', pady=15)
        
        ttk.Label(note_frame, text="ℹ️ Lưu ý:", font=('Arial', 10, 'bold'), foreground="#FF9800").pack(anchor='w')
        ttk.Label(note_frame, text="• Tên đăng nhập không được trùng", font=('Arial', 9), foreground="#666").pack(anchor='w', padx=20)
        ttk.Label(note_frame, text="• Mật khẩu tối thiểu 6 ký tự", font=('Arial', 9), foreground="#666").pack(anchor='w', padx=20)
        ttk.Label(note_frame, text="• Họ tên và Email là tùy chọn", font=('Arial', 9), foreground="#666").pack(anchor='w', padx=20)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        
        ttk.Button(button_frame, text="✅ ĐĂNG KÝ", command=self.register, style="Register.TButton").pack(side='left', expand=True, fill='x', padx=(0, 5))
        ttk.Button(button_frame, text="❌ HỦY", command=self.master.destroy, style="Cancel.TButton").pack(side='left', expand=True, fill='x', padx=(5, 0))
        
        # Bind Enter key
        self.master.bind('<Return>', lambda e: self.register())
    
    def validate_input(self):
        """Kiểm tra dữ liệu nhập vào"""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        # Kiểm tra username
        if not username:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập!")
            return False
        
        if len(username) < 3:
            messagebox.showwarning("Cảnh báo", "Tên đăng nhập phải có ít nhất 3 ký tự!")
            return False
        
        # Kiểm tra mật khẩu
        if not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu!")
            return False
        
        if len(password) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu phải có ít nhất 6 ký tự!")
            return False
        
        # Kiểm tra xác nhận mật khẩu
        if password != confirm_password:
            messagebox.showwarning("Cảnh báo", "Mật khẩu nhập lại không khớp!")
            return False
        
        return True
    
    def register(self):
        """Xử lý đăng ký"""
        if not self.validate_input():
            return
        
        username = self.username_var.get().strip()
        password = self.password_var.get()
        full_name = self.full_name_var.get().strip()
        email = self.email_var.get().strip()
        
        # Thực hiện đăng ký
        success, message = self.user_manager.register_user(
            username=username,
            password=password,
            full_name=full_name if full_name else username,
            email=email
        )
        
        if success:
            messagebox.showinfo("Thành công", f"Đăng ký thành công!\nTên đăng nhập: {username}\n\nBạn có thể đăng nhập ngay bây giờ.")
            # Tự động điền username vào form đăng nhập
            self.login_window.username_var.set(username)
            self.master.destroy()
        else:
            messagebox.showerror("Lỗi", message)