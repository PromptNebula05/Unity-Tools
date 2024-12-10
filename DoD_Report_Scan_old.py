# This program will sort the DoD Report csv file by ally (column 8) and check for 
# students who have not participated in their course(s) within the last 7 days and have
# course missing assignments and course zero assignments. 
# The program will then print the student's name (column 1), the course name (column 11), Unity email (column 4),
# and the course lda (column 15). 
# This will be presented in a table format. 
# The program will print out a menu of options for the user to select from. The first menu will be to select an ally.
# The following menu will print 2 options. The first, to check for students who have not participated in their course(s)
# and have course 0s (column 14) and missing assignments (column 13). The program will then print the student's name (column 1),
# the course name (column 11), Unity email (column 4), and the course lda (column 15).
# The second option will be to see all students for that particular ally.
# The program will then print the student's name, the course name, Unity email, and the date of the last activity (LDA) for the course.
# If the ally is not found, the program will store the student data under a 'blank' ally name. 

# Importing necessary libraries
import pandas as pd
import datetime

# Take user input for the DoD Report csv file name and loop until the file is found. 
# If the file is not found, the user will be prompted to enter the file name again.
while True:
    try:
        file_name = input("Enter the DoD Report csv file name (e.g. 'DoD_YYYMMDD.csv'): ")
        with open(file_name, 'r') as file:
            break
    except FileNotFoundError:
        print("File not found. Please enter a valid file name.")
        continue

# Read the csv file and store the data in a pandas dataframe
data = pd.read_csv(file_name)

# Replace NaN values in the 'allies' column with 'blank'
data.loc[:, 'allies'] = data['allies'].fillna('blank')

# Create a dictionary ally_dict to store the student data by ally
ally_dict = {}

# Loop through the data and store the student data by ally in the ally_dict.
# If the ally field is blank, store the student data under a 'blank' ally name.
for index, row in data.iterrows():
    student = row['student']
    course = row['course']
    email = row['email']
    course_missing_assignments = row['course missing assignments']
    course_zero_assignments = row['course zero assignments']
    course_lda = row['course lda']
    course_last_access = row['course last access']
    ally = row['allies']
    if ally in ally_dict:
        ally_dict[ally].append({'student': student, 'course': course, 'email': email, 'course missing assignments': course_missing_assignments, 'course zero assignments': course_zero_assignments, 'course lda': course_lda, 'course last access': course_last_access})
    else:
        ally_dict[ally] = [{'student': student, 'course': course, 'email': email, 'course missing assignments': course_missing_assignments, 'course zero assignments': course_zero_assignments, 'course lda': course_lda, 'course last access': course_last_access}]

# Ensure 'blank' key exists in ally_dict
if 'blank' not in ally_dict:
    ally_dict['blank'] = []

# Print the menu for the user to select an ally by name or number in a list, including the 'blank' ally name.
ally_list = list(ally_dict.keys())
ally_list = [str(ally) for ally in ally_list]  # Convert all elements to strings
ally_list.sort()
ally_menu = {}
for i, ally in enumerate(ally_list):
    ally_menu[i] = ally
    print(f"{i}: {ally}")

