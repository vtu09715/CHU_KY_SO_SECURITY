# tamper_preserve_signature.py
# Phiên bản không tạo file tạm overlay_temp.pdf – overlay thực hiện trong bộ nhớ

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
from pikepdf import Pdf
from pathlib import Path
from datetime import datetime
from io import BytesIO
import sys

# === Cấu hình ===
SIGNED_PDF = Path(r"D:\BAITAP2\pdf\signed.pdf")         # File PDF đã ký
TAMPERED_PDF = Path(r"D:\BAITAP2\pdf\tampered.pdf")     # File PDF đầu ra
SIGN_IMAGE = Path("chuky.jpg")                          # Ảnh chữ ký cá nhân (tùy chọn)

# === Kiểm tra file nguồn ===
if not SIGNED_PDF.exists():
    print(f"❌ Không tìm thấy file nguồn: {SIGNED_PDF}")
    sys.exit(1)

# === Đăng ký font ===
FONT_PATH = Path("C:/Windows/Fonts/arial.ttf")
FONT_NAME = "ArialUnicode"
if FONT_PATH.exists():
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))
    except Exception:
        FONT_NAME = "Helvetica"
else:
    FONT_NAME = "Helvetica"

# === Lấy kích thước trang ===
with Pdf.open(str(SIGNED_PDF)) as base_check:
    mb = base_check.pages[0].MediaBox
    llx, lly, urx, ury = [float(x) for x in mb]
    page_w = urx - llx
    page_h = ury - lly

# === Tạo overlay trực tiếp trong bộ nhớ ===
overlay_buffer = BytesIO()
c = canvas.Canvas(overlay_buffer, pagesize=(page_w, page_h))
c.setFont(FONT_NAME, 14)
try:
    c.setFillAlpha(0.3)  # chữ mờ, không che nội dung
except Exception:
    pass

# Màu đỏ nhạt cảnh báo
c.setFillColor(Color(1, 0, 0, alpha=0.3))

# Thêm chữ cảnh báo mờ
x = 100
y = page_h - 100
c.drawString(x, y, "⚠ Đây là bản sao có chỉnh sửa (Demo) ⚠")

# Thêm timestamp nhỏ
c.setFont(FONT_NAME, 9)
ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
c.drawRightString(page_w - 15*mm, 8*mm, f"Modified on: {ts}")

# (Tùy chọn) thêm ảnh chữ ký nếu có
if SIGN_IMAGE.exists():
    c.drawImage(str(SIGN_IMAGE), x=page_w - 60*mm, y=15*mm, width=40*mm, height=20*mm, mask='auto')

c.save()
overlay_buffer.seek(0)

print("✅ Overlay tạm được tạo trong bộ nhớ, không ghi ra đĩa.")

# === Ghép overlay với PDF gốc ===
with Pdf.open(str(SIGNED_PDF)) as base:
    with Pdf.open(overlay_buffer) as overlay:
        for i, page in enumerate(base.pages):
            page.add_overlay(overlay.pages[0])
            print(f"  → Đã áp dụng overlay lên trang {i+1}")

        base.save(str(TAMPERED_PDF))
        print(f"💾 Đã lưu file chỉnh sửa tại: {TAMPERED_PDF}")

print("✅ Hoàn tất, không tạo file tạm overlay_temp.pdf nào.")
