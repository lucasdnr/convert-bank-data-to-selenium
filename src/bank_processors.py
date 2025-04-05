from typing import Dict, Tuple

from .bank_processor_base import BankProcessor

class PCBankProcessor(BankProcessor):
    """Processor for PC Bank statements."""
    
    def __init__(self, config: Dict[str, str]):
        super().__init__("PC Bank", config)
    
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
    
    def __init__(self, config: Dict[str, str]):
        super().__init__("CIBC Bank", config)
    
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
    
    def __init__(self, config: Dict[str, str]):
        super().__init__("RBC Bank", config)
    
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