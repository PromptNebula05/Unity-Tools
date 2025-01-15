import datetime as dt
import DoD_Report_Scan as ReportScan
import sys
import pandas as pd
import os

def main_menu():
    while True:
        report_data = ReportScan.data

        # Fill missing values in the 'Assingned Advisor: Full Name' column with 'Unknown'.
        report_data['Assigned Advisor: Full Name'].fillna('Unknown', inplace=True)

        # Filter out grad students based on 'course' which will include "DE8W".
        # Filter out hybrid students based on 'allies' containing "Hudnor" or "Konya".
        report_data = report_data[~report_data['course'].str.contains('DE8W', na=False)]
        report_data = report_data[~report_data['allies'].str.contains('Hudnor', na=False)]
        report_data = report_data[~report_data['allies'].str.contains('Konya', na=False)]

        # Print the menu for the user to select an advisor by name or number in a list, including the "Incoming Team" advisor name.
        # Sort the advisor list alphabetically.
        advisor_list = list(report_data['Assigned Advisor: Full Name'].unique())
        advisor_list.sort()
        if 'Incoming Team' not in advisor_list:
            advisor_list.append('Incoming Team')
        print("Select an advisor:")
        for i, advisor in enumerate(advisor_list):
            print(f"{i+1}. {advisor}")

        # Take user input for the advisor name or number and loop until a valid advisor is selected.
        while True:
            advisor_input = input("Enter the advisor name or number: ")
            if advisor_input.isdigit():
                advisor = advisor_list[int(advisor_input)-1]
                break
            elif advisor_input in advisor_list:
                advisor = advisor_input
                break
            else:
                print("Invalid advisor name or number. Please try again.")

        # Print the menu for the user to select an option for the selected advisor.
        while True:
            print(f"\nSelected Advisor: {advisor}")
            print("1. Check for students who have not participated in their course(s) in the past 5 days and have course 0s and/or missing assignments.")
            print(f"2. See all students for {advisor}.")
            print(f"3. List all students whose ally did not match their Assigned Advisor for {advisor}")
            print(f"4. Check students with blank LDA's for {advisor}.")
            print(f"5. Check students with Course and Section mismatches for {advisor}.")
            print("6. Enter '6' to go back and select a different advisor.")
            print("7. Enter '7' to exit the program.")

            # Take user input for the option and loop until a valid option is selected.
            option_input = input("Enter option number: ")
            try:
                option = int(option_input)
                if option in [1, 2, 3, 4, 5, 6, 7]:
                    process_option(option, advisor, report_data)
                else:
                    print("Invalid option. Please enter a valid option number.")
            except ValueError:
                print("Invalid option. Please enter a valid option number.")
            
