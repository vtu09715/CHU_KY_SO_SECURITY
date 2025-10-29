BÀI TẬP VỀ NHÀ – MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN
 Chủ đề: Chữ ký số trong file PDF
 Giảng viên: Đỗ Duy Cốp
 Thời điểm giao: 2025-10-24 11:45
 Đối tượng áp dụng: Toàn bộ sv lớp học phần 58KTPM
 Hạn nộp: Sv upload tất cả lên github trước 2025-10-31 23:59:59--
I. MÔ TẢ CHUNG
 Sinh viên thực hiện báo cáo và thực hành: phân tích và hiện thực việc nhúng, xác 
thực chữ ký số trong file PDF.
 Phải nêu rõ chuẩn tham chiếu (PDF 1.7 / PDF 2.0, PAdES/ETSI) và sử dụng công cụ 
thực thi (ví dụ iText7, OpenSSL, PyPDF, pdf-lib).--
II. CÁC YÊU CẦU CỤ THỂ
 1) Cấu trúc PDF liên quan chữ ký (Nghiên cứu)- Mô tả ngắn gọn: Catalog, Pages tree, Page object, Resources, Content streams, 
XObject, AcroForm, Signature field (widget), Signature dictionary (/Sig), 
/ByteRange, /Contents, incremental updates, và DSS (theo PAdES).- Liệt kê object refs quan trọng và giải thích vai trò của từng object trong 
lưu/truy xuất chữ ký.- Đầu ra: 1 trang tóm tắt + sơ đồ object (ví dụ: Catalog → Pages → Page → /Contents
 ; Catalog → /AcroForm → SigField → SigDict).
 2) Thời gian ký được lưu ở đâu?- Nêu tất cả vị trí có thể lưu thông tin thời gian:
 + /M trong Signature dictionary (dạng text, không có giá trị pháp lý).
 + Timestamp token (RFC 3161) trong PKCS#7 (attribute timeStampToken).
 + Document timestamp object (PAdES).
 + DSS (Document Security Store) nếu có lưu timestamp và dữ liệu xác minh.- Giải thích khác biệt giữa thông tin thời gian /M và timestamp RFC3161.
 3) Các bước tạo và lưu chữ ký trong PDF (đã có private RSA)- Viết script/code thực hiện tuần tự:
 1. Chuẩn bị file PDF gốc.
 2. Tạo Signature field (AcroForm), reserve vùng /Contents (8192 bytes).
 3. Xác định /ByteRange (loại trừ vùng /Contents khỏi hash).
 4. Tính hash (SHA-256/512) trên vùng ByteRange.
 5. Tạo PKCS#7/CMS detached hoặc CAdES:- Include messageDigest, signingTime, contentType.- Include certificate chain.- (Tùy chọn) thêm RFC3161 timestamp token.
 6. Chèn blob DER PKCS#7 vào /Contents (hex/binary) đúng offset.
 7. Ghi incremental update.
 8. (LTV) Cập nhật DSS với Certs, OCSPs, CRLs, VRI.- Phải nêu rõ: hash alg, RSA padding, key size, vị trí lưu trong PKCS#7.- Đầu ra: mã nguồn, file PDF gốc, file PDF đã ký.
4) Các bước xác thực chữ ký trên PDF đã ký- Các bước kiểm tra:
 1. Đọc Signature dictionary: /Contents, /ByteRange.
 2. Tách PKCS#7, kiểm tra định dạng.
 3. Tính hash và so sánh messageDigest.
 4. Verify signature bằng public key trong cert.
 5. Kiểm tra chain → root trusted CA.
 6. Kiểm tra OCSP/CRL.
 7. Kiểm tra timestamp token.
 8. Kiểm tra incremental update (phát hiện sửa đổi).- Nộp kèm script verify + log kiểm thử.--
III. YÊU CẦU NỘP BÀI
 1. Báo cáo PDF ≤ 6 trang: mô tả cấu trúc, thời gian ký, rủi ro bảo mật.
 2. Code + README (Git repo hoặc zip).
 3. Demo files: original.pdf, signed.pdf, tampered.pdf.
 4. (Tuỳ chọn) Video 3–5 phút demo kết quả.--
