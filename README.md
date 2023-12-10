#Online-Learning-Platform
Project Description: This project is a system developed in Python using the Flask framework as the core component. It includes a login system ("/login") where users cannot self-register. Users are categorized into three different roles: Administrator, Teacher, and Student. Once logged in, users are redirected to the home page ("/home").

Features
Administrator

Access to the admin tool ("/adminTool") through the "adminTool" button on the home page.
Administrator-exclusive functionalities:
Individual account registration.
Batch registration using an XLSX file.
User search by ID for modification.
Course creation and management.
Student

Access to the home page ("/home").
"My Course" button on the home page redirects to the "/course" page.
View enrolled courses with individual pages.
Course pages include sections for announcements, resources, and assignments.
"Academic Records" button on the home page redirects to the "/academicRecords" page.
View academic records such as CGPA, SGPA, and GPA.
Teacher

Similar functionalities to students.
Additional privileges:
Add or delete announcements, resources, and assignments.
Publish grades for students.
Personal Information

"Personal Information" button on the home page redirects to the "/personal-info" page.
Displays account information for the logged-in user.
Installation
Clone the repository.
Install the required dependencies using pip install -r requirements.txt.
Run the application using python app.py.
Access the system through the provided URL.
Usage
Open a web browser and navigate to the specified URL.
Click on the "Login" button to access the login page.
Enter the credentials for the respective user role (Administrator, Teacher, or Student).
After successful login, users will be redirected to the home page ("/home").
From the home page, users can navigate to different sections of the system based on their role and access the corresponding functionalities.
Contributing
Fork the repository.
Create a new branch for your feature or bug fix.
Make the necessary changes and commit them.
Push your branch to your forked repository.
Submit a pull request to the main repository.
License
This project is licensed under the MIT License.

Acknowledgements
We would like to thank the contributors and open-source community for their valuable contributions and support.

Please feel free to reach out to us for any further assistance or inquiries.
