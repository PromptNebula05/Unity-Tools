This program needs to check the data from the DoD Report csv file and compare it against student account information from the
DoD Enrollment Reg List. It will match student accounts based on the "student_sis_id" on the DoD Report to the "Canvas SIS User ID"
from the DoD Enrollment Reg List (these should be the same account number). It will then check the each student's "Assigned Advisor: Full Name"
and assign that as the student's "advisor". From there, the program will sort the DoD Report csv file by ally (column 8) and check for 
students who have not participated in their course(s) within the last 7 days and have course missing assignments and course zero assignments. 
The program will then print the student's name (column 1), student's Unity ID (column 2 of DoD Enrollment Reg List) the course name (column 11),
Unity email (column 4), and the course lda (column 15). This will be presented in a table format.

The program will print out a menu of options for the user to select. The first menu will be to select an advisor. If the ally for the student is blank
and the Assigned Advisor is "To Be Assigned", then the student's advisor will be stored as "Incoming Team". If the student has multiple allies, the Assigned
Advisor from the Reg List will be that student's advisor. Otherwise, the Assigned Advisor will be stored as the student's advisor. 

The menu for each advisor will print 3 options. The first, to check for students who have not participated in their course(s) with the past 7 days
and have course 0s (column 14) and/or missing assignments (column 13). The program will then print the student's name (column 1), Unity ID (column 2 of Reg List),
the course name (column 11), Unity email (column 4), personal email (column 17 of Reg List), and the course lda (column 15).
The second option will be to see all students for that particular advisor. The program will then print the student's name, Unity ID, the course name, Unity email, personal email and the date of the last activity (LDA) for the course. The third option is to list all student whose ally did not match their Assigned Advisor.
The program will then print the student's name, Unity ID, the course name, Unity email, and their personal email.