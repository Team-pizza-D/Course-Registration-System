# Here we will add the courses
import sqlite3
# Shared courses :
####################################################################################################
course_codes_Y1 = ["MATH110", "PHYS110", "CHEM110", "CPIT110", "BIO110","STAT110","ELIS110","ELIS120"]
course_codes_Y2 = ["MATH206", "IE200","PHYS202", "CHEM281", "EE201", "ISLS101", "ARAB101", "IE201", "IE255", "MENG102", "MATH207", "PHYS281"]
course_codes_Y3 = ["ARAB201", "EE202", "EE250", "MATH204", "ISLS201", "EE300", "EE301", "IE202"]
course_codes_Y4 = ["EE321", "EE311", "IE256", "EE360", "EE366", "ISLS301"]
course_codes_Y5 = ["EE499", "ISLS401", "EE390", "COMM101"]
All = course_codes_Y1 + course_codes_Y2 + course_codes_Y3 + course_codes_Y4 + course_codes_Y5
####################################################################################################
Y1_Credits = [3, 3, 3, 3, 3, 3, 3, 3]
Y2_Credits = [4, 2, 4, 1, 2, 2, 2, 3, 3, 3, 4, 1]
Y3_Credits = [3, 3, 4, 3, 2, 3, 3, 3]
Y4_Credits = [4, 4, 2, 4, 3, 2]
Y5_Credits = [4, 2, 3, 3]

All_Credits = Y1_Credits + Y2_Credits + Y3_Credits + Y4_Credits + Y5_Credits
PP = dict(zip(All, All_Credits))

# Power and machine courses :
power_sh = ["EE331", "EE332", "EE302", "EE351",]################################################################### Not shared with all majors
power = ["MEP261", "EE303", "EE341", "EE442", "EE441", "EE404", "EE451", "EE405", "EE453", "EE454"] 
all_power = power_sh + power

# Computer courses :
computer_sh = ["EE331", "EE306", "EE332", "IE331"]####################################################### Not shared with all majors
computer = ["EE305", "EE364", "EE361", "EE367", "EE460", "EE462", "EE463",]
all_computer = computer_sh + computer

# Electronics and communication courses :
communication_sh = ["EE331", "EE306", "EE332", "IE331", "EE302", "EE312", "EE351"]####################### Not shared with all majors
communication = ["EE421", "EE423", "EE413", "EE425"]
all_communication = communication_sh + communication

# Biomedical courses :
biomedical_sh = ["EE306", "EE302", "EE312"]##################################################### Not shared with all majors
biomedical = ["BIO321", "EE374", "EE372", "EE370", "EE472", "EE474", "EE471", "EE470"]
all_biomedical = biomedical_sh + biomedical

### For who is working with databases , these are temporary values(only credits and prerequisites)
Semi_Shared_Courses = ["EE331", "EE302", "EE306", "EE332", "IE331", "EE312", "EE351"]
Semi_Shared_C = {"EE331": 4, "EE302": 3, "EE306": 3, "EE332": 3, "IE331": 3, "EE312": 4, "EE351": 3,}
Semi_Shared_PR = {"EE331": "EE300, EE301", "EE302": "EE250", "EE306": "EE250, STAT110", "EE332": "EE201, MATH 204", "IE331": "MATH207, STAT110", "EE312": "EE311", "EE351": "EE250",}

Semi_Shared_Terms_Power         = {"EE331": 8, "EE302": 7, "EE332": 8, "EE351": 8}
Semi_Shared_Terms_Computer      = {"EE331": 9, "EE306": 6, "EE332": 8, "IE331": 6}
Semi_Shared_Terms_Communication = {"EE331": 8, "EE302": 6, "EE306": 6, "EE332": 8, "IE331": 7, "EE312": 8, "EE351": 9}
Semi_Shared_Terms_Biomedical    = {"EE302": 7, "EE306": 6, "EE312": 8}
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

Third_Year_C = {"ARAB201":3, "EE202":3, "EE250":4, "MATH204":3, "ISLS201":2, "EE300":3, "EE301":3, "IE202":2}
Third_Year_PR = {"ARAB201":"ARAB101", "EE202":"EE201", "EE250":"PHYS202", "MATH204":"MATH207", "ISLS201":"ISLS101", "EE300":"MATH207", "EE301":"EE250" and "MATH204", "IE202":"IE200" and "IE201"}
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

Fourth_Year_C = {"EE321":4, "EE311":4, "IE256":2, "EE360":4, "EE366":3, "ISLS301":2}
Fourth_Year_PR = {"EE321":"EE301", "EE311":"EE250", "IE256":"IE255", "EE360":"EE250", "EE366":"EE202, EE360", "ISLS301":"ISLS201"}
Fourth_Year_Terms = {"EE321":7, "EE311":7, "IE256":7, "EE360":7, "EE366":8, "ISLS301":8}
Fourth_Year_Courses_Names= {"EE321":"Introduction to Communications",  
                       "EE311":"Electronics 1", 
                       "IE256":"Engineering Management", 
                       "EE360":"Digital Design 1", 
                       "EE366":"Microprocessors and Microcontrollers", 
                       "ISLS301":"Islamic Culture 3"}