IV. TIÊU CHÍ CHẤM- Lý thuyết & cấu trúc PDF/chữ ký: 25%- Quy trình tạo chữ ký đúng kỹ thuật: 30%- Xác thực đầy đủ (chain, OCSP, timestamp): 25%- Code & demo rõ ràng: 15%- Sáng tạo mở rộng (LTV, PAdES): 5%--
V. GHI CHÚ AN TOÀN- Vẫn lưu private key (sinh random) trong repo. Tránh dùng private key thương mại.- Dùng RSA ≥ 2048-bit và SHA-256 hoặc mạnh hơn.- Có thể dùng RSA-PSS thay cho PKCS#1 v1.5.- Khuyến khích giải thích rủi ro: padding oracle, replay, key leak.--
VI. GỢI Ý CÔNG CỤ- OpenSSL, iText7/BouncyCastle, pypdf/PyPDF2.- Tham khảo chuẩn PDF: ISO 32000-2 (PDF 2.0) và ETSI EN 319 142 (PAdES)
# BÀI LÀM </P>
+ Tạo folder trong ổ D:</p>
<img width="969" height="339" alt="image" src="https://github.com/user-attachments/assets/fcabb416-f5ca-4e37-9ad8-bb475fc9f9a1" /></p>
+ tạo 1 folder chứa 2 file code python</p>
<img width="930" height="244" alt="image" src="https://github.com/user-attachments/assets/aea7540b-6a90-4054-8ae2-405286701ac4" /> </p>
+ tạo folder chứa 2 file pdf 1 là pdf gốc( original ) 1 là file pdf đã ký
<img width="1480" height="813" alt="image" src="https://github.com/user-attachments/assets/2cfca123-3c32-420b-b907-8665f6be87c8" /> </p>
+ file pdf đã ký
<img width="1543" height="821" alt="image" src="https://github.com/user-attachments/assets/8a6cba4e-ce48-4a12-8517-0cdf92446f74" /> </p>

# mã nguồn </p>
```
      
        # ==========================================
# sign_pdf.py - Ký số tài liệu PDF bằng chứng chỉ tự ký (self-signed)
# Cá nhân hóa bởi: Vu Duc Tu
# ==========================================

from datetime import datetime
from pyhanko.sign import signers, fields
from pyhanko.stamp.text import TextStampStyle
from pyhanko.pdf_utils import images
from pyhanko.pdf_utils.text import TextBoxStyle
from pyhanko.pdf_utils.layout import SimpleBoxLayoutRule, AxisAlignment, Margins
from pyhanko.sign.general import load_cert_from_pemder, SigningError
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign.fields import SigFieldSpec
import os

# === 🗂️ CẤU HÌNH ĐƯỜNG DẪN ===
BASE_DIR = r"D:\BAITAP2"
PDF_IN = os.path.join(BASE_DIR, "pdf", "original.pdf")
PDF_OUT = os.path.join(BASE_DIR, "pdf", "signed.pdf")
KEY_FILE = os.path.join(BASE_DIR, "keys", "signer_key.pem")
CERT_FILE = os.path.join(BASE_DIR, "keys", "signer_cert.pem")
SIG_IMG = os.path.join(BASE_DIR, "anhky", "chuky.jpg")

print("==========================================")
print("🖋️  BẮT ĐẦU QUÁ TRÌNH KÝ SỐ TÀI LIỆU PDF")
print("==========================================")
print("Bước 1️⃣: Chuẩn bị file PDF gốc:", PDF_IN)

# --- 🔑 Tạo signer và ValidationContext ---
signer = signers.SimpleSigner.load(KEY_FILE, CERT_FILE, key_passphrase=None)
vc = ValidationContext(trust_roots=[load_cert_from_pemder(CERT_FILE)])

# --- ✍️ Bắt đầu tiến trình ký ---
try:
    with open(PDF_IN, "rb") as inf:
        # ⚙️ Cho phép hybrid xref bằng cách tắt strict mode
        writer = IncrementalPdfFileWriter(inf, strict=False)

        # 🟢 Xác định số trang trong PDF
        try:
            pages = writer.root["/Pages"]
            num_pages = int(pages.get("/Count", 1))
        except Exception:
            num_pages = 1

        target_page = num_pages - 1
        print(f"Bước 2️⃣: Thêm trường chữ ký ở trang {target_page + 1}...")

        # 🟩 Thêm vùng chữ ký ở góc phải dưới
        fields.append_signature_field(
            writer,
            SigFieldSpec(
                sig_field_name="Signature_VuDucTu",
                box=(240, 50, 550, 150),
                on_page=target_page
            )
        )

        # 🖼️ Hình ảnh chữ ký tay
        background_img = images.PdfImage(SIG_IMG)

        # --- 📐 Bố cục khung chữ ký ---
        bg_layout = SimpleBoxLayoutRule(
            x_align=AxisAlignment.ALIGN_MIN,
            y_align=AxisAlignment.ALIGN_MID,
            margins=Margins(right=20)
        )
        text_layout = SimpleBoxLayoutRule(
            x_align=AxisAlignment.ALIGN_MIN,
            y_align=AxisAlignment.ALIGN_MID,
            margins=Margins(left=150)
        )
        text_style = TextBoxStyle(font_size=13)

        # 🕒 Thông tin chữ ký hiển thị trong tem
        ngay_ky = datetime.now().strftime("%d/%m/%Y")
        stamp_text = (
            "Vu Duc Tu "
            "\nSV: DHKTCN"
            "\nMSSV: K225480106068"
            "\nSDT: 0813424299"
            "\nfrom: THAI NGUYEN"
            f"\nNgày ký: {ngay_ky}"
        )

        # --- 🪶 Cấu trúc khung hiển thị chữ ký ---
        stamp_style = TextStampStyle(
            stamp_text=stamp_text,
            background=background_img,
            background_layout=bg_layout,
            inner_content_layout=text_layout,
            text_box_style=text_style,
            border_width=1,
            background_opacity=1.0,
        )

        # --- 🧾 Thông tin metadata của chữ ký ---
        meta = signers.PdfSignatureMetadata(
            field_name="Signature_VuDucTu",
            reason="Bài tập: Ký số PDF bằng Python - Lớp K58",
            location="Thái Nguyên, Việt Nam",
            md_algorithm="sha256",
        )

        # --- 🧑‍💻 Khởi tạo signer ---
        pdf_signer = signers.PdfSigner(
            signature_meta=meta,
            signer=signer,
            stamp_style=stamp_style,
        )

        print("Bước 3️⃣: Tạo PKCS#7 (messageDigest, signingTime, contentType)...")
        print("Bước 4️⃣: Tiến hành ký...")

        # --- ✨ Tiến hành ký số tài liệu ---
        with open(PDF_OUT, "wb") as outf:
            pdf_signer.sign_pdf(writer, output=outf)

        print("\n✅ HOÀN TẤT KÝ SỐ!")
        print("📄 File đã lưu tại:", PDF_OUT)
        print("🧾 Có thể kiểm tra chữ ký bằng verify_check_vn.py")

except SigningError as e:
    print("\n❌ LỖI KHI KÝ:", e)
    print("👉 Nếu PDF gốc có hybrid xref, hãy normalize lại bằng pikepdf trước khi ký.")
except Exception as e:
    print("\n❌ LỖI KHÔNG XÁC ĐỊNH:", e)
    print("⚠️ Kiểm tra lại đường dẫn file hoặc định dạng PDF.")

print("==========================================")
print("🏁 HOÀN TẤT QUÁ TRÌNH KÝ PDF")
print("==========================================")
```

