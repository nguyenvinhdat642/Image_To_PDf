from PIL import Image
import os

# Đường dẫn đến thư mục cha chứa các thư mục con
parent_folder = r'D:\GAME\manga'

# Lặp qua các thư mục con trong thư mục cha
for subfolder in os.listdir(parent_folder):
    subfolder_path = os.path.join(parent_folder, subfolder)

    # Chắc chắn rằng đây là thư mục và không phải tệp
    if os.path.isdir(subfolder_path):
        # Tạo danh sách các tệp hình ảnh trong thư mục con
        image_files = [f for f in os.listdir(subfolder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

        # Sắp xếp tệp hình ảnh theo thứ tự
        image_files.sort()

        # Tạo tên tệp PDF đầu ra dựa trên tên thư mục con
        output_pdf = os.path.join(parent_folder, f'{subfolder}.pdf')

        # Mở hình ảnh đầu tiên để có kích thước mẫu
        with Image.open(os.path.join(subfolder_path, image_files[0])) as img:
            try:
                images_to_append = [Image.open(os.path.join(subfolder_path, image)) for image in image_files[1:]]
                img.save(output_pdf, save_all=True, append_images=images_to_append)
                print(f"Chuyển đổi thành công thư mục {subfolder} thành tệp PDF: {output_pdf}")
            except Exception as e:
                print(f"Lỗi khi xử lý thư mục {subfolder}: {e}")
