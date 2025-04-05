from src.processor_factory import BankProcessorFactory
from config.settings import BANK_PROCESSOR_CONFIG

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
        
        processor = BankProcessorFactory.create_processor(choice, BANK_PROCESSOR_CONFIG)
        if processor:
            file_name = input(f"Enter the {processor.bank_name} CSV file name (with extension): ")
            processor.process_file(file_name)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()