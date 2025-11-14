# Here we will add the courses
import sqlite3
# Shared courses :
####################################################################################################
course_codes_Y1 = ["MATH110", "PHYS110", "CHEM110", "CPIT110", "BIO110","STAT110","ELIS110","ELIS120"]
course_codes_Y2 = ["MATH206", "IE200","PHYS202", "CHEM281", "EE201", "ISLS101", "ARAB101", "IE201", "IE255", "MENG102", "MATH207", "PHYS281"]
course_codes_Y3 = ["ARAB201", "EE202", "EE250", "MATH204", "ISLS201", "EE300", "EE301", "IE202"]
course_codes_Y4 = ["EE321", "EE311", "IE256", "EE360", "EE366", "ISLS301"]
course_codes_Y5 = ["EE499", "ISLS401", "EE390"]
####################################################################################################
Y1_Credits = [3, 3, 3, 3, 3, 3, 2, 2]
Y2_Credits = [4, 2, 4, 1, 2, 2, 2, 3, 3, 3, 4, 1]
Y3_Credits = [3, 3, 4, 3, 2, 3, 3, 3]
Y4_Credits = [4, 4, 2, 4, 3, 2]
Y5_Credits = [4, 2, 3]

# Power and machine courses :
power_sh = ["EE331", "EE332", "EE302"]################################################################### Not shared with all majors
power = ["MEP261", "EE303", "EE341", "EE442", "EE441", "EE404", "EE451", "EE405", "EE453", "EE454"] 


# Computer courses :
computer_sh = ["EE331", "EE306", "EE332", "IE331"]####################################################### Not shared with all majors
computer = ["EE305", "EE364", "EE361", "EE367", "EE460", "EE462", "EE463"]


# Electronics and communication courses :
communication_sh = ["EE331", "EE306", "EE332", "IE331", "EE302", "EE312", "EE351"]####################### Not shared with all majors
communication = ["EE421", "EE423", "EE413", "EE425"]


# Biomedical courses :
biomedical_sh = ["EE306", "EE302", "EE312", "EE351"]##################################################### Not shared with all majors
biomedical = ["BIO321", "EE374", "EE372", "EE370", "EE472", "EE474", "EE471", "EE470"]

### For whose working with databases , these are temporary values(only credits and prerequisites)
### MMM & CCC & BBB are just temporary
MMM = {"EE331": 0, "EE302": 0, "EE306": 0, "EE332": 0, "IE331": 0, "EE312": 0, "EE351": 0,}
CCC = {"EE331": 0, "EE302": 0, "EE306": 0, "EE332": 0, "IE331": 0, "EE312": 0, "EE351": 0,}
BBB = {"EE331": "Principles of Automatic Control",
       "EE302": "Magnetic 1", 
       "EE306": "Electrical Engineering Technologies", 
       "EE332": "Numerical Methods in Engineering", 
       "IE331": "Probability and Engineering Statistics", 
       "EE312": "Electronics 2", 
       "EE351": "Electrical Power Systems I"}


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
# A = loop_dict_value(computer_codes)
# B = loop_dict_key(course_codes)
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
# add_course(A, B, C, D)