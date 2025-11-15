# Here we will add the courses
import sqlite3
# Shared courses :
####################################################################################################
course_codes_Y1 = ["MATH110", "PHYS110", "CHEM110", "CPIT110", "BIO110","STAT110","ELIS110","ELIS120"]
course_codes_Y2 = ["MATH206", "IE200","PHYS202", "CHEM281", "EE201", "ISLS101", "ARAB101", "IE201", "IE255", "MENG102", "MATH207", "PHYS281"]
course_codes_Y3 = ["ARAB201", "EE202", "EE250", "MATH204", "ISLS201", "EE300", "EE301", "IE202"]
course_codes_Y4 = ["EE321", "EE311", "IE256", "EE360", "EE366", "ISLS301"]
course_codes_Y5 = ["EE499", "ISLS401", "EE390"]
All = course_codes_Y1 + course_codes_Y2 + course_codes_Y3 + course_codes_Y4 + course_codes_Y5
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

### For who is working with databases , these are temporary values(only credits and prerequisites)
Semi_Shared_C = {"EE331": 0, "EE302": 0, "EE306": 0, "EE332": 0, "IE331": 0, "EE312": 0, "EE351": 0,}
Semi_Shared_PR = {"EE331": 0, "EE302": 0, "EE306": 0, "EE332": 0, "IE331": 0, "EE312": 0, "EE351": 0,}
Semi_Shared_Courses_Names = {"EE331": "Principles of Automatic Control",
       "EE302": "Magnetic 1", 
       "EE306": "Electrical Engineering Technologies", 
       "EE332": "Numerical Methods in Engineering", 
       "IE331": "Probability and Engineering Statistics", 
       "EE312": "Electronics 2", 
       "EE351": "Electrical Power Systems I"}
###all the shared courses codes
# C = credits
# PR = prerequisites
First_Year_C = {"MATH110": 3, "PHYS110": 3, "CHEM110": 3, "CPIT110": 3, "BIO110": 3,"STAT110": 3,"ELIS110": 3,"ELIS120": 3}
First_Year_PR = {"MATH110": None, "PHYS110": None, "CHEM110": None, "CPIT110": None, "BIO110": None,"STAT110": None,"ELIS110": None,"ELIS120": None}
First_Year_Terms = {"MATH110": 1, "PHYS110": 2, "CHEM110": 1, "CPIT110": 2, "BIO110": 2,"STAT110": 1,"ELIS110": 1,"ELIS120": 2}
First_Year_Courses_Names= {"MATH110":"General Mathematics 1",
                        "PHYS110":"General Physics 1",
                        "CHEM110":" General Chemistry 1",
                        "CPIT110":"Problem Solving & Programming",
                        "BIO110":"General Biology 1",
                        "STAT110":"General Statistics 1",
                        "ELIS110":"English Language-Science 1",
                        "ELIS120":"English Language-Science 2"}

Second_Year_C = {"MATH206": 4, "IE200": 2,"PHYS202": 4, "CHEM281": 1, "EE201": 2, "ISLS101": 2,
                "ARAB101": 3, "IE201": 3, "IE255": 3, "MENG102": 3, "MATH207": 4, "PHYS281": 1}
Second_Year_PR = {"MATH206": "MATH110", "IE200": None,"PHYS202": "MATH110" and "Phys110", "CHEM281": "CHEM110", "EE201": None, "ISLS101": None,
                "ARAB101": None, "IE201": None, "IE255": None, "MENG102": None, "MATH207": "Math206", "PHYS281": None}
Second_Year_Terms = {"MATH206": 3, "IE200": 3,"PHYS202": 3, "CHEM281": 3, "EE201": 3, "ISLS101": 3,
                "ARAB101": 4, "IE201": 4, "IE255": 4, "MENG102": 4, "MATH207": 4, "PHYS281": 4}