# Take user input for the ally selection and loop until a valid ally is selected.
# If an invalid ally is selected, the user will be prompted to enter the ally again.
while True:
    try:
        ally_selection = int(input("Select an advisor by number: "))
        if ally_selection in ally_menu:
            selected_ally = ally_menu[ally_selection]
            break
        else:
            print("Invalid selection. Please select an advisor by number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    
# Print the menu for the user to select an option for the selected ally.
# The first option is to check for students who have not participated in their course(s) within the last 7 days and have course 0s and/ or missing assignments.
# The second option is to see all students for that particular ally.
# Loop until a valid option is selected.
# If an invalid option is selected, the user will be prompted to enter the option again.
# The last option is to navigate back to the ally selection menu.
while True:
    print(f"Selected advisor: {selected_ally}")
    print("Select an option:")
    print("1: Check for students who have not participated in their course(s) within the last 7 days and have course 0s and/ or missing assignments.")
    print("2: See all students for this advisor.")
    print("3: Select a different advisor.")
    try:
        option = int(input("Enter option number: "))
        if option == 1 or option == 2 or option == 3:
            break
        else:
            print("Invalid option. Please enter a valid option number.")
            continue
    except ValueError:
        print("Invalid option. Please enter a valid option number.")
        continue

# If option 1 is selected, check for students who's course lda is 7 days or greater and have course 0s and/ or missing assignments.
# Print the student's name, course name, Unity email, and course lda.
if option == 1:
    print("Students who have not participated in their course(s) within the last 7 days and have course 0s and/ or missing assignments:")
    print("-----------------------------------------------------------------------------------------------------------------")
    for student_data in ally_dict[selected_ally]:
        course_lda = student_data['course lda']
        course_lda_date = datetime.datetime.strptime(course_lda, '%Y-%m-%d %H:%M:%S+00:00')
        current_date = datetime.datetime.now()
        days_since_lda = (current_date - course_lda_date).days
        if days_since_lda >= 7 and (student_data['course missing assignments'] > 0 or student_data['course zero assignments'] > 0):
            print(f"Student: {student_data['student']}")
            print(f"Course: {student_data['course']}")
            print(f"Unity Email: {student_data['email']}")
            print(f"Course LDA: {student_data['course lda']}")
            print("-----------------------------------------------------------------------------------------------------------------")

# If option 2 is selected, print all students for the selected ally.
# Print the student's name, course name, Unity email, and course lda.
elif option == 2:
    print("All students for this advisor:")
    print("-----------------------------------------------------------------------------------------------------------------")
    for student_data in ally_dict[selected_ally]:
        print(f"Student: {student_data['student']}")
        print(f"Student ID: {student_data['student id']}")
        print(f"Course: {student_data['course']}")
        print(f"Unity Email: {student_data['email']}")
#       print(f"Personal Email: {student_data['personal email']}") 
        print(f"Course LDA: {student_data['course lda']}")
        print("-----------------------------------------------------------------------------------------------------------------")

# If option 3 is selected, navigate back to the ally selection menu.
elif option == 3:
    print("Select a different advisor:")
    print("-----------------------------------------------------------------------------------------------------------------")
    for i, ally in enumerate(ally_list):
        print(f"{i}: {ally}")
    while True:
        try:
            ally_selection = int(input("Select an advisor by number: "))
            if ally_selection in ally_menu:
                selected_ally = ally_menu[ally_selection]
                break
            else:
                print("Invalid selection. Please select an advisor by number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    print(f"Selected advisor: {selected_ally}")
    print("Select an option:")
    print("1: Check for students who have not participated in their course(s) within the last 7 days and have course 0s and/ or missing assignments.")
    print("2: See all students for this advisor.")
    print("3: Select a different advisor.")
    while True:
        try:
            option = int(input("Enter option number: "))
            if option == 1 or option == 2 or option == 3:
                break
            else:
                print("Invalid option. Please enter a valid option number.")
                continue
        except ValueError:
            print("Invalid option. Please enter a valid option number.")
            continue

# If the user selects option 1 and there are students who have not participated in their course(s) within the last 7 days and have course 0s and/ or missing assignments,
# print "There are no students who have not participated or done their work for this advisor."
if option == 1:
    print("There are no students who have not participated or done their work for this advisor.")

# If the user selects option 2 and there are no students for the selected ally, print "There are no students for this advisor."
if option == 2:
    print("There are no students for this advisor.")
    
# Compare against DOD_DE_ENROLLMENT list for assigned advisor. 
# Assigned advisor should be the same as the ally for each student.

# Multiple allies listed for a student. Assign student data to correct ally. 