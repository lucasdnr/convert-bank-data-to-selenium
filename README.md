# Bank Data to Selenium Script Converter

This Python program reads CSV bank files from different banks (PC Bank, CIBC Bank, RBC Bank), processes the transaction data and converts it into a Selenium IDE `.side` script that can automatically input the data into the [MinhasEconomias](https://www.minhaseconomias.com.br/) website.

## Features

- **Multi-bank support**: The program currently supports CSV exports from PC Bank, CIBC Bank, and RBC Bank.
- **Date conversion**: Converts dates from the format used by the banks to the format required by MinhasEconomias (DD/MM/YYYY).
- **Transaction categorization (Debit/Credit)**: Identifies whether a transaction is an expense or income based on the amount.
- **Automated web interaction**: Generates Selenium IDE-compatible scripts that automate the input of transaction data into the MinhasEconomias website.
- **Customizable**: The solution can be adapted to other banks or websites with similar requirements.

## Project Structure

```
.
├── banks/                     # Folder containing the input CSV files from the banks.
├── processed/                 # Folder for the intermediate output files generated.
├── selenium/                  # Folder containing the Selenium script template and output.
│   ├── MinhasEconomiasMaster.side   # Selenium master file with a placeholder for the transactions.
│   ├── MinhasEconomiasNew.side      # Selenium script generated after processing the CSV data.
├── script.py          # Main Python script for processing and generating Selenium scripts.
```

## How It Works

1. **User input**: The user selects which bank's CSV file to process via the command-line interface.
2. **Data parsing**: The script reads the CSV file, processes the date formats, transaction descriptions, and values.
3. **Selenium script generation**: The transaction data is formatted into Selenium commands, and the placeholders in the master Selenium file are replaced with the actual data.
4. **Selenium execution**: The generated Selenium `.side` file can then be used with the Selenium IDE to automatically input the transactions into MinhasEconomias.

## Prerequisites

- Python 3.x
- Selenium IDE installed in your browser (for running the generated `.side` file)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/lucasdnr/convert-bank-data-to-selenium.git
   cd convert-bank-data-to-selenium
   ```

2. **Install dependencies** (optional):
   There are no external Python libraries used in this script, but ensure that Python 3.x is installed.

## Usage

1. **Prepare the input files**:
   - Place the CSV export files from your bank in the `banks/` directory.

2. **Run the program**:
   ```bash
   python script.py
   ```

3. **Select your bank** and provide the CSV filename when prompted:
   ```
   Select a bank to process the file:
   1. PC Bank
   2. CIBC Bank
   3. RBC Bank
   0. Exit
   ```

4. **Check output**:
   - The processed transaction data will be saved in the `processed/` folder.
   - The final Selenium `.side` script will be saved in the `selenium/` folder.

5. **Run the Selenium script**:
   - Open Selenium IDE in your browser.
   - Load the `MinhasEconomiasNew.side` file.
   - Run the script to automatically input your bank transactions into MinhasEconomias (May Sign-In MinhasEconomias is required).

## Extending the Program

To add support for another bank:
1. Create a new function similar to `process_pc_bank` for the new bank's CSV format.
2. Implement date format conversion if necessary.
3. Add the function to the menu in the `main()` function.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or new features.

## License

This project is licensed under the MIT License. 
