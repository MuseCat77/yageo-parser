from utils.pdf_operations import extract_line_after_keyword
import os
import pandas as pd


def join_missing_datasheet(base_dir):
    missing_elements_csv_path = os.path.join(base_dir, "missing_datasheet_elements.csv")
    for root, dirs, files in os.walk(base_dir):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            pdf_paths = [file for file in os.listdir(directory_path) if file.endswith(".pdf")]
            csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]
            for pdf in pdf_paths:
                result_line = extract_line_after_keyword(pdf, "GLOBAL PART NUMBER (PREFERRED)")
                # if result_line:
                #     print(f"The line after '{keyword}' is:\n{result_line}")
                # else:
                #     print(f"'{keyword}' not found in the document.")
            for csv in csv_files:
                # csv_path = os.path.join(directory_path, csv_file)
                # df = pd.read_csv(csv_path, sep=';')
