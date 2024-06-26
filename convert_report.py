import pandas as pd
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process a CSV file.')
parser.add_argument('-i', '--input', metavar='InputFile', type=str, help='The path to the input file', required=True)
parser.add_argument('-o', '--output', metavar='OutputFile', type=str, help='The path to the output file. Default output (output.xlsx) file is stored is stored in the same directory of execution', default='output_processed.xlsx')

# Parse the arguments
args = parser.parse_args()

# Load the CSV file
file_path = args.input
csv_data = pd.read_csv(file_path)

# Initialize an empty list to store the structured data
structured_data_list = []

# Perform the operation on the "Description" column
for entry in csv_data["Description"]:
    # Split the entry based on "Rationale" and "Solution" sections
    sections = entry.split("\n\n")
    control_statement, status = sections[0].rsplit(":", 1)  # Split at the last colon
    control_statement = control_statement.strip()
    status = status.strip()

    # Find indices for "Rationale" and "Solution" to accurately extract the "Control Point"
    rationale_index = entry.find("\n\nRationale:")
    control_point_end_index = rationale_index if rationale_index != -1 else entry.find("\n\nSolution:")
    control_point = entry[entry.find("]") + 1:control_point_end_index].strip()
    
    # Extract "Rationale" and "Solution"
    rationale_start_index = entry.find("Rationale:")
    solution_start_index = entry.find("Solution:")
    output_start_index = entry.find("Policy Value:")
    rationale = entry[rationale_start_index:solution_start_index].replace("Rationale:", "").strip() if rationale_start_index != -1 else ""
    solution = entry[solution_start_index:output_start_index].replace("Solution:", "In order to Mitigate:\n").strip() if solution_start_index != -1 else ""
    output = entry[output_start_index:].replace("", "").strip() if output_start_index != -1 else ""

    # Append the structured data to the list
    structured_data_list.append({
        "Control Statement": control_statement,
        "Status": status if status else "N/A",
        "Control Point": control_point,
        "Rationale": rationale,
        "Solution": solution,
        "Output": output
    })

# Convert the list to a DataFrame
structured_data = pd.DataFrame(structured_data_list)

# Save the structured data
structured_data.to_excel(args.output, index=False)
