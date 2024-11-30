
from extract import extract
import json

file_path = 'data.pdf'

def save_to_json(data, json_path='output.json'): 
    with open(json_path, 'w') as json_file: 
        json.dump(data, json_file, indent=4)

print("Extracting Data... ")
result = extract(file_path)
print("The Extraction Results Are: ")
print(result)
save_to_json(result)