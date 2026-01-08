#Onetime used program for extracting data from student Admission forms ot excel file 
# Creates
from docstrange import DocumentExtractor
import csv
import os

# Authenticated access - run 'docstrange login' first
extractor = DocumentExtractor(api_key="2091d216-87fe-11f0-9813-2ebbabb9cbf8")

csv_filename = "newdata.csv"

fieldnames = [
    "Name",
    "Father name",
    "Date of birth",
    "Class",
    "contact",
    "Address",
]
 
# Check if the file exists to determine if headers need to be written
file_exists = os.path.isfile(csv_filename)

# Open the CSV file in append mode. The headers will be written only if the file is new.
with open(csv_filename, "a", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header row only if the file did not exist before
    if not file_exists:
        writer.writeheader()

    # Loop through your documents and extract data
    for i in range(1, 10):
        if i < 10:
            path = f"Filename({i}).jpeg"
        else:
            path = f"Filename{i}.jpg"

        try:
            result = extractor.extract(path)
            data = result.extract_data(specified_fields=fieldnames)

            # The .extract_data() method returns the 'extracted_fields' dictionary
            # directly when you use 'specified_fields'.
            # It's better practice to assign it to a variable for clarity.
            extracted_fields = data.get("extracted_fields", {})

            # Check if any data was actually extracted before writing
            if extracted_fields:
                writer.writerow(extracted_fields)
                print(
                    f"Data from {os.path.basename(path)} successfully written to CSV."
                )
            else:
                print(f"No data extracted from {os.path.basename(path)}.")

        except Exception as e:
            print(f"Error processing {os.path.basename(path)}: {e}")
