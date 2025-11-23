# ============================================================
# FILE: utils/__init__.py
# MỤC ĐÍCH: Export các hàm tiện ích từ module helpers
# ============================================================

from .helpers import (
    center_window,
    format_currency,
    format_number,
    validate_positive_number,
    validate_year,
    validate_not_empty,
    get_stock_status,
    truncate_text,
    calculate_profit,
    calculate_profit_margin,
    format_phone_number,
    validate_email,
    get_color_scheme,
    show_success,
    show_error,
    show_warning,
    show_info
)

def validate_number(value):
    """
    KIỂM TRA SỐ HỢP LỆ (backward compatibility với code cũ)
    
    Tham số:
        value: Giá trị cần kiểm tra
    
    Trả về:
        bool: True nếu là số hợp lệ
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

__all__ = [
    'center_window',
    'format_currency',
    'format_number',
    'validate_number',
    'validate_positive_number',
    'validate_year',
    'validate_not_empty',
    'get_stock_status',
    'validate_email'
]