# ==========================================
# Người phát triển: Vũ Đức Tú – K58 – Thái Nguyên
# ==========================================
import os, io, hashlib, datetime
from datetime import timezone, timedelta
from pyhanko.sign import validation
from pyhanko.sign.diff_analysis import ModificationLevel
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.keys import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext

# === 🔧 Cấu hình tệp tin (đồng bộ với file sign_pdf.py) ===
DUONG_DAN_PDF = r"D:\BAITAP2\pdf\signed.pdf"
DUONG_DAN_CHUNG_THU = r"D:\BAITAP2\keys\signer_cert.pem"
DUONG_DAN_LOG = r"D:\BAITAP2\KIEMTRA.txt"

# === ✍️ Hàm ghi log ra tệp văn bản (hiển thị đồng thời trên console) ===
def ghi_log(noi_dung):
    print(noi_dung)
    with open(DUONG_DAN_LOG, "a", encoding="utf-8") as file_log:
        file_log.write(noi_dung + "\n")

# === 🕐 Bắt đầu quá trình xác thực ===
if os.path.exists(DUONG_DAN_LOG):
    os.remove(DUONG_DAN_LOG)

ghi_log("=== HỆ THỐNG XÁC THỰC CHỮ KÝ PDF – PHIÊN BẢN VŨ ĐỨC TÚ ===")
ghi_log(f"📅 Thời điểm kiểm tra: {datetime.datetime.now()}")
ghi_log(f"📄 Tệp PDF cần xác thực: {DUONG_DAN_PDF}")
ghi_log("===============================================")

# === 🧩 Nạp chứng thư tin cậy để xác thực ===
try:
    chung_thu_tin_cay = load_cert_from_pemder(DUONG_DAN_CHUNG_THU)
    ngu_canh = ValidationContext(trust_roots=[chung_thu_tin_cay])
except Exception as loi:
    ghi_log(f"❌ Lỗi khi tải chứng thư tin cậy: {loi}")
    exit()

# === 📄 Mở file PDF và phát hiện chữ ký ===
try:
    with open(DUONG_DAN_PDF, "rb") as tep_pdf:
        pdf_doc = PdfFileReader(tep_pdf, strict=False)

        danh_sach_chu_ky = pdf_doc.embedded_signatures

        if not danh_sach_chu_ky:
            ghi_log("❌ Không tìm thấy chữ ký nào trong tài liệu PDF.")
            exit()

        chu_ky = danh_sach_chu_ky[0]
        ten_truong = chu_ky.field_name or "Signature1"
        ghi_log(f"🔍 Phát hiện trường chữ ký: {ten_truong}")

        # === Lấy thông tin cơ bản ===
        doi_tuong_chu_ky = chu_ky.sig_object
        do_dai_noi_dung = len(doi_tuong_chu_ky.get('/Contents'))
        byte_range = doi_tuong_chu_ky.get('/ByteRange')
        ghi_log(f"Kích thước chữ ký (/Contents): {do_dai_noi_dung} byte")
        ghi_log(f"Vùng ByteRange: {byte_range}")

        # === 🧮 Tính lại giá trị băm SHA256 của vùng ký ===
        tep_pdf.seek(0)
        du_lieu = tep_pdf.read()
        br = list(byte_range)
        du_lieu_ky = du_lieu[br[0]:br[0]+br[1]] + du_lieu[br[2]:br[2]+br[3]]
        gia_tri_bam = hashlib.sha256(du_lieu_ky).hexdigest()
        ghi_log(f"Giá trị SHA256 tính được: {gia_tri_bam[:64]} ✅")

        # === 🔍 Tiến hành xác thực chữ ký ===
        try:
            ket_qua = validation.validate_pdf_signature(chu_ky, ngu_canh)
        except Exception as e:
            ghi_log(f"⚠️ Không thể xác thực bằng pyhanko: {e}")
            ghi_log("👉 Gợi ý: Hãy lưu lại file PDF bằng Adobe hoặc Foxit rồi chạy lại.")
            exit()

        ghi_log("===============================================")
        ghi_log("🔒 KẾT QUẢ XÁC THỰC CHỮ KÝ:")
        ghi_log(ket_qua.pretty_print_details())

        # === 👤 Thông tin chứng thư người ký ===
        chung_thu_nguoi_ky = getattr(ket_qua, "signing_cert", None)
        if chung_thu_nguoi_ky:
            ghi_log("\n📜 THÔNG TIN CHỨNG THƯ NGƯỜI KÝ:")
            ghi_log(f"  Chủ thể: {chung_thu_nguoi_ky.subject.human_friendly}")
            sha1 = chung_thu_nguoi_ky.sha1_fingerprint
            sha256 = chung_thu_nguoi_ky.sha256_fingerprint
            sha1 = sha1.hex() if hasattr(sha1, 'hex') else sha1
            sha256 = sha256.hex() if hasattr(sha256, 'hex') else sha256
            ghi_log(f"  Dấu vân tay SHA1: {sha1}")
            ghi_log(f"  Dấu vân tay SHA256: {sha256}")
        else:
            ghi_log("⚠️ Không thể đọc chứng thư của người ký.")

        # === 🕓 Thời gian ký ===
        thoi_gian_ky = getattr(ket_qua, "signer_reported_dt", None)
        if thoi_gian_ky:
            gio_vn = thoi_gian_ky.astimezone(timezone(timedelta(hours=7)))
            ghi_log(f"\n🕒 Thời gian ký (giờ Việt Nam): {gio_vn}")
        else:
            ghi_log("⚠️ Không tìm thấy tem thời gian (timestamp).")

        # === 🔍 Kiểm tra tình trạng chỉnh sửa tài liệu ===
        muc_do = getattr(ket_qua, "modification_level", None)
        if muc_do == ModificationLevel.NONE:
            ghi_log("✅ Tài liệu KHÔNG bị chỉnh sửa sau khi ký.")
        elif muc_do == ModificationLevel.FORM_FILLING:
            ghi_log("⚠️ Có chỉnh sửa nhẹ (điền biểu mẫu) sau khi ký.")
        else:
            ghi_log("❌ Phát hiện thay đổi nội dung sau khi ký!")

        ghi_log("===============================================")

        # === 📋 Tổng kết ===
        if getattr(ket_qua, "bottom_line", False):
            ghi_log("✅ CHỮ KÝ HỢP LỆ – TÀI LIỆU NGUYÊN VẸN.")
        else:
            ghi_log("❌ CHỮ KÝ KHÔNG HỢP LỆ HOẶC FILE ĐÃ BỊ SỬA ĐỔI.")

except Exception as loi:
    ghi_log(f"❌ Lỗi khi xác thực tệp PDF: {loi}")

ghi_log("\n📘 Quá trình kiểm tra hoàn tất – kết quả được lưu trong kqkt.txt.")
ghi_log("👨‍💻 Người thực hiện: Vũ Đức Tú – K58 – Đại học Thái Nguyên")
ghi_log("===============================================")
