import pandas as pd
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Process a CSV file.')
parser.add_argument('-i', '--input', metavar='InputFile', type=str, help='The path to the input file', required=True)
parser.add_argument('-o', '--output', metavar='OutputFile', type=str, help='The path to the output file. Default output (output.xlsx) file is stored is stored in the same directory of execution', default='output44.xlsx')

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

    # Normalize the status values
    if status == "[FAILED]":
        status = "Failed"
    elif status == "[PASSED]":
        status = "Passed"
    elif status == "[WARNING]":
        status = "Failed"

    # Find indices for "Rationale" and "Solution" to accurately extract the "Control Point"
    rationale_index = entry.find("\n\nRationale:")
    solution_start_index = entry.find("Solution:")
    solution_end_index = entry.find("See Also:") if entry.find("See Also:") != -1 else len(entry)
    control_point_end_index = rationale_index if rationale_index != -1 else solution_start_index
    control_point = entry[entry.find("]") + 1:control_point_end_index].strip()
    
    # Extract "Rationale" and "Solution"
    rationale = entry[rationale_index:solution_start_index].replace("Rationale:", "").strip() if rationale_index != -1 else ""
    solution = entry[solution_start_index:solution_end_index].replace("Solution:", "In order to Mitigate:\n").strip() if solution_start_index != -1 else ""

    # Extract "Policy Value" and "Actual Value"
    policy_value_start_index = entry.find("Policy Value:")
    actual_value_start_index = entry.find("Actual Value:")
    policy_value = entry[policy_value_start_index:actual_value_start_index].replace("Policy Value:", "").strip() if policy_value_start_index != -1 else ""
    actual_value = entry[actual_value_start_index:].replace("Actual Value:", "").strip() if actual_value_start_index != -1 else ""

    # Extract "See Also" and "Reference"
    see_also_start_index = entry.find("See Also:")
    reference_start_index = entry.find("Reference:")
    see_also = entry[see_also_start_index:reference_start_index].replace("See Also:", "").strip() if see_also_start_index != -1 else ""
    reference = entry[reference_start_index:policy_value_start_index].replace("Reference:", "").strip() if reference_start_index != -1 else ""

    # Append the structured data to the list
    structured_data_list.append({
        "Control Statement": control_statement,
        "Status": status if status else "N/A",
        "Control Point": control_point,
        "Rationale": rationale,
        "Solution": solution,
        "Policy Value": policy_value,
        "Actual Value": actual_value,
        "See Also": see_also,
        "Reference": reference
    })

# Convert the list to a DataFrame
structured_data = pd.DataFrame(structured_data_list)

# Save the structured data
structured_data.to_excel(args.output, index=False)