Second_Year_Courses_Names= {"MATH206":"Calculus 2 for Engineers",
                        "IE200":"Technical Communication Skills",
                        "PHYS202":"General Physics 2",
                        "CHEM281":"General Chemistry Lab",
                        "EE201":"Struvtured Computer Programming",
                        "ISLS101":"Islamic Culture 1",
                        "ARAB101":"Arabic Language 1",
                        "IE201":"Introduction to Engineering Design 1",
                        "IE255":"Engineering Economy",
                        "MENG102":"Engineering Graphics",
                        "MATH207":"Calculus 3 for Engineers",
                        "PHYS281":"General Physics Lab"}

Third_Year_C = {"ARAB201":0, "EE202":0, "EE250":0, "MATH204":0, "ISLS201":0, "EE300":0, "EE301":0, "IE202":0}
Third_Year_PR = {"ARAB201":0, "EE202":0, "EE250":0, "MATH204":0, "ISLS201":0, "EE300":0, "EE301":0, "IE202":0}
Third_Year_Terms = {"ARAB201":5, "EE202":5, "EE250":5, "MATH204":5, "ISLS201":5,
                    "EE300":6, "EE301":6, "IE202":6}
Third_Year_Courses_Names= {"ARAB201":"Arabic Language 2",
                        "EE202":"Object-Oriented Computer Programming",
                        "EE250":"Basic Electrical Circuits",
                        "MATH204":"Differential Equations 1",
                        "ISLS201":"Islamic Culture 2",
                        "EE300":"Analytical Methods in Engineering",
                        "EE301":"Electrical Circuits and Systems",
                        "IE202":"Introduction to Engineering Design 2"}

Fourth_Year_C = {"EE321":0, "EE311":0, "IE256":0, "EE360":0, "EE366":0, "ISLS301":0}
Fourth_Year_PR = {"EE321":0, "EE311":0, "IE256":0, "EE360":0, "EE366":0, "ISLS301":0}
Fourth_Year_Terms = {"EE321":1, "EE311":1, "IE256":1, "EE360":2, "EE366":2, "ISLS301":2}
Fourth_Year_Courses_Names= {"EE321":"Introduction to Communications",  
                       "EE311":"Electronics 1", 
                       "IE256":"Engineering Management", 
                       "EE360":"Digital Design 1", 
                       "EE366":"Microprocessors and Microcontrollers", 
                       "ISLS301":"Islamic Culture 3"}

Fifth_Year_C = {"EE499":0, "ISLS401":0, "EE390":0} 
Fifth_Year_PR = {"EE499":0, "ISLS401":0, "EE390":0}
Fifth_Year_Terms = {"EE499":9, "ISLS401":10, "EE390":3}
Fifth_Year_Courses_Names= {"EE499":"Senior Project",
                         "ISLS401":"Islamic Culture 4", 
                         "EE390":"Summer Training"}

All_Courses_C = {**First_Year_C, **Second_Year_C, **Third_Year_C, **Fourth_Year_C, **Fifth_Year_C}  
All_Courses_PR = {**First_Year_PR, **Second_Year_PR, **Third_Year_PR, **Fourth_Year_PR, **Fifth_Year_PR}
All_Courses_Names = {**First_Year_Courses_Names, **Second_Year_Courses_Names, **Third_Year_Courses_Names, **Fourth_Year_Courses_Names, **Fifth_Year_Courses_Names}
# Power and machine courses :
power_courses = {"MEP261":0, "EE303":0, "EE341":0, "EE442":0, "EE441":0, "EE404":0, "EE451":0, "EE405":0, "EE453":0, "EE454":0} 
power_courses2 = {"MEP261":0, "EE303":0, "EE341":0, "EE442":0, "EE441":0, "EE404":0, "EE451":0, "EE405":0, "EE453":0, "EE454":0}
power_terms= {"MEP261":6, "EE303":7, "EE341":8, "EE442":9, "EE441":9, "EE404":9, "EE451":9, "EE405":10, "EE453":10, "EE454":10}
power_coursesName= {"MEP261":"Thermodynamics I",
                    "EE303":"Electrical Measurement and Instrumentation ",
                    "EE341":"Electromechanical Energy Conversion I",
                    "EE442":"Power Electronics I",
                    "EE441":"Electromechanical Energy Conversion II",
                    "EE404":"Machines Lab",
                    "EE451":"Electrical Power Systems II",
                    "EE405":"Power System Lab",
                    "EE453":"Power Transmission and Distribution",
                    "EE454":"Switchgear and Protection of Power Systems I"}
