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
###all the shared courses codes
secondYear_courses = {"ARAB201":0, "EE202":0, "EE250":0, "MATH204":0, "ISLS201":0, "EE300":0, "EE301":0, "IE202":0}
secondYear_courses2 = {"ARAB201":0, "EE202":0, "EE250":0, "MATH204":0, "ISLS201":0, "EE300":0, "EE301":0, "IE202":0}
secondyear_coursesName= {"ARAB201":"Arabic Language 2",
                        "EE202":"Object-Oriented Computer Programming",
                        "EE250":"Basic Electrical Circuits",
                        "MATH204":"Differential Equations 1",
                        "ISLS201":"Islamic Culture 2",
                        "EE300":"Analytical Methods in Engineering",
                        "EE301":"Electrical Circuits and Systems",
                        "IE202":"Introduction to Engineering Design 2"}

thirdYear_courses = {"EE321":0, "EE311":0, "IE256":0, "EE360":0, "EE366":0, "ISLS301":0}
thirdYear_courses2 = {"EE321":0, "EE311":0, "IE256":0, "EE360":0, "EE366":0, "ISLS301":0}
thirdyear_coursesName= {"EE321":"Introduction to Communications",  
                       "EE311":"Electronics 1", 
                       "IE256":"Engineering Management", 
                       "EE360":"Digital Design 1", 
                       "EE366":"Microprocessors and Microcontrollers", 
                       "ISLS301":"Islamic Culture 3"}

fourthYear_courses = {"EE499":0, "ISLS401":0, "EE390":0}
fourthYear_courses2 = {"EE499":0, "ISLS401":0, "EE390":0}
fourthyear_coursesName= {"EE499":"Senior Project",
                         "ISLS401":"Islamic Culture 4", 
                         "EE390":"Summer Training"}
# Power and machine courses :
power_courses = {"MEP261":0, "EE303":0, "EE341":0, "EE442":0, "EE441":0, "EE404":0, "EE451":0, "EE405":0, "EE453":0, "EE454":0} 
power_courses2 = {"MEP261":0, "EE303":0, "EE341":0, "EE442":0, "EE441":0, "EE404":0, "EE451":0, "EE405":0, "EE453":0, "EE454":0}
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