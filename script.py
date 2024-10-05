import csv
import json
import os
from datetime import datetime
import uuid

# Define paths for the input and output files
input_folder = "banks"
output_folder = "processed"
selenium_folder = "selenium"
placeholder = "<REPLACE_CONTENT_HERE>"
master_file = "MinhasEconomiasMaster.side"
selenium_file = "MinhasEconomiasNew.side"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to get the current timestamp in yyyymmddhhmmss format
def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

# Function to convert MM/DD/YYYY to DD/MM/YYYY


def convert_date_format(date_str):
    month, day, year = date_str.split('/')
    return f"{day}/{month}/{year}"

# Function to generate a unique ID


def generate_unique_id():
    return str(uuid.uuid4())


def add_item(date, description, value, value_float):
    data_list = []

    # Append the processed data to a list with the unique ID
    data_list.append(add_to_json('type', 'id=ext-comp-1814', date))
    data_list.append(add_to_json('type', 'id=ext-comp-1816', description))
    data_list.append(add_to_json('pause', '1000', ''))
    
    if value_float < 0:
        # type expenses
        data_list.append(add_to_json('click', 'id=ext-comp-1884', ''))
    else:
        # type income
        data_list.append(add_to_json('click','id=ext-comp-1886',''))

    data_list.append(add_to_json('type','id=ext-comp-1821','Can'))
    data_list.append(add_to_json('type','id=ext-comp-1821','Canada'))
    data_list.append(add_to_json('sendKeys','id=ext-comp-1821','${KEY_ENTER}'))
    data_list.append(add_to_json('type','id=ext-comp-1825',value))
    data_list.append(add_to_json('sendKeys','id=ext-comp-1825','${KEY_ENTER}'))
    data_list.append(add_to_json('waitForElementVisible',"xpath=//*[contains(text(), 'adicionada com sucesso')]",'30000'))
    data_list.append(add_to_json('waitForElementNotVisible',"xpath=//*[contains(text(), 'adicionada com sucesso')]",'80000'))

    return data_list

def add_to_json(command, target, value):
    # Generate unique ID
    unique_id = generate_unique_id()

    data = {
        'id': unique_id,
        "comment": "",
        "command": command,
        "target": target,
        "targets": [],
        'value': value
    }

    return data

def handler_output_files(data_list, output_file):
    # Serializing json
    # json_object = json.dumps(data_list, indent=4)

    # Save the processed data as JSON to a TXT file
    lstindex = len(data_list)
    with open(output_file, mode='w', encoding='utf-8') as outfile:
        # outfile.write(json_object)
        # for entry in data_list:
        for index, entry in enumerate(data_list):    
            json.dump(entry, outfile)
            if index < lstindex - 1:
                outfile.write(',\n')

    # Read content from the MASTER file
    input_master_file = os.path.join(selenium_folder, master_file)
    with open(input_master_file, 'r') as src:
        destination_content = src.read()
    
    # Read content from the destination file
    with open(output_file, 'r') as dest:
        source_content = dest.read()

    # Replace the placeholder with the source content
    modified_content = destination_content.replace(placeholder, source_content)

    # Write the modified content back into the destination file
    destination_file =  os.path.join(selenium_folder, selenium_file)
    with open(destination_file, 'w') as dest:
        dest.write(modified_content)

    return destination_file

# PC Bank function to process the CSV file
def process_pc_bank(file_name):
    input_file = os.path.join(input_folder, file_name)
    timestamp = get_timestamp()
    output_file = os.path.join(output_folder, f"pc_bank_output_{timestamp}.txt")

    data_list = []
    with open(input_file, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        #Append Initial Action
        data_list.append(add_to_json('click','css=#ext-comp-1193 .x-btn-mc',''))
        
        for row in csv_reader:
            # Convert date format
            date = convert_date_format(row['Date'])
            
            # Replace periods by commas
            value = row['Amount'].replace('.', ',')
            value_float = float(row['Amount'])
            
            # Description
            description = row['Description']

            # add item        
            data_list = data_list + add_item(date, description, value, value_float)

    # handler files
    destination_file = handler_output_files(data_list, output_file)

    print(f"PC Bank data successfully processed and saved to {output_file}")
    print(f"Selenium file successfully created to  {destination_file}")

# CIBC Bank function to process the CSV file
def process_cibc_bank(file_name):
    # Save the processed data as JSON to a TXT file
    with open(output_file, mode='w', encoding='utf-8') as txt_file:
        for entry in data_list:
            json.dump(entry, txt_file)
            txt_file.write('\n')

    print(f"CIBC Bank data successfully processed and saved to {output_file}")

# RBC Bank function to process the CSV file
def process_rbc_bank(file_name):

    # Save the processed data as JSON to a TXT file
    with open(output_file, mode='w', encoding='utf-8') as txt_file:
        for entry in data_list:
            json.dump(entry, txt_file)
            txt_file.write('\n')

    print(f"RBC Bank data successfully processed and saved to {output_file}")

# Menu function to choose the bank
def display_menu():
    print("Select a bank to process the file:")
    print("1. PC Bank")
    print("2. CIBC Bank")
    print("3. RBC Bank")
    print("0. Exit")

# Main function to run the menu
def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            file_name = input("Enter the PC Bank CSV file name (with extension): ")
            process_pc_bank(file_name)
        elif choice == '2':
            file_name = input("Enter the CIBC Bank CSV file name (with extension): ")
            process_cibc_bank(file_name)
        elif choice == '3':
            file_name = input("Enter the RBC Bank CSV file name (with extension): ")
            process_rbc_bank(file_name)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
