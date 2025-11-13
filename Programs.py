# Here we will add the courses
import sqlite3
course_codes_Y1 = ["MATH110", "PHYS110", "CHEM110", "CPIT110", "BIO110","STAT110","ELIS110","ELIS120"]
course_codes_Y2 = ["MATH206", "IE200","PHYS202", "CHEM281", "EE201", "ISLS101", "ARAB101", "IE201", "IE255", "MENG102", "MATH207", "PHYS281"]

course_credits = {}
course_prerequests = {}
course_sections = {}
course_section_codes = {}
course_instructors = {}
computer_capacitys = {}



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
B = loop_dict_key(course_codes)
C = loop_dict_value(course_credits)
D = loop_dict_value(course_prerequests)

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