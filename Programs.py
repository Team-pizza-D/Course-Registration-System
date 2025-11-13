# Here we will add the courses
import sqlite3
computer_codes = {"EE-250": "Introduction to Electrical Engineering",
                  "CS-101": "Introduction to Computer Science",
                  "MATH-201": "Calculus I",
                  "PHYS-150": "Generl Phaysics",}

computer_credits = {"EE-250": 3, "CS-101": 4, "MATH-201": 4, "PHYS-150": 2}
computer_prerequests = {"EE-250": "PHYS-202", "CS-101": None, "MATH-201": None, "PHYS-150": "PHYS-100"}
def loop_dict_key(d):
    x = []
    for key in d.keys():
        x.append(key)
    return x

def loop_dict_value(d):
    y = []
    for value in d.values():
        y.append(value)
    return y
A = loop_dict_value(computer_codes)
B = loop_dict_key(computer_codes)
C = loop_dict_value(computer_credits)
D = loop_dict_value(computer_prerequests)

def add_course(x, y ,z, p):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('CREATE TABLE IF NOT EXISTS courses (course_name TEXT, course_code TEXT, credit INTEGER, prerequisites TEXT)')
    for i in range(len(x)):
        cr.execute('INSERT INTO courses (course_name, course_code, credit, prerequisites) VALUES (?, ?, ?, ?)',
               (x[i] , y[i], z[i], p[i]))
    db.commit()
    db.close()
add_course(A, B, C, D)