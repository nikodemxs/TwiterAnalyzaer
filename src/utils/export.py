import csv
import json
import pandas as pd

def export_to_xlsx(data, filename="output.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename} successfully.")

def export_to_csv(data, filename="output.csv"):
    keys = data[0].keys() 
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data exported to {filename} successfully.")

def export_to_json(data, filename="output.json"):
    with open(filename, 'w') as output_file:
        json.dump(data, output_file)
    print(f"Data exported to {filename} successfully.")

def print_in_console(data, filename="output"):
    for item in data:
        print(item)