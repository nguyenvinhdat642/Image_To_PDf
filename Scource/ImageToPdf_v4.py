import os
import subprocess
from tkinter import Tk, Button, Label, Listbox, filedialog, StringVar, Entry, messagebox, scrolledtext
from PIL import Image
from PyPDF2 import PdfMerger

selected_folder = ""

def convert_images_to_pdf(subfolder_path, output_pdf, progress_list):
    # Tạo danh sách các tệp hình ảnh trong thư mục con
    image_files = [f for f in os.listdir(subfolder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Kiểm tra xem có ít nhất một tệp hình ảnh để chuyển đổi
    if not image_files:
        progress_list.insert('end', f"Không tìm thấy tệp hình ảnh trong thư mục {subfolder_path}.")
        return

    # Sắp xếp tệp hình ảnh theo thứ tự
    image_files.sort()

    # Mở hình ảnh đầu tiên để có kích thước mẫu
    with Image.open(os.path.join(subfolder_path, image_files[0])) as img:
        try:
            images_to_append = [Image.open(os.path.join(subfolder_path, image)) for image in image_files[1:]]
            img.save(output_pdf, save_all=True, append_images=images_to_append)
            progress_list.insert('end', f"Chuyển đổi thành công thư mục {subfolder_path} thành tệp PDF: {output_pdf}")
        except Exception as e:
            progress_list.insert('end', f"Lỗi khi xử lý thư mục {subfolder_path}: {e}")

def merge_pdfs(parent_folder, output_merged_pdf, progress_list):
    # Lấy danh sách tất cả các thư mục con trong thư mục đầu vào
    subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

    # Kiểm tra xem có ít nhất hai thư mục con để gộp không
    if len(subfolders) < 2:
        progress_list.insert('end', f"Cần ít nhất hai thư mục con để gộp trong thư mục {parent_folder}.")
        return

    # Tạo đối tượng PdfMerger
    pdf_merger = PdfMerger()

    # Chuyển đổi và gộp tất cả các thư mục con
    for subfolder in subfolders:
        subfolder_path = os.path.join(parent_folder, subfolder)
        output_pdf = os.path.join(parent_folder, f'{subfolder}.pdf')
        
        # Chuyển đổi ảnh thành tệp PDF cho mỗi thư mục con
        convert_images_to_pdf(subfolder_path, output_pdf, progress_list)

        # Thêm tệp PDF đã chuyển đổi vào đối tượng PdfMerger
        pdf_merger.append(output_pdf)

    # Lưu tất cả vào một tệp PDF đầu ra
    pdf_merger.write(output_merged_pdf)
    pdf_merger.close()

    progress_list.insert('end', f"Tất cả các tệp PDF trong thư mục {parent_folder} đã được gộp thành '{output_merged_pdf}'.")
    open_folder_button.config(state='normal')

# Hàm mở thư mục đã được thực thi
def open_folder():
    global selected_folder
    if selected_folder:
        os.startfile(selected_folder)
    else:
        messagebox.showinfo("Thông báo", "Vui lòng chọn một thư mục trước khi mở.")





# Hàm chọn thư mục
def select_folder(entry_var, progress_list):
    global selected_folder
    folder_selected = filedialog.askdirectory(title="Select Folder")
    selected_folder = folder_selected
    entry_var.set(selected_folder)
    progress_list.insert('end', f"\nĐã chọn thư mục: {selected_folder}\n")


# Hàm chạy quá trình chuyển đổi và gộp PDF
def run_conversion(path_var, progress_list):
    folder_path = path_var.get()

    if not os.path.isdir(folder_path):
        messagebox.showerror("Lỗi", "Vui lòng chọn một thư mục hợp lệ.")
        return

    # Tên tệp PDF đầu ra sau khi gộp là tên của thư mục cha
    output_merged_pdf = os.path.join(folder_path, f'{os.path.basename(folder_path)}.pdf')

    # Gọi hàm để chuyển đổi và gộp các tệp PDF
    merge_pdfs(folder_path, output_merged_pdf, progress_list)

# Tạo cửa sổ Tkinter
root = Tk()
root.title("Ứng dụng chuyển đổi ảnh thành PDF")

# Biến lưu trữ đường dẫn thư mục được chọn
path_var = StringVar()

# Label hiển thị tiêu đề
title_label = Label(root, text="Chuyển đổi ảnh thành PDF", font=("Helvetica", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

# Button để chọn thư mục
select_button = Button(root, text="Chọn Thư Mục", command=lambda: select_folder(path_var, progress_list), font=("Helvetica", 12))
select_button.grid(row=1, column=0, pady=(0, 10))

# Entry để hiển thị đường dẫn thư mục đã chọn
path_entry = Entry(root, textvariable=path_var, state='readonly', width=50, font=("Helvetica", 12))
path_entry.grid(row=1, column=1, pady=(0, 10))

# Button để thực thi chuyển đổi và gộp PDF
run_button = Button(root, text="Chạy", command=lambda: run_conversion(path_var, progress_list), font=("Helvetica", 14), bg="#4CAF50", fg="white")
run_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))

# Button để mở thư mục đã được thực thi
open_folder_button = Button(root, text="Mở Thư Mục", command=open_folder, font=("Helvetica", 14), state='disabled')
open_folder_button.grid(row=2, column=2, pady=(10, 20))

# Listbox để hiển thị tiến trình
progress_list = Listbox(root, width=80, height=10, font=("Helvetica", 12))
progress_list.grid(row=3, column=0, columnspan=3, pady=(0, 10))

# Chạy vòng lặp sự kiện của cửa sổ
root.mainloop()
