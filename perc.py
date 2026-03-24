import tkinter as tk
from tkinter import filedialog, messagebox
import os
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
from openpyxl import Workbook, load_workbook
import io

EXCEL_FILE = "PDF_Analysis.xlsx"

def extract_images_from_pdf(pdf_path):
    """Извлечение изображений из PDF с использованием PyMuPDF."""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img = Image.open(io.BytesIO(image_bytes))
            images.append(img)
    return images

def calculate_fill_percentage(image):
    """
    Рассчитать процент заполненности с учетом прозрачности.
    Полностью прозрачные пиксели (альфа = 0) исключаются из расчета.
    """
    if image.mode == "RGBA":
        alpha_channel = np.array(image.split()[-1])  # Извлекаем альфа-канал
        total_pixels = alpha_channel.size  # Общее количество пикселей
        opaque_pixels = np.sum(alpha_channel == 255)  # Количество полностью непрозрачных пикселей
        fill_percentage = (opaque_pixels / total_pixels) * 100
    else:
        # Если альфа-канал отсутствует, предполагаем, что изображение полностью непрозрачно
        fill_percentage = 100
    return fill_percentage

def process_pdf(file_path):
    """Обработка PDF-файла."""
    pdf_name = os.path.basename(file_path)

    # Проверка существования Excel файла
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(["File Name", "Total Pages", "Total Images", "Fill Percentage"])
        wb.save(EXCEL_FILE)

    # Открыть Excel и проверить на дубликаты
    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    existing_files = [row[0].value for row in ws.iter_rows(min_row=2, max_col=1)]

    if pdf_name in existing_files:
        messagebox.showinfo("Info", f"Файл {pdf_name} уже существует в базе данных.")
        return

    # Извлечение изображений и расчет заполненности
    images = extract_images_from_pdf(file_path)
    if not images:
        messagebox.showerror("Error", "В PDF не найдено изображений!")
        return

    fill_percentages = [calculate_fill_percentage(img) for img in images]
    avg_fill_percentage = sum(fill_percentages) / len(fill_percentages)

    # Запись в Excel
    ws.append([pdf_name, len(fitz.open(file_path)), len(images), round(avg_fill_percentage, 2)])
    wb.save(EXCEL_FILE)

    messagebox.showinfo("Success", f"Файл {pdf_name} успешно обработан!")

def select_pdf():
    """Открыть диалоговое окно для выбора PDF."""
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Выберите PDF-файл"
    )
    if file_path:
        process_pdf(file_path)

# Создание графического интерфейса
root = tk.Tk()
root.title("PDF Analyzer")

btn_select_pdf = tk.Button(root, text="Выбрать PDF", command=select_pdf, width=20, height=2)
btn_select_pdf.pack(pady=20)

root.mainloop()
