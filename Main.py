import datetime as dt
import DoD_Report_Scan as ReportScan

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
            print("5. Enter '5' to go back and select a different advisor.")
            print("6. Enter '6' to exit the program.")

            # Take user input for the option and loop until a valid option is selected.
            option_input = input("Enter option number: ")
            try:
                option = int(option_input)
                if option in [1, 2, 3, 4, 5, 6]:
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
    elif option == 2:
        # See all students for the selected advisor.
        students = report_data[report_data['Assigned Advisor: Full Name'] == advisor]
        students = students.sort_values(by='student')
        print(f"\n All students for {advisor}:")
        print("---------------------------------------------------------------------------------------------------------------")
        count = students['student'].count()
        for _, student in students.iterrows():
            print(f"Name: {student['student']}")
            print(f"Unity ID: {student['Unity ID']}")
            print(f"Course: {student['course']}")
            print(f"Unity Email: {student['email']}")
            print(f"Personal Email: {student['Personal Email']}")
            print(f"Course LDA: {student['course lda']}")
            print("-----------------------------------------------------------------------------------------------------------------")
        print(f"Total: {count} students.")
    elif option == 3:
        # List Ally Mismatch students for the selected advisor.
        # Count 'Ally Mismatch' students.
        students = report_data[(report_data['ally'] == 'Ally Mismatch') & (report_data['Assigned Advisor: Full Name'] == advisor)]
        students = students.sort_values(by='student')
        print(f"\nStudents whose ally did not match their Assigned Advisor for {advisor}:")
        print("---------------------------------------------------------------------------------------------------------------")
        count = students['student'].count()
        for _, student in students.iterrows():
            print(f"Name: {student['student']}")
            print(f"Unity ID: {student['Unity ID']}")
            print(f"Ally: {student['original ally']}")
            print(f"Assigned Advisor: {student['Assigned Advisor: Full Name']}")
            print("-----------------------------------------------------------------------------------------------------------------")
        print(f"Total: {count} students.")
    elif option == 4:
        students = report_data[(report_data['course lda'].isna()) & (report_data['Assigned Advisor: Full Name'] == advisor)]
        students = students.sort_values(by='student')
        print(f"\nStudents with blank LDA's for {advisor}:")
        print("---------------------------------------------------------------------------------------------------------------")
        for _, student in students.iterrows():
            print(f"Name: {student['student']}")
            print(f"Unity ID: {student['Unity ID']}")
            print(f"Course: {student['course']}")
            print(f"Unity Email: {student['email']}")
            print(f"Personal Email: {student['Personal Email']}")
            print("-----------------------------------------------------------------------------------------------------------------")
    elif option == 5:
        main_menu()    
    elif option == 6:
        print("Exiting program...")
        exit()

if __name__ == "__main__":
    main_menu()
    print("Exiting program...")
    exit()