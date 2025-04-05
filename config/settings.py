import os

# Base directory configuration
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Bank processor configuration
BANK_PROCESSOR_CONFIG = {
    'input_folder': os.path.join(BASE_DIR, 'files\\banks'),
    'output_folder': os.path.join(BASE_DIR, 'files\\processed'),
    'selenium_folder': os.path.join(BASE_DIR, 'files\\selenium'),
    'master_file': 'MinhasEconomiasMaster.side',
    'selenium_file': 'MinhasEconomiasNew.side',
    'placeholder': '<REPLACE_CONTENT_HERE>'
}