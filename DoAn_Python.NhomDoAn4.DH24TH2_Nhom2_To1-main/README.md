# HE THONG QUAN LY NHA SACH

**Phien ban:** 1.0.0  
**Tac gia:** Duong Gia Phu - Vo Hai Quan
**Ngay hoan thanh:** 18/11/2025  
**Cong nghe:** Python 3.x + SQL Server + Tkinter

---

## MUC LUC

1. [Tong quan](#tong-quan)
2. [Cong nghe](#cong-nghe)
3. [Co so du lieu](#co-so-du-lieu)
4. [Chuc nang](#chuc-nang)
5. [Cai dat](#cai-dat)
6. [Huong dan su dung](#huong-dan-su-dung)
7. [Cau truc thu muc](#cau-truc-thu-muc)
8. [Luong hoat dong](#luong-hoat-dong)

---

## TONG QUAN

He thong quan ly nha sach la ung dung desktop giup quan ly:
- Thong tin sach, tac gia, nha xuat ban
- Ton kho, nhap xuat hang
- Don hang va khach hang
- Thong ke doanh thu

**Dac diem:**
- Giao dien don gian, de su dung
- Luu tru du lieu tren SQL Server
- Bao mat voi ma hoa password
- Phan quyen user va admin
- Theo doi lich su giao dich

---

## CONG NGHE

**Ngon ngu lap trinh:**
- Python 3.8+

**Co so du lieu:**
- SQL Server 2022

**Thu vien Python:**
- tkinter (GUI)
- pyodbc (ket noi SQL Server)
- hashlib (ma hoa password)
- secrets (tao salt)

---

## CO SO DU LIEU

### Cac bang chinh:

**1. Sach**
- Luu thong tin sach: ma, ten, tac gia, gia, nam xuat ban
- Lien ket voi TacGia, LinhVuc, NhaXuatBan

**2. TonKho**
- Quan ly so luong ton kho cua tung sach
- Vi tri luu kho

**3. DonHang**
- Thong tin don hang: ma don, khach hang, tong tien
- Trang thai: Dang xu ly, Hoan thanh, Da huy
- Nguoi tao don (username)

**4. ChiTietDonHang**
- Chi tiet sach trong don hang
- So luong, don gia, thanh tien

**5. Users**
- Tai khoan nguoi dung
- Password duoc ma hoa (SHA256 + Salt)
- Phan quyen: admin hoac user

**6. NhapXuatKho**
- Lich su nhap/xuat kho
- Theo doi nguoi thuc hien

**Bang phu:**
- TacGia (tac gia)
- LinhVuc (the loai sach)
- NhaXuatBan (nha xuat ban)

### So do lien ket:

```
TacGia ----+
           |
LinhVuc ---+---> Sach ---> TonKho
           |        |
NhaXuatBan +        +---> NhapXuatKho
                    |
                    +---> ChiTietDonHang ---> DonHang
                                               |
Users -------------------------------------> NguoiTao
```

---

## CHUC NANG

### 1. QUAN LY NGUOI DUNG

**Dang nhap:**
- Nhap username va password
- Xac thuc voi SQL Server
- Hien thi menu theo phan quyen

**Dang ky:**
- Tao tai khoan moi
- Tu dong ma hoa password
- Gan quyen: user hoac admin

**Doi mat khau:**
- Nhap mat khau cu va moi
- Tu dong ma hoa lai

### 2. QUAN LY SACH

**Them sach:**
- Nhap thong tin sach day du
- Tu dong tao ma sach (MS001, MS002...)
- Tu dong tao dong ton kho

**Sua sach:**
- Chon sach can sua
- Cap nhat thong tin
- Luu lich su cap nhat

**Xoa sach:**
- Xoa sach va ton kho lien quan
- Kiem tra da co trong don hang chua

**Tim kiem:**
- Tim theo ma sach, ten sach
- Tim theo tac gia, the loai

**Xem danh sach:**
- Hien thi tat ca sach
- Sap xep theo thu tu

### 3. QUAN LY KHO

**Nhap kho:**
- Chon sach can nhap
- Nhap so luong
- Cap nhat ton kho
- Luu lich su nhap kho

**Xuat kho:**
- Chon sach can xuat
- Nhap so luong
- Kiem tra ton kho du hay khong
- Cap nhat ton kho
- Luu lich su xuat kho

**Xem ton kho:**
- Hien thi so luong ton cua tat ca sach
- Vi tri luu kho
- Canh bao sach sap het

**Lich su giao dich:**
- Xem lich su nhap/xuat
- Loc theo ngay, loai giao dich
- Nguoi thuc hien

### 4. QUAN LY DON HANG

**Tao don hang:**
- Nhap thong tin khach hang
- Chon sach va so luong
- Kiem tra ton kho
- Tinh tong tien tu dong
- Luu nguoi tao don

**Cap nhat trang thai:**
- Dang xu ly
- Hoan thanh
- Da huy

**Huy don:**
- Doi trang thai thanh "Da huy"
- Khong xoa khoi database

**Xem chi tiet:**
- Thong tin khach hang
- Danh sach sach da mua
- Tong tien
- Trang thai
- Nguoi tao

**Tim kiem don:**
- Tim theo ma don
- Tim theo ten khach hang
- Tim theo so dien thoai

**Loc don hang:**
- Loc theo trang thai
- Loc theo khoang ngay

### 5. THONG KE

**Thong ke don hang:**
- Tong so don hang
- Don hoan thanh
- Don dang xu ly
- Don da huy

**Thong ke doanh thu:**
- Doanh thu chi tinh don hoan thanh
- Doanh thu trung binh
- Loc theo thoi gian

**Sach ban chay:**
- Top sach ban nhieu nhat
- So luong da ban

---

## CAI DAT

### Yeu cau he thong:

**Phan mem:**
- Windows 10/11
- Python 3.8 tro len
- SQL Server 2019 tro len
- SQL Server Management Studio (tuy chon)

**Thu vien Python:**
```
pyodbc>=4.0.0
```

### Cac buoc cai dat:

**Buoc 1: Cai dat Python**
```
1. Tai Python tu python.org
2. Cai dat va tick chon "Add Python to PATH"
3. Kiem tra: python --version
```

**Buoc 2: Cai dat SQL Server**
```
1. Tai SQL Server Developer tu Microsoft
2. Cai dat voi Windows Authentication hoac Mixed Mode
3. Ghi nho Server Name (vi du: DESKTOP-ABC\SQLEXPRESS)
```

**Buoc 3: Cai dat thu vien**
```bash
pip install pyodbc
```

**Buoc 4: Tao database**
```
1. Mo SQL Server Management Studio
2. Ket noi voi Server
3. Chay file sql/01_create_database.sql
4. Chay file sql/02_add_users_table.sql
```

**Buoc 5: Cau hinh ket noi**
```
1. Mo file config/config.py
2. Sua thong tin ket noi:
   - SERVER_NAME
   - DATABASE_NAME
   - USERNAME (neu dung SQL Authentication)
   - PASSWORD (neu dung SQL Authentication)
```

**Buoc 6: Chay ung dung**
```bash
python main.py
```

---

## HUONG DAN SU DUNG

### Dang nhap lan dau:

**Tai khoan mac dinh:**
- Username: admin
- Password: admin
- Role: admin

**Sau khi dang nhap, nen:**
1. Doi mat khau admin
2. Tao tai khoan user moi

### Su dung chuc nang:

**1. Quan ly sach:**
```
Menu chinh > Quan ly sach
- Them sach: Click "Them", nhap thong tin, click "Luu"
- Sua sach: Chon sach, click "Sua", sua thong tin, click "Cap nhat"
- Xoa sach: Chon sach, click "Xoa", xac nhan
- Tim sach: Click "Tim kiem", nhap tu khoa
```

**2. Quan ly kho:**
```
Menu chinh > Quan ly kho
- Nhap kho: Chon sach, nhap so luong, click "Nhap kho"
- Xuat kho: Chon sach, nhap so luong, click "Xuat kho"
- Xem ton: Hien thi tu dong trong danh sach
```

**3. Quan ly don hang:**
```
Menu chinh > Quan ly kinh doanh
- Tao don: Click "Tao don moi"
  + Nhap thong tin khach hang
  + Click "Chon sach", chon sach va so luong
  + Click "Tao don"
- Cap nhat trang thai: Chon don, click "Sua don", chon trang thai
- Xem chi tiet: Chon don, click "Chi tiet"
- Huy don: Chon don, click "Huy don"
```

**4. Xem thong ke:**
```
Menu chinh > Quan ly kinh doanh
- Xem o thong ke tren cung:
  + Tong don hang
  + Doanh thu
  + Don hoan thanh
  + Don dang xu ly
```

### Luu y khi su dung:

**Quan ly sach:**
- Ma sach phai unique (khong trung)
- Gia mua va gia bia phai la so
- Nen luu tat ca thong tin day du

**Quan ly kho:**
- Khong the xuat vuot qua ton kho
- Nen kiem tra ton truoc khi xuat
- Luu lich su de theo doi

**Quan ly don hang:**
- Kiem tra ton kho truoc khi tao don
- Cap nhat trang thai dung thoi gian
- Chi tinh doanh thu khi don "Hoan thanh"

---

## CAU TRUC THU MUC

```
QuanLyNhaSach/
|
+-- main.py                     # File khoi dong ung dung
|
+-- database/                   # Thu muc database layer
|   +-- __init__.py
|   +-- book_database.py        # Quan ly sach, kho, don hang
|   +-- user_manager.py         # Quan ly user, xac thuc
|   +-- connection_manager.py   # Quan ly ket noi SQL Server
|
+-- gui/                        # Thu muc giao dien
|   +-- __init__.py
|   +-- login_window.py         # Man hinh dang nhap
|   +-- main_menu.py            # Menu chinh
|   +-- book_manager.py         # Quan ly sach
|   +-- inventory_manager.py    # Quan ly kho
|   +-- business_manager.py     # Quan ly kinh doanh
|
+-- sql/                        # Thu muc SQL scripts
|   +-- 01_create_database.sql  # Tao database va tables
|   +-- 02_add_users_table.sql  # Tao bang Users
|   +-- 03_insert_sample_data.sql
|
+-- config/                     # Thu muc cau hinh
|   +-- config.py               # Cau hinh ket noi database
|
+-- requirements.txt            # Danh sach thu vien
+-- README.md                   # File nay
```

---

## LUONG HOAT DONG

### 1. Khoi dong ung dung:

```
[main.py]
    |
    +-> Ket noi SQL Server
    |
    +-> Hien thi LoginWindow
    |
    +-> Xac thuc user
    |
    +-> Hien thi MainMenu (neu thanh cong)
```

### 2. Them sach moi:

```
[User click "Them sach"]
    |
    +-> Nhap thong tin sach
    |
    +-> Validate du lieu
    |
    +-> Kiem tra ma sach trung
    |
    +-> INSERT INTO Sach
    |
    +-> Tu dong INSERT INTO TonKho (so luong = 0)
    |
    +-> Hien thi thong bao thanh cong
    |
    +-> Refresh danh sach
```

### 3. Nhap kho:

```
[User click "Nhap kho"]
    |
    +-> Chon sach can nhap
    |
    +-> Nhap so luong
    |
    +-> UPDATE TonKho SET SoLuongTon = SoLuongTon + SoLuong
    |
    +-> INSERT INTO NhapXuatKho (loai='Nhap')
    |
    +-> COMMIT
    |
    +-> Hien thi thong bao thanh cong
```

### 4. Tao don hang:

```
[User click "Tao don moi"]
    |
    +-> Nhap thong tin khach hang
    |
    +-> Chon sach va so luong
    |
    +-> Kiem tra ton kho
    |
    +-> Tinh tong tien
    |
    +-> BEGIN TRANSACTION
    |   |
    |   +-> INSERT INTO DonHang (NguoiTao = username)
    |   |
    |   +-> Lay ID don vua tao
    |   |
    |   +-> INSERT INTO ChiTietDonHang (tung sach)
    |   |
    |   +-> COMMIT
    |
    +-> Hien thi thong bao thanh cong
    |
    +-> Refresh danh sach don hang
```

### 5. Cap nhat trang thai don:

```
[User chon don va click "Sua don"]
    |
    +-> Hien thi popup voi trang thai hien tai
    |
    +-> User chon trang thai moi
    |
    +-> UPDATE DonHang SET TrangThai = ?, NgayCapNhat = NOW()
    |
    +-> COMMIT
    |
    +-> Refresh danh sach
    |
    +-> Cap nhat thong ke (neu can)
```

### 6. Tinh doanh thu:

```
[He thong tinh doanh thu]
    |
    +-> SELECT COUNT(*) FROM DonHang
    |       (Tong don hang)
    |
    +-> SELECT COUNT(*), SUM(TongTien) FROM DonHang
    |       WHERE TrangThai = 'Hoan thanh'
    |       (Don hoan thanh va doanh thu)
    |
    +-> SELECT COUNT(*) FROM DonHang
    |       WHERE TrangThai = 'Dang xu ly'
    |       (Don dang xu ly)
    |
    +-> Hien thi len giao dien
```

---

## BAO MAT

### Ma hoa password:

**Khi dang ky:**
```python
# 1. Tao salt ngau nhien (64 ky tu)
salt = secrets.token_hex(32)

# 2. Noi password voi salt
password_with_salt = password + salt

# 3. Hash bang SHA256
password_hash = hashlib.sha256(password_with_salt.encode()).hexdigest()

# 4. Luu ca password_hash va salt vao database
INSERT INTO Users (Username, PasswordHash, Salt, ...)
VALUES (?, ?, ?, ...)
```

**Khi dang nhap:**
```python
# 1. Lay PasswordHash va Salt tu database
SELECT PasswordHash, Salt FROM Users WHERE Username = ?

# 2. Hash password nhap vao voi salt tu database
input_hash = hashlib.sha256((input_password + salt).encode()).hexdigest()

# 3. So sanh
if input_hash == stored_hash:
    # Dang nhap thanh cong
```

### Phan quyen:

**Admin:**
- Quan ly sach
- Quan ly kho
- Quan ly don hang
- Xem thong ke
- Quan ly user (neu co chuc nang)

**User:**
- Xem thong tin sach
- Tao don hang
- Xem don hang cua minh

### Bao ve du lieu:

- Transaction: Dam bao du lieu nhat quan
- Foreign Key: Dam bao toan ven tham chieu
- Rollback: Hoan tac khi co loi
- Validation: Kiem tra du lieu truoc khi luu

---

## XU LY LOI

### Loi ket noi database:

**Trieu chung:**
- "Khong the ket noi SQL Server"
- "Login failed"

**Giai phap:**
1. Kiem tra SQL Server dang chay
2. Kiem tra ten server dung
3. Kiem tra username/password (neu dung SQL Auth)
4. Kiem tra firewall
5. Kiem tra ODBC Driver 17 da cai dat

### Loi du lieu:

**Trieu chung:**
- "Ma sach da ton tai"
- "Khong du ton kho"
- "Invalid input"

**Giai phap:**
1. Kiem tra ma sach khong trung
2. Kiem tra so luong ton truoc khi xuat
3. Kiem tra dinh dang du lieu (so, chu, ngay thang)

### Loi giao dien:

**Trieu chung:**
- Giao dien khong hien thi
- Button khong hoat dong
- Loi font chu

**Giai phap:**
1. Kiem tra Python version (>=3.8)
2. Kiem tra tkinter da cai dat
3. Restart ung dung

---

## LIEN HE

**Tac gia:** Duong Gia Phu  
**Email:** duongphu010620@gmail.com  
**Phone:** 0325120429  
**Dia chi:** Long Xuyen, An Giang

---

## LICENSE

Du an nay duoc phat trien phuc vu muc dich hoc tap va nghien cuu.

---

**PHIEN BAN:** 1.0.0 - Hoan thanh ngay 18/11/2025