Fifth_Year_C = {"EE499":4, "ISLS401":2, "EE390":2, "COMM101":10} 
Fifth_Year_PR = {"EE499":"Department Approval", "ISLS401":"ISLS301", "EE390":"Department Approval", "COMM101": None}
Fifth_Year_Terms = {"EE499":9, "ISLS401":10, "COMM101":10, "EE390":11,}
Fifth_Year_Courses_Names= {"EE499":"Senior Project",
                         "ISLS401":"Islamic Culture 4", 
                         "EE390":"Summer Training",
                        "COMM101":"Communication Skills"}

All_Courses_C = {**First_Year_C, **Second_Year_C, **Third_Year_C, **Fourth_Year_C, **Fifth_Year_C}  
All_Courses_PR = {**First_Year_PR, **Second_Year_PR, **Third_Year_PR, **Fourth_Year_PR, **Fifth_Year_PR}
All_Courses_Names = Fifth_Year_Courses_Names | Fourth_Year_Courses_Names | Third_Year_Courses_Names | Second_Year_Courses_Names | First_Year_Courses_Names
All_Terms = First_Year_Terms | Second_Year_Terms | Third_Year_Terms | Fourth_Year_Terms | Fifth_Year_Terms
# Power and machine courses :
power_courses_C = {"MEP261":3, "EE303":3, "EE341":3, "EE442":3, "EE441":3, "EE404":1, "EE451":3, "EE405":1, "EE453":3, "EE454":3,} 
power_courses_PR = {"MEP261":None, "EE303":"EE311", "EE341":"EE250", "EE442":"EE311", "EE441":"EE351, EE341", "EE404":"EE441", "EE451":"EE351, EE332", "EE405":"EE451", "EE453":"EE351, EE332", "EE454":"EE351, EE341"}
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
computer_courses_C = {"EE305":3, "EE364":3, "EE361":3, "EE367":3, "EE460":4, "EE462":3, "EE463":4}
computer_courses_PR = {"EE305":"EE202, MATH204, IE202", "EE364":"EE202", "EE361":"EE360, STAT110", "EE367":"EE202, EE305", "EE460":"EE360", "EE462":"EE202, EE364", "EE463":"EE361, EE367"}
computer_terms= {"EE305":7, "EE364":8, "EE361":8, "EE367":8, "EE460":9, "EE462":10, "EE463":10}
computer_coursesName= {"EE305":"Discrete Mathematics and its Applications",
                       "EE364":"Advanced Programming",
                       "EE361":"Digital Computer Organization",
                       "EE367":"Data Structures and Algorithms",
                       "EE460":"Digital Design 2",
                       "EE462":"Computer Communication Networks",
                       "EE463":"Operating Systems"}
# Electronics and communication courses :
communication_courses_C = {"EE421":3, "EE423":3, "EE413":4, "EE425":3}
communication_courses_PR = {"EE421":"EE321, IE331", "EE423":"EE302, MATH204", "EE413":"EE312, EE321", "EE425":"EE421"}
communication_terms = {"EE421":9, "EE423":9, "EE413":10, "EE425":10}
communication_coursesName= {"EE421":"Communication Theory 1",
                            "EE423":"Magnetic 2",
                            "EE413":"Communication Circuits",
                            "EE425":"Communication Systems"}
#  Biomedical courses :
biomedical_courses_C = {"BIO321":3, "EE374":3, "EE372":3, "EE370":4, "EE472":3, "EE474":3, "EE471":3, "EE470":4}
biomedical_courses_PR = {"BIO321":None, "EE374":"BIO321", "EE372":"BIO321", "EE370":"EE306, BIO321", "EE472":"EE370, EE303", "EE474":"EE370", "EE471":"EE370, EE372, EE312", "EE470":"EE301, EE370"}
biomedical_terms = {"BIO321":6, "EE374":7, "EE372":7, "EE370":8, "EE472":10, "EE474":10, "EE471":9, "EE470":9}
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


