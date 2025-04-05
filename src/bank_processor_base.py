import csv
import json
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

from .utils import generate_unique_id

class BankProcessor(ABC):
    """Abstract base class for bank statement processors."""
    
    def __init__(self, bank_name: str, config: Dict[str, str]):
        """
        Initialize bank processor with configuration.
        
        :param bank_name: Name of the bank
        :param config: Configuration dictionary with paths and settings
        """
        self.bank_name = bank_name
        self.config = config
        self._validate_config()
        
        # Ensure output directory exists
        os.makedirs(self.config['output_folder'], exist_ok=True)
    
    def _validate_config(self):
        """Validate the configuration dictionary."""
        required_keys = [
            'input_folder', 
            'output_folder', 
            'selenium_folder', 
            'master_file', 
            'selenium_file',
            'placeholder'
        ]
        
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing configuration key: {key}")
    
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
    
    def add_to_json(self, command: str, target: str, value: str) -> Dict[str, Any]:
        """Create a JSON entry for Selenium commands."""
        return {
            'id': generate_unique_id(),
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
    
    def process_file(self, file_name: str) -> None:
        """Process a bank statement file."""
        input_file = os.path.join(self.config['input_folder'], file_name)
        timestamp = self.get_timestamp()
        output_file = os.path.join(
            self.config['output_folder'], 
            f"{self.bank_name.lower().replace(' ', '_')}_output_{timestamp}.txt"
        )
        
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
        self.handler_output_files(data_list, output_file)
    
    def handler_output_files(self, data_list: List[Dict[str, Any]], output_file: str) -> None:
        """Create output files and selenium config."""
        # Save processed data as JSON to a TXT file
        lst_index = len(data_list)
        with open(output_file, mode='w', encoding='utf-8') as outfile:
            for index, entry in enumerate(data_list):
                json.dump(entry, outfile)
                if index < lst_index - 1:
                    outfile.write(',\n')
        
        # Read and modify master selenium file
        input_master_file = os.path.join(
            self.config['selenium_folder'], 
            self.config['master_file']
        )
        with open(input_master_file, 'r') as src:
            destination_content = src.read()
        
        # Read processed data
        with open(output_file, 'r') as dest:
            source_content = dest.read()
        
        # Replace placeholder with processed data
        modified_content = destination_content.replace(
            self.config['placeholder'], 
            source_content
        )
        
        # Write modified content to selenium file
        destination_file = os.path.join(
            self.config['selenium_folder'], 
            self.config['selenium_file']
        )
        with open(destination_file, 'w') as dest:
            dest.write(modified_content)
        
        # Print processing information
        print(f"{self.bank_name} data successfully processed and saved to {output_file}")
        print(f"Selenium file successfully created at {destination_file}")