def process_option(option, advisor, report_data):
    if option == 1:
        # Check for students who have not participated in the past 5 days and have course 0s and/or missing assignments.
        # Print LDA in chronological order for each student, oldest at the top. 
        students = report_data[(report_data['Assigned Advisor: Full Name'] == advisor) & ((report_data['course zero assignments'] > 0) | (report_data['course missing assignments'] > 0)) & (report_data['course lda'] != '')]
        students = students.sort_values(by='course lda')
        if students.empty:
            print(f"\nNo students with blank LDA's for {advisor}.")
            main_menu()
        else:
            print("Students who have not participated in their course(s) in the past 5 days and have course 0s and/or missing assignments:")
            print("---------------------------------------------------------------------------------------------------------------")
            for _, student in students.iterrows():
                course_lda = student['course lda']
                course_lda_date = dt.datetime.strptime(course_lda, '%Y-%m-%d %H:%M:%S+00:00')
                current_date = dt.datetime.now()
                days_since_lda = (current_date - course_lda_date).days
                if days_since_lda >= 5:
                    print(f"Name: {student['student']}")
                    print(f"Unity ID: {student['Unity ID']}")
                    print(f"Course: {student['course']}")
                    print(f"Unity Email: {student['email']}")
                    print(f"Personal Email: {student['Personal Email']}")
                    print(f"Course LDA: {student['course lda']}")
                    print("-----------------------------------------------------------------------------------------------------------------")
            export_data(students)    
    elif option == 2:
        # See all students for the selected advisor.
        students = report_data[report_data['Assigned Advisor: Full Name'] == advisor]
        students = students.sort_values(by='student')
        print(f"\n All students for {advisor}:")
        if students.empty:
            print(f"\nNo students with blank LDA's for {advisor}.")
            main_menu()
        else:        
            print("---------------------------------------------------------------------------------------------------------------")
            count = students['student'].count()
            for _, student in students.iterrows():
                course_lda = student['course lda']
                if pd.isna(course_lda) or course_lda == '':
                    course_lda = 'blank'
                print(f"Name: {student['student']}")
                print(f"Unity ID: {student['Unity ID']}")
                print(f"Course: {student['course']}")
                print(f"Unity Email: {student['email']}")
                print(f"Personal Email: {student['Personal Email']}")
                print(f"Course LDA: {student['course lda']}")
                print("-----------------------------------------------------------------------------------------------------------------")
            print(f"Total: {count} students.")
            export_data(students)
    elif option == 3:
        # List Ally Mismatch students for the selected advisor.
        # Count 'Ally Mismatch' students.
        students = report_data[(report_data['ally'] == 'Ally Mismatch') & (report_data['Assigned Advisor: Full Name'] == advisor)]
        students = students.sort_values(by='student')
        if students.empty:
            print(f"\nNo students with blank LDA's for {advisor}.")
            main_menu()
        else:
            print(f"\nStudents whose ally did not match their Assigned Advisor for {advisor}:")
            print("---------------------------------------------------------------------------------------------------------------")
            count = students['student'].count()
            for _, student in students.iterrows():
                course_lda = student['course lda']
                if pd.isna(course_lda) or course_lda == '':
                    course_lda = 'blank'
                print(f"Name: {student['student']}")
                print(f"Unity ID: {student['Unity ID']}")
                print(f"Ally: {student['original ally']}")
                print(f"Assigned Advisor: {student['Assigned Advisor: Full Name']}")
                print("-----------------------------------------------------------------------------------------------------------------")
            print(f"Total: {count} students.")
            export_report(students)
    elif option == 4:
        students = report_data[(report_data['course lda'].isna()) & (report_data['Assigned Advisor: Full Name'] == advisor)]
        students = students.sort_values(by='student')
        if students.empty:
            print(f"\nNo students with blank LDA's for {advisor}.")
            main_menu()
        else:
            print(f"\nStudents with blank LDA's for {advisor}:")
            print("---------------------------------------------------------------------------------------------------------------")
            for _, student in students.iterrows():
                print(f"Name: {student['student']}")
                print(f"Unity ID: {student['Unity ID']}")
                print(f"Course: {student['course']}")
                print(f"Unity Email: {student['email']}")
                print(f"Personal Email: {student['Personal Email']}")
                print("-----------------------------------------------------------------------------------------------------------------")
            export_data(students)
    # Check for course/section mismatches for students for the selected advisor by checking if all but two of the characters match in the 'course' column of the report_data.
    # DE5W01.13.25_MBAQ315-01: DIVERSITY OF MARINE AND AQUATIC VEGETATION versus DE5W01.13.25_MBAQ315-02: DIVERSITY OF MARINE AND AQUATIC VEGETATION.
    # These are the same course but different sections. 
    elif option == 5:
        students = report_data[report_data['Assigned Advisor: Full Name'] == advisor]
        mismatched_students = []

        def is_same_course_different_section(course1, course2):
            # Assuming the section is the last part after the last hyphen
            base_course1 = course1.rsplit('-', 1)[0]
            base_course2 = course2.rsplit('-', 1)[0]
            return base_course1 == base_course2 and course1 != course2

        grouped_students = students.groupby('Unity ID')
        for unity_id, group in grouped_students:
            if len(group) > 1:
                for i, student1 in group.iterrows():
                    for j, student2 in group.iterrows():
                        if i >= j:
                            continue
                        if is_same_course_different_section(student1['course'], student2['course']):
                            mismatched_students.append(student1)
                            mismatched_students.append(student2)
        mismatched_students = pd.DataFrame(mismatched_students).drop_duplicates().sort_values(by='student')

        if mismatched_students.empty:
            print(f"\nNo students with Course and Section mismatches for {advisor}.")
            main_menu()
        else:
            print(f"\nStudents with Course and Section mismatches for {advisor}:")
            print("---------------------------------------------------------------------------------------------------------------")
            for _, student in mismatched_students.iterrows():
                print(f"Name: {student['student']}")
                print(f"Unity ID: {student['Unity ID']}")
                print(f"Course: {student['course']}")
                print(f"Unity Email: {student['email']}")
                print(f"Personal Email: {student['Personal Email']}")
                print("-----------------------------------------------------------------------------------------------------------------")
            export_data(mismatched_students)
            
    elif option == 6:
        main_menu()    
    elif option == 7:
        print("Exiting program...")
        sys.exit()

def export_data(data):
    while True:
        try:
            # Define the path to the reports folder in the Downloads directory
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            reports_folder = os.path.join(downloads_path, "Reports")
            os.makedirs(reports_folder, exist_ok=True)

            filename = input("Enter the filename to export the data (e.g., 'filename.csv'): ")
            filename = os.path.join(reports_folder, filename)

            # Select the specific columns to export
            export_columns = ['student', 'Unity ID', 'course', 'email', 'Personal Email', 'course lda']
            export_data = data[export_columns]
            # Rename columns to match the desired headers
            export_data.columns = ['Name', 'Unity ID', 'Course', 'Unity Email', 'Personal Email', 'Course LDA']
            export_data.to_csv(filename, index=False)
            print(f"Data exported to {filename}.")
            main_menu()
        except Exception as e:
            print(f"Error exporting data: {e}. Please try again.")

def export_report(data):
    while True:
        try:
            # Define the path to the reports folder in the Downloads directory
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            reports_folder = os.path.join(downloads_path, "Reports")
            os.makedirs(reports_folder, exist_ok=True)

            filename = input("Enter the filename to export the report (e.g., 'filename.csv'): ")
            filename = os.path.join(reports_folder, filename)

            # Select the specific columns to export
            export_columns = ['student', 'Unity ID', 'original ally', 'Assigned Advisor: Full Name']
            export_data = data[export_columns]
            # Rename columns to match the desired headers
            export_data.columns = ['Name', 'Unity ID', 'Ally', 'Assigned Advisor']
            export_data.to_csv(filename, index=False)
            print(f"Report exported to {filename}.")
            break
        except Exception as e:
            print(f"Error exporting report: {e}. Please try again.")

if __name__ == "__main__":
    main_menu()
    print("Exiting program...")
    sys.exit()
