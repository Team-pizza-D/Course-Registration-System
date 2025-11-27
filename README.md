# Course-Registration-System

## Project Overview
The ECE Department Course Registration System is a software solution designed to streamline  the course registration process for students within the ECE department.

This project contains 3 parts, which are :

1. **DataBase**
2. **Classes**
3. **The GUI**

Each part is created in a separate Python file and connected through the main file (`main.py`). 

---

## Group Members and Contributions
- **Faisal Ahmed Alidiny** — Creating the DataBase and README documentation  
- **Azzam Wael Alsayed** — The GUI  
- **Azad Ayman Felemban** — Cresting the Classes 
- **Ammar Ehab Jeddawi** — The GUI    
- **Abdulkreem Mohammed Alghamdi** — Cresting the Classes  
- **Abdulaziz Qasim Alqahtani** — Creating the DataBase and connecting it to Classes

---
## How to Run the Program
1. Make sure **Python 3** is installed on your computer.  
2. Place all project files in the same folder:
```css
main.py
classes.py
GUI.py
users.py
programs.py
README.md
```
3. Open a terminal or command prompt in that folder.  
4. Run the program by typing:
```bash
python main.py()
```
Follow the on-screen menu enter University ID and password then press Login.


---

## File Descriptions
**main.py**	Entry point of the program. Displays the main menu and connects all parts of the project.

**Programs.py**	 It contains all the data about the transcripts such as, courses, prerequists, credits, and terms.

**GUI.py**	It contains all code for the GUI interfaces.

**Users.py**	It contains all code for the users and connecting it to Classes.

**Classes.py**	It has all the classes the control the whole project. It connects classes, DataBase, and the GUI to each other.

**README.md**	Documentation file describing the project, team members,and usage instructions.

---


## Example Program Output
```bash
Welcome to Multi-Mode Calculator
1. Standard Mode
2. Programmer Mode
3. Scientific Mode
4. Converter Mode
5. Exit
Enter your choice: 1
```
```bash
Standard Mode
#	Input	Expected Output
1	5 + 3	8
2	10 / 0	Error: Cannot divide by zero
3	sqrt(9)	3
4	2 ** 4	16
5	15 % 4	3
```
```bash
Programmer Mode
#	Input	Expected Output
1	Decimal 10 → Binary	1010
2	Binary 1111 → Decimal	15
3	5 & 3	1
4	6 ^ 2	4
5	Invalid binary (e.g. "2G")	Error: Invalid base or input format
```
```bash
Scientific Mode
#	Input	Expected Output
1	sin(90°)	1.0
2	cos(0°)	1.0
3	log(10)	1.0
4	ln(e)	1.0
5	factorial(5)	120
```
```bash
Converter Mode
#	Input	Expected Output
1	1 m → ft	3.281 ft
2	100 cm → in	39.37 in
3	0 °C → °F	32 °F
4	10 kg → lb	22.046 lb
5	Invalid unit (e.g. "meterz")	Error: Unknown unit
```

---
## Challenges Faced

### 1-DataBase

Learn everything from the beginning

Understand what is the DataBase and how to creat it

Learn how to create multiple table and columns

Learn how to insert data in the tables

Learn how to connect the tables with the Classes and manage it


### 2-Classes

Understand what is the Classes and how to creat it

Learn how to connect the Classes with the DataBase and the GUI and manage it


### 3-The GUI

Understand what is the GUI and how to creat it
Learn how to connect the GUI with the Classes and manage it




## Conclusion
This project demonstrates teamwork, modular programming, and data validation in Python.
Each part was developed by two team members to ensure the quality of the work.
The result is a user-friendly Course-Registration-System that is organized, functional, and easy to extend in the future.
This project has improved our teamwork skills. 