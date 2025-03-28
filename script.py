import csv
import json
import os
from datetime import datetime
import uuid
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple

class BankProcessor(ABC):
    """Abstract base class for bank statement processors."""
    
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.input_folder = "banks"
        self.output_folder = "processed"
        self.selenium_folder = "selenium"
        self.placeholder = "<REPLACE_CONTENT_HERE>"
        self.master_file = "MinhasEconomiasMaster.side"
        self.selenium_file = "MinhasEconomiasNew.side"
        
        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)
    
    @abstractmethod
    def convert_date_format(self, date_str: str) -> str:
        """Convert date format from bank-specific to DD/MM/YYYY."""
        pass
    
    @abstractmethod
    def process_row(self, row: Dict[str, str]) -> Tuple[str, str, str, float]:
        """Process a row of bank statement data."""
        pass
    
    def get_timestamp(self) -> str:
        """Get current timestamp in yyyymmddhhmmss format."""
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    def generate_unique_id(self) -> str:
        """Generate a unique ID for JSON entries."""
        return str(uuid.uuid4())
    
    def add_to_json(self, command: str, target: str, value: str) -> Dict[str, Any]:
        """Create a JSON entry for Selenium commands."""
        return {
            'id': self.generate_unique_id(),
            "comment": "",
            "command": command,
            "target": target,
            "targets": [],
            'value': value
        }
    
    def add_item(self, date: str, description: str, value: str, value_float: float) -> List[Dict[str, Any]]:
        """Generate Selenium commands for adding a transaction."""
        data_list = []
        
        # Add basic transaction information
        data_list.append(self.add_to_json('type', 'id=ext-comp-1814', date))
        data_list.append(self.add_to_json('type', 'id=ext-comp-1816', description))
        data_list.append(self.add_to_json('pause', '1000', ''))
        
        # Select transaction type
        if value_float < 0:
            # Expense
            data_list.append(self.add_to_json('click', 'id=ext-comp-1884', ''))
        else:
            # Income
            data_list.append(self.add_to_json('click', 'id=ext-comp-1886', ''))
        
        # Add country and value
        data_list.append(self.add_to_json('type', 'id=ext-comp-1821', 'Can'))
        data_list.append(self.add_to_json('type', 'id=ext-comp-1821', 'Canada'))
        data_list.append(self.add_to_json('sendKeys', 'id=ext-comp-1821', '${KEY_ENTER}'))
        data_list.append(self.add_to_json('type', 'id=ext-comp-1825', value))
        data_list.append(self.add_to_json('sendKeys', 'id=ext-comp-1825', '${KEY_ENTER}'))
        
        # Wait for confirmation and completion
        data_list.append(self.add_to_json('waitForElementVisible', "xpath=//*[contains(text(), 'adicionada com sucesso')]", '30000'))
        data_list.append(self.add_to_json('waitForElementNotVisible', "xpath=//*[contains(text(), 'adicionada com sucesso')]", '80000'))
        
        return data_list
    
    def handler_output_files(self, data_list: List[Dict[str, Any]], output_file: str) -> str:
        """Create output files and selenium config."""
        # Save processed data as JSON to a TXT file
        lst_index = len(data_list)
        with open(output_file, mode='w', encoding='utf-8') as outfile:
            for index, entry in enumerate(data_list):
                json.dump(entry, outfile)
                if index < lst_index - 1:
                    outfile.write(',\n')
        
        # Read and modify master selenium file
        input_master_file = os.path.join(self.selenium_folder, self.master_file)
        with open(input_master_file, 'r') as src:
            destination_content = src.read()
        
        # Read processed data
        with open(output_file, 'r') as dest:
            source_content = dest.read()
        
        # Replace placeholder with processed data
        modified_content = destination_content.replace(self.placeholder, source_content)
        
        # Write modified content to selenium file
        destination_file = os.path.join(self.selenium_folder, self.selenium_file)
        with open(destination_file, 'w') as dest:
            dest.write(modified_content)
        
        return destination_file
    
    def process_file(self, file_name: str) -> None:
        """Process a bank statement file."""
        input_file = os.path.join(self.input_folder, file_name)
        timestamp = self.get_timestamp()
        output_file = os.path.join(self.output_folder, f"{self.bank_name}_output_{timestamp}.txt")
        
        data_list = []
        
        # Add initial action
        data_list.append(self.add_to_json('click', 'css=#ext-comp-1193 .x-btn-mc', ''))
        
        # Read and process CSV file
        with open(input_file, mode='r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                date, description, value, value_float = self.process_row(row)
                data_list.extend(self.add_item(date, description, value, value_float))
        
        # Generate output files
        destination_file = self.handler_output_files(data_list, output_file)
        
        print(f"{self.bank_name} data successfully processed and saved to {output_file}")
        print(f"Selenium file successfully created at {destination_file}")


class PCBankProcessor(BankProcessor):
    """Processor for PC Bank statements."""
    
    def __init__(self):
        super().__init__("PC Bank")
    
    def convert_date_format(self, date_str: str) -> str:
        """Convert MM/DD/YYYY to DD/MM/YYYY."""
        month, day, year = date_str.split('/')
        return f"{day}/{month}/{year}"
    
    def process_row(self, row: Dict[str, str]) -> Tuple[str, str, str, float]:
        """Process a row from PC Bank statement."""
        date = self.convert_date_format(row['Date'])
        value = row['Amount'].replace('.', ',')
        value_float = float(row['Amount'])
        description = row['Description']
        
        return date, description, value, value_float


class CIBCBankProcessor(BankProcessor):
    """Processor for CIBC Bank statements."""
    
    def __init__(self):
        super().__init__("CIBC Bank")
    
    def convert_date_format(self, date_str: str) -> str:
        """Convert YYYY-MM-DD to DD/MM/YYYY."""
        year, month, day = date_str.split('-')
        return f"{day}/{month}/{year}"
    
    def process_row(self, row: Dict[str, str]) -> Tuple[str, str, str, float]:
        """Process a row from CIBC Bank statement."""
        date = self.convert_date_format(row['Date'])
        description = row['Description']
        
        debit = row['Debit']
        credit = row['Credit']
        if debit:
            value = debit.replace('.', ',')
            value_float = -abs(float(debit))
        else:
            value = credit.replace('.', ',')
            value_float = float(credit)
        
        return date, description, value, value_float


class RBCBankProcessor(BankProcessor):
    """Processor for RBC Bank statements."""
    
    def __init__(self):
        super().__init__("RBC Bank")
    
    def convert_date_format(self, date_str: str) -> str:
        """Convert MM/DD/YYYY to DD/MM/YYYY."""
        month, day, year = date_str.split('/')
        return f"{day}/{month}/{year}"
    
    def process_row(self, row: Dict[str, str]) -> Tuple[str, str, str, float]:
        """Process a row from RBC Bank statement."""
        date = self.convert_date_format(row['Date'])
        value = row['Amount'].replace('.', ',')
        value_float = float(row['Amount'])
        description = row['Description']
        
        return date, description, value, value_float


class BankProcessorFactory:
    """Factory for creating bank processors."""
    
    @staticmethod
    def create_processor(bank_type: str) -> Optional[BankProcessor]:
        """Create appropriate bank processor based on type."""
        processors = {
            '1': PCBankProcessor,
            '2': CIBCBankProcessor,
            '3': RBCBankProcessor
        }
        
        processor_class = processors.get(bank_type)
        if processor_class:
            return processor_class()
        return None


def display_menu() -> None:
    """Display menu for bank selection."""
    print("\nSelect a bank to process the file:")
    print("1. PC Bank")
    print("2. CIBC Bank")
    print("3. RBC Bank")
    print("0. Exit")


def main() -> None:
    """Main function to run the program."""
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '0':
            print("Exiting...")
            break
        
        processor = BankProcessorFactory.create_processor(choice)
        if processor:
            file_name = input(f"Enter the {processor.bank_name} CSV file name (with extension): ")
            processor.process_file(file_name)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()