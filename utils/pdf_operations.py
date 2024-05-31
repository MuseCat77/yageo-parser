import fitz  # PyMuPDF
import os
from PIL import Image
from io import BytesIO
from utils.logger import log_message

def extract_line_after_keyword(pdf_path, keyword):
    document = fitz.open(pdf_path)

    for page_num in range(len(document)):
        page = document[page_num]
        text = page.get_text("text")

        # Разбиение текста по строкам
        lines = text.splitlines()

        for i, line in enumerate(lines):
            if keyword in line:
                # Проверка на следующую строку
                if i + 1 < len(lines):
                    return lines[i + 1]
    return None


def extract_images(pdf_file, output_directory, filename):
    pdf_document = fitz.open(pdf_file)
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)

        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Открываем изображение с помощью Pillow
            image = Image.open(BytesIO(image_bytes))

            # Проверяем наличие альфа-канала и заменяем его на белый фон, если нужно
            if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
                alpha = image.convert("RGBA").getchannel("A")
                background = Image.new("RGBA", image.size, (255, 255, 255))
                background.paste(image, mask=alpha)
                image = background.convert("RGB")

            output_filename = os.path.join(output_directory, f"{filename}_{page_num}_{image_index}.png")
            if not os.path.exists(output_filename):
                log_message(output_filename)
                os.makedirs(output_directory, exist_ok=True)
                image.save(output_filename, "PNG")
    pdf_document.close()
