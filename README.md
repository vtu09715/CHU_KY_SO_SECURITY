# CHU_KY_SO_SECURITY
## 1. Chuẩn bị file PDF gốc. </p>
+ tạo file gốc chưa có chữ ký.
<img width="1074" height="620" alt="image" src="https://github.com/user-attachments/assets/e063bd40-84ff-4268-a488-4c75ad7b9af7" />
+ lệnh chạy tạo file pdf gốc
<img width="947" height="432" alt="image" src="https://github.com/user-attachments/assets/259ddd54-9c3c-43b3-954f-c1117b1a81bb" />
+ kết quả khi tạo file pdf ( hoàn thành )
<img width="912" height="262" alt="image" src="https://github.com/user-attachments/assets/f5d92920-2b96-46be-bca9-04d35aaae99a" />
## 2. Tạo Signature field (AcroForm), reserve vùng /Contents (8192 bytes).</p>
+ cài pypdf
<img width="1210" height="228" alt="image" src="https://github.com/user-attachments/assets/c36c14a6-686a-47c7-b8c8-272e3512bdbf" />
+ tạo file create_signed_blank.py
<img width="1589" height="883" alt="image" src="https://github.com/user-attachments/assets/40fc9f9b-8901-43ea-9d5c-ef991511ae8d" />
+ tạo signed_blank.pdf với trường chữ ký Sig1 và /Contents reserve = 8192 bytes
<img width="886" height="112" alt="image" src="https://github.com/user-attachments/assets/17230774-22f6-465a-95bd-f17d4eca2095" />
+ kiểm tra xác minh /contents có tồn tại hay không
<img width="1376" height="406" alt="image" src="https://github.com/user-attachments/assets/439ac17b-2d0f-4157-ad41-f18c069ad20f" />
+ tạo file và chạy lệnh kiểm tra ( kết quả File signed_blank.pdf đã có vùng /Contents được reserve 8192 bytes.)
<img width="1238" height="188" alt="image" src="https://github.com/user-attachments/assets/0ebb2fae-81cb-4185-85a0-36358b7cbeea" />
## 3. Xác định /ByteRange (loại trừ vùng /Contents khỏi hash).</p>
+ kết quả tìm kiếm và kiểm tra
+ <img width="1008" height="288" alt="image" src="https://github.com/user-attachments/assets/bce606ac-7bc2-4169-999c-2d74913297ed" />
##  4. Tính hash (SHA-256/512) trên vùng ByteRange.</p>
+ tạo file và chạy lệnh
<img width="1135" height="811" alt="image" src="https://github.com/user-attachments/assets/63d2c92e-8688-4dd3-82b9-3893c39d3d54" />
+ chạy lệnh
<img width="1287" height="197" alt="image" src="https://github.com/user-attachments/assets/ac1e0679-8281-4bd4-853b-695af20f3e10" />
##  5. Tạo PKCS#7/CMS detached hoặc CAdES:- Include messageDigest, signingTime, contentType.- Include certificate chain.- (Tùy chọn) thêm RFC3161 timestamp token.</p>












