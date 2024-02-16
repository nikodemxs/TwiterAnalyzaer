import csv
import os
import json
import pandas as pd
from src.utils.logger import Logger

def export_to_xlsx(data, filename="output"):
    logger = Logger("File Export service")
    os.makedirs("outputs", exist_ok=True)
    file_path = f"outputs/{filename}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    logger.info(f"Data exported to {file_path} successfully.")

def export_to_csv(data, filename="output"):
    logger = Logger("File Export service")
    os.makedirs("outputs", exist_ok=True)
    file_path = f"outputs/{filename}.csv"
    keys = data[0].keys() 
    with open(file_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    logger.info(f"Data exported to {file_path} successfully.")

def export_to_json(data, filename="output"):
    logger = Logger("File Export service")
    os.makedirs("outputs", exist_ok=True)
    file_path = f"outputs/{filename}.json"
    with open(file_path, 'w') as output_file:
        json.dump(data, output_file)
    logger.info(f"Data exported to {file_path} successfully.")

def print_in_console(data, filename="output"):
    for item in data:
        print(item)