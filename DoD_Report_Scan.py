# Scan both the DoD Enrollment and DoD Report csv files and store the data in a pandas dataframe.

import pandas as pd

# Take user input for the DoD Enrollment Reg List csv file name and loop until the file is found.
while True:
    try:
        reg_list_path = input("Enter the DoD Enrollment csv file name (e.g. 'filename.csv'): ")
        reg_list = pd.read_csv(reg_list_path, header=0)
        break
    except FileNotFoundError:
        print("File not found. Please enter a valid file name.")
        continue

# Take user input for the DoD Report csv file name and loop until the file is found. 
while True:
    try:
        dod_report_path = input("Enter the DoD Report csv file name (e.g. 'filename.csv'): ")
        dod_report = pd.read_csv(dod_report_path, header=0)
        break
    except FileNotFoundError:
        print("File not found. Please enter a valid file name.")
        continue

# Ensure data types match for merge.
dod_report['student_sis_id'] = dod_report['student_sis_id'].astype(str)
reg_list['Canvas SIS User ID'] = reg_list['Canvas SIS User ID'].astype(str)
reg_list['Unity ID'] = reg_list['Unity ID'].astype(str)

# Merge the DoD Enrollment Reg List and DoD Report data.
report_data = dod_report.merge(reg_list[['Canvas SIS User ID', 'Assigned Advisor: Full Name', 'Unity ID', 'Personal Email', 'Incoming/Returning']], left_on='student_sis_id', right_on='Canvas SIS User ID', how='left')

# Loop through each row in the report data and store the original ally.
for index, row in report_data.iterrows():
    ally = row['allies']
    if ally == '':
        ally = 'blank'
    report_data.at[index, 'original ally'] = ally

# Loop through and set the Assigned Advisor as the advisor for each student.
# Filter grad students to 'Graduate'. The student 'course' will include "DE8W".
for index, row in report_data.iterrows():
    advisor = row['Assigned Advisor: Full Name']
    if advisor == 'To Be Assigned':
        advisor = 'Incoming Team'
        report_data.at[index, 'Assigned Advisor: Full Name'] = advisor

# Check for Ally Mismatch.
report_data['ally_mismatch'] = report_data['original ally'] != report_data['Assigned Advisor: Full Name']
report_data.loc[report_data['ally_mismatch'], 'ally'] = 'Ally Mismatch'

# Export the data for use in other modules.
data = report_data