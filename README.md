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
<img width="1237" height="684" alt="image" src="https://github.com/user-attachments/assets/fa89f220-fa74-4e51-a31c-f1bd6cdeae00" />
# mã nguồn </p>
```
# ==========================================
# sign_pdf.py - Phiên bản ổn định PyHanko 0.31.0 (Windows)
# Tác giả: Vũ Đức Tú - 58KTP
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

# === CẤU HÌNH ĐƯỜNG DẪN ===
BASE_DIR = r"D:\BAITAP2"
PDF_IN = os.path.join(BASE_DIR, "pdf", "original.pdf")
PDF_OUT = os.path.join(BASE_DIR, "pdf", "signed.pdf")
KEY_FILE = os.path.join(BASE_DIR, "keys", "signer_key.pem")
CERT_FILE = os.path.join(BASE_DIR, "keys", "signer_cert.pem")
SIG_IMG = os.path.join(BASE_DIR, "anhky", "chuky.jpg")

print("=== BẮT ĐẦU QUÁ TRÌNH KÝ PDF ===")
print("Bước 1: Chuẩn bị file PDF gốc (original.pdf).")

# --- Tạo signer và ValidationContext ---
signer = signers.SimpleSigner.load(KEY_FILE, CERT_FILE, key_passphrase=None)
vc = ValidationContext(trust_roots=[load_cert_from_pemder(CERT_FILE)])

# --- Bắt đầu ghi incremental PDF ---
try:
    with open(PDF_IN, "rb") as inf:
        # ⚙️ Cho phép hybrid xref bằng cách tắt strict mode
        writer = IncrementalPdfFileWriter(inf, strict=False)

        # 🟢 Lấy số trang để thêm chữ ký
        try:
            pages = writer.root["/Pages"]
            num_pages = int(pages.get("/Count", 1))
        except Exception:
            num_pages = 1

        target_page = num_pages - 1
        print(f"Bước 2: Thêm trường chữ ký ở trang {target_page + 1}.")

        # 🟩 Tạo field chữ ký ở góc dưới phải trang cuối
        fields.append_signature_field(
            writer,
            SigFieldSpec(
                sig_field_name="SigField1",
                box=(240, 50, 550, 150),
                on_page=target_page
            )
        )

        # 🖼️ Hình ảnh chữ ký tay (jpg/png)
        background_img = images.PdfImage(SIG_IMG)

        # --- Bố cục ảnh và chữ ---
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

        # 🕒 Thông tin chữ ký
        ngay_ky = datetime.now().strftime("%d/%m/%Y")
        stamp_text = (
            "Vũ Đức Tú"
            "\nSĐT: 0813424299"
            "\nMSV: K225480106068"
            "\nĐịa chỉ: Thái Nguyên"
            f"\nNgày ký: {ngay_ky}"
        )

        # --- Khung chữ ký ---
        stamp_style = TextStampStyle(
            stamp_text=stamp_text,
            background=background_img,
            background_layout=bg_layout,
            inner_content_layout=text_layout,
            text_box_style=text_style,
            border_width=1,
            background_opacity=1.0,
        )

        # --- Metadata chữ ký ---
        meta = signers.PdfSignatureMetadata(
            field_name="SigField1",
            reason="Nộp bài: Chữ ký số PDF - 58KTP",
            location="Thái Nguyên, Việt Nam",
            md_algorithm="sha256",
        )

        # --- Khởi tạo signer ---
        pdf_signer = signers.PdfSigner(
            signature_meta=meta,
            signer=signer,
            stamp_style=stamp_style,
        )

        print("Bước 3: Tạo PKCS#7 detached (messageDigest, signingTime, contentType).")
        print("Bước 4: Ký tài liệu...")

        # --- Tiến hành ký PDF ---
        with open(PDF_OUT, "wb") as outf:
            pdf_signer.sign_pdf(writer, output=outf)

        print("\n✅ KÝ THÀNH CÔNG!")
        print("📄 File đã lưu tại:", PDF_OUT)

except SigningError as e:
    print("\n❌ LỖI KHI KÝ:", e)
    print("👉 Nếu PDF gốc có hybrid xref, hãy normalize lại bằng pikepdf trước khi ký.")
except Exception as e:
    print("\n❌ LỖI KHÔNG XÁC ĐỊNH:", e)
    print("⚠️ Kiểm tra lại đường dẫn file hoặc định dạng PDF.")

print("=== HOÀN TẤT QUÁ TRÌNH KÝ ===")
```














