# nessus-compliance-report-converter
This Python script converts compliance reports from Nessus, provided in CSV format, into a more structured Excel (xlsx) format. The script specifically extracts and organizes information about each control point, including its status (Passed or Failed).

## Prerequisites
- Python 3.12 or higher
- pandas
- argparse
You can install the required Python packages using pip:
  ```shell
  pip install pandas argparse openpyxl
  ```

## Usage
1. Clone this repository:
    ```shell
    git clone https://github.com/iammainul/nessus-compliance-report-converter.git
    ```
2. The script requires an input CSV file and an output file path as arguments. The input file should be a Nessus compliance report in CSV format. The output file will be an Excel file containing the structured data. Here's how to run the script:
   ```shell
   python convert_report.py -i input.csv -o output.xlsx
   # Replace input.csv with the path to your input file, and output.xlsx with the path where you want the output file to be saved. 
   # If the output file path is not provided, the script will save the output as output.xlsx in the current directory.
   ```

## Output
The output Excel file will contain the following columns:
 - Control Statement: The control statement extracted from the Description column of the input file.
 - Status: The status of the control point (Passed or Failed).
 - Control Point: The control point extracted from the Description column.
 - Rationale: The rationale for the control point, if provided in the Description.
 - Solution: The solution for the control point, if provided in the Description.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
