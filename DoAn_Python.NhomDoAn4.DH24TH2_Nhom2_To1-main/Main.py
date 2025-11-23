# ============================================================
# FILE: main.py
# MỤC ĐÍCH: Điểm khởi chạy chính của ứng dụng
# ============================================================

import tkinter as tk
from gui.login_window import LoginWindow
from gui.main_menu import MainMenuWindow
from connection_manager import getDbConnection

if __name__ == '__main__':
    """
    KHỞI CHẠY ỨNG DỤNG
    
    Quy trình:
        1. Tạo cửa sổ Tkinter root
        2. Khởi tạo màn hình đăng nhập
        3. Truyền MainMenuWindow và getDbConnection vào
        4. Chạy vòng lặp sự kiện Tkinter
    """
    root = tk.Tk()
    login_app = LoginWindow(root, MainMenuWindow, getDbConnection)
    root.mainloop()