#  Computer courses :
computer_courses = {"EE305":0, "EE364":0, "EE361":0, "EE367":0, "EE460":0, "EE462":0, "EE463":0}
computer_courses2 = {"EE305":0, "EE364":0, "EE361":0, "EE367":0, "EE460":0, "EE462":0, "EE463":0}
computer_courses_terms= {"EE305":7, "EE364":8, "EE361":8, "EE367":8, "EE460":9, "EE462":10, "EE463":10}
computer_coursesName= {"EE305":"Discrete Mathematics and its Applications",
                       "EE364":"Advanced Programming",
                       "EE361":"Digital Computer Organization",
                       "EE367":"Data Structures and Algorithms",
                       "EE460":"Digital Design 2",
                       "EE462":"Computer Communication Networks",
                       "EE463":"Operating Systems"}
# Electronics and communication courses :
communication_courses = {"EE421":0, "EE423":0, "EE413":0, "EE425":0}
communication_courses2 = {"EE421":0, "EE423":0, "EE413":0, "EE425":0}
communication_coursesName= {"EE421":"Communication Theory 1",
                            "EE423":"Magnetic 2",
                            "EE413":"Communication Circuits",
                            "EE425":"Communication Systems"}
#  Biomedical courses :
biomedical_courses = {"BIO321":0, "EE374":0, "EE372":0, "EE370":0, "EE472":0, "EE474":0, "EE471":0, "EE470":0}
biomedical_courses2 = {"BIO321":0, "EE374":0, "EE372":0, "EE370":0, "EE472":0, "EE474":0, "EE471":0, "EE470":0}
biomedical_coursesName= {"BIO321":"Biomedical Engineering",
                        "EE374":"Experimental &Data Analysis",
                        "EE372":"Physiology",
                        "EE370":"Biomedical Primer",
                        "EE472":"Imaging Systems",
                        "EE474":"Safety, Reliability & Maintenance",
                        "EE471":"Instrumentation",
                        "EE470":"Signals & Systems"}
                       




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


def computer(x1, y1, z1, p1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute("DROP TABLE computer")
    cr.execute('CREATE TABLE IF NOT EXISTS Computer (course_name TEXT, course_code TEXT, credit INTEGER, prerequisites TEXT)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Computer (course_name, course_code, credit, prerequisites) VALUES (?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i]))
    db.commit()
    db.close()

def power(x1, y1, z1, p1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('CREATE TABLE IF NOT EXISTS Power (course_name TEXT, course_code TEXT, credit INTEGER, prerequisites TEXT)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO IF NOT EXISTS Power (course_name, course_code, credit, prerequisites) VALUES (?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i]))
    db.commit()
    db.close()

def communication(x1, y1, z1, p1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('CREATE TABLE IF NOT EXISTS Communication (course_name TEXT, course_code TEXT, credit INTEGER, prerequisites TEXT)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO IF NOT EXISTS Communication (course_name, course_code, credit, prerequisites) VALUES (?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i]))
    db.commit()
    db.close()

def biomedical(x1, y1, z1, p1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('CREATE TABLE IF NOT EXISTS Biomedical (course_name TEXT, course_code TEXT, credit INTEGER, prerequisites TEXT)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO IF NOT EXISTS Biomedical (course_name, course_code, credit, prerequisites) VALUES (?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i]))
    db.commit()
    db.close()

