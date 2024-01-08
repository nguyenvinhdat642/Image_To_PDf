from PIL import Image
import os
from PyPDF2 import PdfMerger

def convert_images_to_pdf(subfolder_path, output_pdf):
    # Tạo danh sách các tệp hình ảnh trong thư mục con
    image_files = [f for f in os.listdir(subfolder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Kiểm tra xem có ít nhất một tệp hình ảnh để chuyển đổi
    if not image_files:
        print(f"Không tìm thấy tệp hình ảnh trong thư mục {subfolder_path}.")
        return

    # Sắp xếp tệp hình ảnh theo thứ tự
    image_files.sort()

    # Mở hình ảnh đầu tiên để có kích thước mẫu
    with Image.open(os.path.join(subfolder_path, image_files[0])) as img:
        try:
            images_to_append = [Image.open(os.path.join(subfolder_path, image)) for image in image_files[1:]]
            img.save(output_pdf, save_all=True, append_images=images_to_append)
            print(f"Chuyển đổi thành công thư mục {subfolder_path} thành tệp PDF: {output_pdf}")
        except Exception as e:
            print(f"Lỗi khi xử lý thư mục {subfolder_path}: {e}")

def merge_pdfs(parent_folder, output_merged_pdf):
    # Lấy danh sách tất cả các thư mục con trong thư mục đầu vào
    subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

    # Kiểm tra xem có ít nhất hai thư mục con để gộp không
    if len(subfolders) < 2:
        print(f"Cần ít nhất hai thư mục con để gộp trong thư mục {parent_folder}.")
        return

    # Tạo đối tượng PdfMerger
    pdf_merger = PdfMerger()

    # Lấy tên của thư mục cha
    parent_folder_name = os.path.basename(parent_folder)

    # Chuyển đổi và gộp tất cả các thư mục con
    for subfolder in subfolders:
        subfolder_path = os.path.join(parent_folder, subfolder)
        output_pdf = os.path.join(parent_folder, f'{subfolder}.pdf')
        
        # Chuyển đổi ảnh thành tệp PDF cho mỗi thư mục con
        convert_images_to_pdf(subfolder_path, output_pdf)

        # Thêm tệp PDF đã chuyển đổi vào đối tượng PdfMerger
        pdf_merger.append(output_pdf)

    # Lưu tất cả vào một tệp PDF đầu ra
    pdf_merger.write(output_merged_pdf)
    pdf_merger.close()

    print(f"Tất cả các tệp PDF trong thư mục {parent_folder} đã được gộp thành '{output_merged_pdf}'.")

# Đường dẫn đến thư mục chứa các thư mục con chứa ảnh
parent_folder = r'D:\GAME\Bibo Soukan'

# Tên tệp PDF đầu ra sau khi gộp là tên của thư mục cha
output_merged_pdf = os.path.join(parent_folder, f'{os.path.basename(parent_folder)}.pdf')

# Gộp tất cả các tệp PDF trong thư mục cha và thư mục con thành một tệp PDF duy nhất
merge_pdfs(parent_folder, output_merged_pdf)