+ Sau khi ký thực hiện kiểm tra chữ ký như sau
+ tạo fiel verify_pdf.py trong Script, để chỏ tới file pdf có chữ ký và kiểm tra 
  <img width="1222" height="347" alt="image" src="https://github.com/user-attachments/assets/f67bd3bb-8915-48c1-bd24-24c02327bfff" /></p>
```
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

  ``` 
+ sau khi nhấn chạy sẽ tạo ra file txt ghi kết quả kiểm tra thông tin...
<img width="485" height="211" alt="image" src="https://github.com/user-attachments/assets/f2110081-4b07-40ab-8bb6-e1a6c455c76a" /> </p>
+ như vậy là ok
+ <img width="1918" height="1062" alt="image" src="https://github.com/user-attachments/assets/7dc5fa5b-1bc7-4558-bef3-cdcd0c437f44" /> </p>

+ tạo file tempered.pdf chỉnh sửa file pdf đã ký
<img width="1171" height="419" alt="image" src="https://github.com/user-attachments/assets/3a7624f6-3757-49a0-8faf-82a519b432ff" /> </p>
+ tạo file tempered.py để làm việc
+ sau đó chjay để tạo ra file pdf tạm gọi là pdf edit
<img width="1118" height="537" alt="image" src="https://github.com/user-attachments/assets/60ba4384-e6c5-479f-95d4-b86b589992a6" /></p>
+ kết quả khi tạo ra tempered.pdf
<img width="1359" height="776" alt="image" src="https://github.com/user-attachments/assets/6f09f510-6952-4da7-aa2e-c68de0112b04" />
<img width="1383" height="519" alt="image" src="https://github.com/user-attachments/assets/5a3e3f72-be6f-401f-93a7-731ae91ae9e1" />
+ kiểm tra chữ ký xem chuẩn chưa?
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1bb66cf7-998a-4b57-8996-86dd9bef84f7" />
+ KL: mọi thứ đã ok rồi bài này rất hay phù hợp với thời đại để. EM CẢM ƠN THẦY ĐÃ XEM BÀI LÀM CỦA EM 















