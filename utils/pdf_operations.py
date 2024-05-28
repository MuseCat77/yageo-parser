import fitz  # PyMuPDF


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
