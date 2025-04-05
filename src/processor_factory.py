from typing import Dict, Optional

from .bank_processors import (
    PCBankProcessor, 
    CIBCBankProcessor, 
    RBCBankProcessor
)
from .bank_processor_base import BankProcessor

class BankProcessorFactory:
    """Factory for creating bank processors."""
    
    @staticmethod
    def create_processor(
        bank_type: str, 
        config: Dict[str, str]
    ) -> Optional[BankProcessor]:
        """
        Create appropriate bank processor based on type.
        
        :param bank_type: Identifier for the bank type
        :param config: Configuration dictionary for file paths and settings
        :return: Instantiated bank processor or None if invalid type
        """
        processors = {
            '1': PCBankProcessor,
            '2': CIBCBankProcessor,
            '3': RBCBankProcessor
        }
        
        processor_class = processors.get(bank_type)
        if processor_class:
            return processor_class(config)
        return None