def computer_adding(x1, y1, z1, p1, m1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS Computer')
    cr.execute('CREATE TABLE IF NOT EXISTS Computer (course_code TEXT, course_name TEXT, credit INTEGER, prerequisites TEXT, terms INTEGER)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Computer (course_code, course_name, credit, prerequisites, terms) VALUES (?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], m1[i]))
    db.commit()
    db.close()

def power_adding(x1, y1, z1, p1, m1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS Power')
    cr.execute('CREATE TABLE IF NOT EXISTS Power (course_code TEXT, course_name TEXT, credit INTEGER, prerequisites TEXT, terms INTEGER)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Power (course_code, course_name, credit, prerequisites, terms) VALUES (?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], m1[i]))
    db.commit()
    db.close()

def communication_adding(x1, y1, z1, p1, m1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS Communication')
    cr.execute('CREATE TABLE IF NOT EXISTS Communication (course_code TEXT, course_name TEXT, credit INTEGER, prerequisites TEXT, terms INTEGER)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Communication (course_code, course_name, credit, prerequisites, terms) VALUES (?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], m1[i]))
    db.commit()
    db.close()

def biomedical_adding(x1, y1, z1, p1, m1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS Biomedical')
    cr.execute('CREATE TABLE IF NOT EXISTS Biomedical (course_code TEXT, course_name TEXT, credit INTEGER, prerequisites TEXT, terms INTEGER)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Biomedical (course_code, course_name, credit, prerequisites, terms) VALUES (?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], m1[i]))
    db.commit()
    db.close()


def build_course_dict(codes, d):
    return [d[code] for code in codes]


power_codes = list(set(All + all_power))
power_names = All_Courses_Names | Semi_Shared_Courses_Names | power_coursesName
power_credits = PP | power_courses_C | Semi_Shared_C
power_prerequisites = All_Courses_PR | power_courses_PR | Semi_Shared_PR
power_terms = All_Terms | power_terms | Semi_Shared_Terms_Power
for key in power_terms:
    if key =="EE366":
        power_terms[key]=9
        break
power_adding((power_codes), (build_course_dict(power_codes, power_names)), (build_course_dict(power_codes, power_credits)), (build_course_dict(power_codes, power_prerequisites)), build_course_dict(power_codes, power_terms))


computer_codes = list(set(All + all_computer))
computer_names = All_Courses_Names | Semi_Shared_Courses_Names | computer_coursesName
computer_credits = PP | computer_courses_C | Semi_Shared_C
computer_prerequisites = All_Courses_PR | computer_courses_PR | Semi_Shared_PR
computer_terms = All_Terms | computer_terms | Semi_Shared_Terms_Computer
computer_adding((computer_codes), (build_course_dict(computer_codes, computer_names)), (build_course_dict(computer_codes, computer_credits)), (build_course_dict(computer_codes, computer_prerequisites)), build_course_dict(computer_codes, (computer_terms)))


communication_codes = list(set(All + all_communication))
communication_names = All_Courses_Names | Semi_Shared_Courses_Names | communication_coursesName
communication_credits = PP | communication_courses_C | Semi_Shared_C
communication_prerequisites = All_Courses_PR | communication_courses_PR | Semi_Shared_PR
communication_terms = All_Terms | communication_terms | Semi_Shared_Terms_Communication
communication_adding((communication_codes), (build_course_dict(communication_codes, communication_names)), (build_course_dict(communication_codes, communication_credits)), (build_course_dict(communication_codes, communication_prerequisites)), build_course_dict(communication_codes, communication_terms))


biomedical_codes = list(set(All + all_biomedical))
biomedical_names = All_Courses_Names | Semi_Shared_Courses_Names | biomedical_coursesName
biomedical_credits = PP | biomedical_courses_C | Semi_Shared_C
biomedical_prerequisites = All_Courses_PR | biomedical_courses_PR | Semi_Shared_PR
biomedical_terms = All_Terms | biomedical_terms | Semi_Shared_Terms_Biomedical
for key in biomedical_terms:
    if key == "IE256":
        biomedical_terms[key] = 8
    if key == "EE321":
        biomedical_terms[key] = 8
    if key == "ISLS301":
        biomedical_terms[key] = 9
biomedical_adding((biomedical_codes), (build_course_dict(biomedical_codes, biomedical_names)), (build_course_dict(biomedical_codes, biomedical_credits)), (build_course_dict(biomedical_codes, biomedical_prerequisites)), build_course_dict(biomedical_codes, biomedical_terms))


######################################
# All courses:
def all_courses(x1, y1, z1, p1, m1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS courses')
    cr.execute('CREATE TABLE IF NOT EXISTS Courses (course_name TEXT, course_code TEXT, credit INTEGER, prerequisites TEXT, terms INTEGER)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Courses (course_name, course_code, credit, prerequisites, terms) VALUES (?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], m1[i]))
    db.commit()
    db.close()



All_Courses = All + Semi_Shared_Courses + power + computer + communication + biomedical
All_Names = All_Courses_Names | Semi_Shared_Courses_Names | power_coursesName | computer_coursesName | communication_coursesName | biomedical_coursesName
All_Credits = PP | Semi_Shared_C | power_courses_C | computer_courses_C | communication_courses_C | biomedical_courses_C
All_Prerequisites = All_Courses_PR | Semi_Shared_PR | power_courses_PR | computer_courses_PR | communication_courses_PR | biomedical_courses_PR

B = {}

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
count = 0

for course in All_Courses:
    first = letters[count // 26]       
    second = letters[count % 26]        
    B[course] = first + second
    count += 1

db = sqlite3.connect('courses.db')
cr = db.cursor()
cr.execute('DROP TABLE IF EXISTS Courses')
cr.execute('CREATE TABLE IF NOT EXISTS Courses (course_code TEXT, course_name TEXT, section TEXT)')
for i in range (len(All_Courses)):
    cr.execute('INSERT INTO Courses (course_code, course_name, section) VALUES (?, ?, ?)',
               (All_Courses[i] , All_Names[All_Courses[i]], B[All_Courses[i]]))
db.commit()
db.close()