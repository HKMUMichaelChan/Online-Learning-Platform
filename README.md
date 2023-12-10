
# Online Learning Platform

## Project Description
This project is a Student Management System developed in Python using the Flask framework as the core component.


## Installation

1. Clone the repository.
2. Install the required dependencies using pip install -r requirements.txt.

```bash
  git clone https://github.com/HKMUMichaelChan/Online-Learning-Platform
  pip install -r requirements.txt
  cd Online-Learning-Platform
  python Server.py
```
4. Access the system through the port 5000 (127.0.0.1:5000) 

## Usage
### Initialization

![initializeIMG](https://i.imgur.com/8QWIL52.png)

When opening the server for the first time, you need to create an Admin account first.

### Authorization system
Everyone must be logged in to use the system.

![LoginIMG](https://i.imgur.com/3uFuGCO.png)

There are 3 type of account:
- Administrator (ID Start with 3)
- Teacher (ID Start with 2)
- Student (ID Start with 1)


When logging in, the system will store the authorized TOKEN in the session.

It will be valid for 30 minutes. Each user's valid activity will reset the validity period to 30 minutes.
![te](https://i.imgur.com/f7jjAGh.png)
## Main Page - HOME
The main interface of the system. 
![HOME](https://i.imgur.com/vkZ9shZ.png)
Contains 4 functions:
- Personal Info
- My Course
- Academic records
- Administrator Tools (Administrator Only)

### Personal Info 
Ability to view Basic Information
![PI](https://i.imgur.com/EoPuBz8.png)
In the editing function, only administrators can make comprehensive changes to the information.

For other accounts, only some information can be changed

Of course, the administrator can help them change it
![admin](https://i.imgur.com/5R98y3q.png)
![teacher](https://i.imgur.com/s0ZvmbN.png)

### My Course
For clicking the "My Course" button in Home Page

You can see the course enrolling/teaching are shown here
![courseIndex](https://i.imgur.com/DqDZl0Y.png)

Enter the course page by clicking one of the course button.

The Student can only see the course content here.

Only Teacher can post or remove the content and having the Scoe Management for post the Academic Record for Student. 

![coursePage](https://i.imgur.com/8lGYHyV.png)

![sm](https://i.imgur.com/44g2Kbb.png)


### Academic records
For clicking the "Academic records" button in Home Page

You can see the account Academic Records here
![AR](https://i.imgur.com/4J57sY3.png)

### Administrator Tools
For clicking the "Administrator Tools" button in Home Page

You can see the Tools GUI show here

![AT](https://i.imgur.com/nV0NGxq.png)

You can use the form here to help registration

![regForm](https://i.imgur.com/R5J9CKJ.png)

You can Batch registration with xlsx in following format

![rformat](https://i.imgur.com/KhsgNnu.png)

You can build course by using following form.

![bcForm](https://i.imgur.com/nyl8sh3.png)
The xlsx format for adding students to a course in a semester:

![crxlsx](https://i.imgur.com/xxAzqxQ.png)
## Authors

Name | Student ID
- CHAN Man Kit | 13204789
- Tsang Hok Ki | 13052175 
- Chan Hoi Yuet | 13158953 
- Wong Chi Shing | 13158326 
- Lau Yiu Hung 13190511

