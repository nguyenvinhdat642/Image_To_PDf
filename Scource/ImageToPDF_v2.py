import os
from PyPDF2 import PdfMerger

def merge_pdfs(input_folder, output_file):
    # Kiểm tra xem thư mục đầu vào có tồn tại không
    if not os.path.exists(input_folder):
        print(f"Thư mục đầu vào '{input_folder}' không tồn tại.")
        return

    # Lấy danh sách tất cả các tệp PDF trong thư mục đầu vào
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

    # Kiểm tra xem có ít nhất hai tệp PDF để gộp không
    if len(pdf_files) < 2:
        print("Cần ít nhất hai tệp PDF để gộp.")
        return

    # Tạo đối tượng PdfMerger
    pdf_merger = PdfMerger()

    # Thêm tất cả các tệp PDF vào đối tượng PdfMerger
    for pdf_file in pdf_files:
        pdf_merger.append(os.path.join(input_folder, pdf_file))

    # Lưu tất cả vào một tệp PDF đầu ra
    pdf_merger.write(output_file)

    print(f"Tất cả các tệp PDF đã được gộp thành '{output_file}'.")

# Thực hiện hàm với đường dẫn thư mục đầu vào và tên tệp PDF đầu ra
merge_pdfs(r"D:\GAME\pdf", r"D:\output_merged.pdf")
