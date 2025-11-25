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
Semi_Shared_Power_CoursesClasses = {"EE331":"SAA","EE302":"SAB","EE332":"SAD","EE351":"SAG"}
Semi_Shared_Power_CouresCapacity = {"EE331":30,"EE302":30,"EE332":30,"EE351":30}
Semi_Shared_Power_CouresTimes = {"EE331":" ThuDay , 9-9:50","EE302":" WedDay , 10-10:50","EE332":" MonDay , 11-11:50","EE351":" TueDay , 9-9:50"}


Semi_Shared_Computer_CoursesClasses = {"EE331":"CAA","EE306":"CAB","EE332":"CAD","IE331":"CAE"}
Semi_Shared_Computer_CoursesCapacity = {"EE331":30,"EE306":30,"EE332":30,"IE331":30}
Semi_Shared_Computer_CoursesTimes = {"EE331":" ThuDay , 11-11:50","EE306":" WedDay , 9-9:50","EE332":" MonDay , 10-10:50","IE331":" TueDay , 11-11:50"}



Semi_Shared_Communication_CoursesClasses = {"EE331":"COAA","EE302":"COAB","EE306":"COAC","EE332":"COAD","IE331":"COAE","EE312":"COAF","EE351":"COAG"}
Semi_Shared_Communication_CoursesCapacity = {"EE331":30,"EE302":30,"EE306":30,"EE332":30,"IE331":30,"EE312":30,"EE351":30}
Semi_Shared_Communication_CoursesTimes = {"EE331":" ThuDay , 10-10:50","EE302":" WedDay , 9-9:50","EE306":" MonDay , 11-11:50","EE332":" TueDay , 10-10:50","IE331":" SunDay , 9-9:50","EE312":" MonDay , 9-9:50","EE351":" TueDay , 11-11:50"}



Semi_Shared_Biomedical_CoursesClasses = {"EE306":"BAA","EE302":"BAB","EE312":"BAC"}
Semi_Shared_Biomedical_CoursesCapacity = {"EE306":30,"EE302":30,"EE312":30}
Semi_Shared_Biomedical_CoursesTimes = {"EE306":" WedDay , 9-9:50","EE302":" MonDay , 11-11:50","EE312":" TueDay , 10-10:50"}



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
First_Year_sections = {"MATH110":"1A","PHYS110":"1B","CHEM110":"1C","CPIT110":"1D","BIO110":"1E","STAT110":"1F","ELIS110":"1G","ELIS120":"1H"}
First_Year_capacity = {"MATH110":30,"PHYS110":30,"CHEM110":30,"CPIT110":30,"BIO110":30,"STAT110":30,"ELIS110":30,"ELIS120":30}
First_Year_Times = {"MATH110":" SunDay , 9-9:50","PHYS110":"MonDay , 11-11:50","CHEM110":"TueDay , 10-10:50","CPIT110":"WedDay , 9-9:50","BIO110":"ThuDay , 11-11:50","STAT110":"SunDay , 10-10:50","ELIS110":"MonDay , 9-9:50","ELIS120":"TueDay , 11-11:50"}

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
Second_Year_sections = {"MATH206":"2A","IE200":"2B","PHYS202":"2C","CHEM281":"2D","EE201":"2E","ISLS101":"2F",
                "ARAB101":"2G","IE201":"2H","IE255":"2I","MENG102":"2J","MATH207":"2K","PHYS281":"2L"}
Second_Year_capacity = {"MATH206":30,"IE200":30,"PHYS202":30,"CHEM281":30,"EE201":30,"ISLS101":30,
                "ARAB101":30,"IE201":30,"IE255":30,"MENG102":30,"MATH207":30,"PHYS281":30}

Second_Year_Times = {"MATH206":" SunDay , 11-11:50","IE200":"MonDay , 10-10:50","PHYS202":"TueDay , 11-11:50","CHEM281":"WedDay , 10-10:50","EE201":"ThuDay , 9-9:50","ISLS101":"SunDay , 9-9:50",
                "ARAB101":"MonDay , 11-11:50","IE201":"TueDay , 9-9:50","IE255":"WedDay , 11-11:50","MENG102":"ThuDay , 10-10:50","MATH207":"SunDay , 10-10:50","PHYS281":"MonDay , 9-9:50"}


Third_Year_C = {"ARAB201":3, "EE202":3, "EE250":4, "MATH204":3, "ISLS201":2, "EE300":3, "EE301":3, "IE202":2}
Third_Year_PR = {"ARAB201":"ARAB101", "EE202":"EE201", "EE250":"PHYS202", "MATH204":"MATH207", "ISLS201":"ISLS101", "EE300":"MATH207", "EE301":"EE250,MATH204", "IE202":"IE200 , IE201"}
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
Third_Year_sections = {"ARAB201":"3A","EE202":"3B","EE250":"3C","MATH204":"3D","ISLS201":"3E",
                "EE300":"3F","EE301":"3G","IE202":"3H"}
Third_Year_capacity = {"ARAB201":30,"EE202":30,"EE250":30,"MATH204":30,"ISLS201":30,
                "EE300":30,"EE301":30,"IE202":30}

Third_Year_Times = {"ARAB201":" SunDay , 10-10:50","EE202":"MonDay , 9-9:50","EE250":"TueDay , 10-10:50","MATH204":"WedDay , 11-11:50","ISLS201":"ThuDay , 9-9:50",
                "EE300":"SunDay , 9-9:50","EE301":"MonDay , 11-11:50","IE202":"TueDay , 9-9:50"}


Fourth_Year_C = {"EE321":4, "EE311":4, "IE256":2, "EE360":4, "EE366":3, "ISLS301":2}
Fourth_Year_PR = {"EE321":"EE301", "EE311":"EE250", "IE256":"IE255", "EE360":"EE250", "EE366":"EE202, EE360", "ISLS301":"ISLS201"}
Fourth_Year_Terms = {"EE321":7, "EE311":7, "IE256":7, "EE360":7, "EE366":8, "ISLS301":8}
Fourth_Year_Courses_Names= {"EE321":"Introduction to Communications",  
                       "EE311":"Electronics 1", 
                       "IE256":"Engineering Management", 
                       "EE360":"Digital Design 1", 
                       "EE366":"Microprocessors and Microcontrollers", 
                       "ISLS301":"Islamic Culture 3"}
Fourth_Year_sections = {"EE321":"4A","EE311":"4B","IE256":"4C","EE360":"4D","EE366":"4E","ISLS301":"4F"}
Fourth_Year_capacity = {"EE321":30,"EE311":30,"IE256":30,"EE360":30,"EE366":30,"ISLS301":30}

Fourth_Year_Times = {"EE321":" SunDay , 9-9:50","EE311":"MonDay , 10-10:50","IE256":"TueDay , 11-11:50","EE360":"WedDay , 9-9:50","EE366":"ThuDay , 11-11:50","ISLS301":"SunDay , 10-10:50"}


Fifth_Year_C = {"EE499":4, "ISLS401":2, "EE390":2, "COMM101":10} 
Fifth_Year_PR = {"EE499":"Department Approval", "ISLS401":"ISLS301", "EE390":"Department Approval", "COMM101": None}
Fifth_Year_Terms = {"EE499":9, "ISLS401":10, "COMM101":10, "EE390":11,}
Fifth_Year_Courses_Names= {"EE499":"Senior Project",
                         "ISLS401":"Islamic Culture 4", 
                         "EE390":"Summer Training",
                        "COMM101":"Communication Skills"}
Fifth_Year_sections = {"EE499":"5A","ISLS401":"5B","EE390":"5C","COMM101":"5D"}
Fifth_Year_capacity = {"EE499":30,"ISLS401":30,"EE390":30,"COMM101":30}

Fifth_Year_Times = {"EE499":" MonDay , 9-9:50","ISLS401":"TueDay , 10-10:50","COMM101":"WedDay , 11-11:50","EE390":"ThuDay , 9-9:50"}


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
power_courseClases = {"MEP261":"PAA","EE303":"PAB","EE341":"PAC","EE442":"PAD","EE441":"PAE","EE404":"PAF","EE451":"PAG","EE405":"PAH","EE453":"PAI","EE454":"PAJ"}
power_courseClasesCapacity = {"MEP261":30,"EE303":30,"EE341":30,"EE442":30,"EE441":30,"EE404":30,"EE451":30,"EE405":30,"EE453":30,"EE454":30}
power_courseClasesTimes = {"MEP261":" WedDay , 11-11:50","EE303":" MonDay , 9-9:50","EE341":" TueDay , 10-10:50","EE442":" ThuDay , 9-9:50","EE441":" WedDay , 9-9:50","EE404":" MonDay , 10-10:50","EE451":" TueDay , 9-9:50","EE405":" ThuDay , 10-10:50","EE453":" WedDay , 10-10:50","EE454":" MonDay , 11-11:50"}

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
computer_courseClases = {"EE305":"CAA","EE364":"CAB","EE361":"CAC","EE367":"CAD","EE460":"CAE","EE462":"CAF","EE463":"CAG"}
computer_courseClasesCapacity = {"EE305":30,"EE364":30,"EE361":30,"EE367":30,"EE460":30,"EE462":30,"EE463":30}
computer_courseClasesTimes = {"EE305":" ThuDay , 11-11:50","EE364":" WedDay , 9-9:50","EE361":" MonDay , 10-10:50","EE367":" TueDay , 9-9:50","EE460":" SunDay , 9-9:50","EE462":" MonDay , 9-9:50","EE463":" TueDay , 10-10:50"}
# Electronics and communication courses :
communication_courses_C = {"EE421":3, "EE423":3, "EE413":4, "EE425":3}
communication_courses_PR = {"EE421":"EE321, IE331", "EE423":"EE302, MATH204", "EE413":"EE312, EE321", "EE425":"EE421"}
communication_terms = {"EE421":9, "EE423":9, "EE413":10, "EE425":10}
communication_coursesName= {"EE421":"Communication Theory 1",
                            "EE423":"Magnetic 2",
                            "EE413":"Communication Circuits",
                            "EE425":"Communication Systems"}
communication_courseClases = {"EE421":"COAA","EE423":"COAB","EE413":"COAC","EE425":"COAD"}
communication_courseClasesCapacity = {"EE421":30,"EE423":30,"EE413":30,"EE425":30}
communication_courseClasesTimes = {"EE421":" ThuDay , 10-10:50","EE423":" WedDay , 9-9:50","EE413":" MonDay , 11-11:50","EE425":" TueDay , 11-11:50"}
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
biomedical_courseClases = {"BIO321":"BAA","EE374":"BAB","EE372":"BAC","EE370":"BAD","EE472":"BAE","EE474":"BAF","EE471":"BAG","EE470":"BAH"}
biomedical_courseClasesCapacity = {"BIO321":30,"EE374":30,"EE372":30,"EE370":30,"EE472":30,"EE474":30,"EE471":30,"EE470":30}
biomedical_courseClasesTimes = {"BIO321":" WedDay , 9-9:50","EE374":" MonDay , 10-10:50","EE372":" TueDay , 9-9:50","EE370":" ThuDay , 11-11:50","EE472":" SunDay , 9-9:50","EE474":" MonDay , 9-9:50","EE471":" TueDay , 10-10:50","EE470":" WedDay , 11-11:50"}


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


def computer_adding(x1, y1, z1, p1, m1,):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS Computer')
    cr.execute('CREATE TABLE IF NOT EXISTS Computer (course_code TEXT, course_name TEXT, credit INTEGER, prerequisites TEXT, terms INTEGER)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Computer (course_code, course_name, credit, prerequisites, terms) VALUES (?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], m1[i],))
    db.commit()
    db.close()

def power_adding(x1, y1, z1, p1, m1,):
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
power_sections = power_courseClases | Semi_Shared_Power_CoursesClasses|First_Year_sections | Second_Year_sections | Third_Year_sections | Fourth_Year_sections | Fifth_Year_sections
power_capacity = power_courseClasesCapacity | Semi_Shared_Power_CouresCapacity |First_Year_capacity | Second_Year_capacity | Third_Year_capacity | Fourth_Year_capacity | Fifth_Year_capacity
power_times = power_courseClasesTimes | Semi_Shared_Power_CouresTimes |First_Year_Times | Second_Year_Times | Third_Year_Times | Fourth_Year_Times | Fifth_Year_Times

for key in power_terms:
    if key =="EE366":
        power_terms[key]=9
    if key == "EE311":
        power_terms[key] = 6
power_adding((power_codes), (build_course_dict(power_codes, power_names)), (build_course_dict(power_codes, power_credits)), (build_course_dict(power_codes, power_prerequisites)), build_course_dict(power_codes, power_terms))


computer_codes = list(set(All + all_computer))
computer_names = All_Courses_Names | Semi_Shared_Courses_Names | computer_coursesName
computer_credits = PP | computer_courses_C | Semi_Shared_C
computer_prerequisites = All_Courses_PR | computer_courses_PR | Semi_Shared_PR
computer_terms = All_Terms | computer_terms | Semi_Shared_Terms_Computer
computer_sections = computer_courseClases | Semi_Shared_Computer_CoursesClasses |First_Year_sections | Second_Year_sections | Third_Year_sections | Fourth_Year_sections | Fifth_Year_sections
computer_capacity = computer_courseClasesCapacity | Semi_Shared_Computer_CoursesCapacity |First_Year_capacity | Second_Year_capacity | Third_Year_capacity | Fourth_Year_capacity | Fifth_Year_capacity
computer_times = computer_courseClasesTimes | Semi_Shared_Computer_CoursesTimes |First_Year_Times | Second_Year_Times | Third_Year_Times | Fourth_Year_Times | Fifth_Year_Times
computer_adding(
    computer_codes,
    build_course_dict(computer_codes, computer_names),
    build_course_dict(computer_codes, computer_credits),
    build_course_dict(computer_codes, computer_prerequisites),
    build_course_dict(computer_codes, computer_terms),
)


communication_codes = list(set(All + all_communication))
communication_names = All_Courses_Names | Semi_Shared_Courses_Names | communication_coursesName
communication_credits = PP | communication_courses_C | Semi_Shared_C
communication_prerequisites = All_Courses_PR | communication_courses_PR | Semi_Shared_PR
communication_terms = All_Terms | communication_terms | Semi_Shared_Terms_Communication
communication_sections = communication_courseClases | Semi_Shared_Communication_CoursesClasses |First_Year_sections | Second_Year_sections | Third_Year_sections | Fourth_Year_sections | Fifth_Year_sections
communication_capacity = communication_courseClasesCapacity | Semi_Shared_Communication_CoursesCapacity |First_Year_capacity | Second_Year_capacity | Third_Year_capacity | Fourth_Year_capacity | Fifth_Year_capacity
communication_times = communication_courseClasesTimes | Semi_Shared_Communication_CoursesTimes |First_Year_Times | Second_Year_Times | Third_Year_Times | Fourth_Year_Times | Fifth_Year_Times
communication_adding((communication_codes), (build_course_dict(communication_codes, communication_names)), (build_course_dict(communication_codes, communication_credits)), (build_course_dict(communication_codes, communication_prerequisites)), build_course_dict(communication_codes, communication_terms))


biomedical_codes = list(set(All + all_biomedical))
biomedical_names = All_Courses_Names | Semi_Shared_Courses_Names | biomedical_coursesName
biomedical_credits = PP | biomedical_courses_C | Semi_Shared_C
biomedical_prerequisites = All_Courses_PR | biomedical_courses_PR | Semi_Shared_PR
biomedical_terms = All_Terms | biomedical_terms | Semi_Shared_Terms_Biomedical
biomedical_sections = biomedical_courseClases | Semi_Shared_Biomedical_CoursesClasses |First_Year_sections | Second_Year_sections | Third_Year_sections | Fourth_Year_sections | Fifth_Year_sections
biomedical_capacity = biomedical_courseClasesCapacity | Semi_Shared_Biomedical_CoursesCapacity|First_Year_capacity | Second_Year_capacity | Third_Year_capacity | Fourth_Year_capacity | Fifth_Year_capacity
for key in biomedical_terms:
    if key == "IE256":
        biomedical_terms[key] = 8
    if key == "EE321":
        biomedical_terms[key] = 8
    if key == "ISLS301":
        biomedical_terms[key] = 9
biomedical_times = biomedical_courseClasesTimes | Semi_Shared_Biomedical_CoursesTimes |First_Year_Times | Second_Year_Times | Third_Year_Times | Fourth_Year_Times | Fifth_Year_Times
biomedical_adding((biomedical_codes), (build_course_dict(biomedical_codes, biomedical_names)), (build_course_dict(biomedical_codes, biomedical_credits)), (build_course_dict(biomedical_codes, biomedical_prerequisites)), build_course_dict(biomedical_codes, biomedical_terms))


######################################
# All courses:
def all_courses(x1, y1, z1, p1, a1, a2, i1):
    db = sqlite3.connect('courses.db')
    cr = db.cursor()
    cr.execute('DROP TABLE IF EXISTS courses')
    cr.execute('CREATE TABLE IF NOT EXISTS Courses (course_code TEXT, course_name TEXT, credit INTEGER, section TEXT, instructor INTEGER, capacity TEXT, time TEXT, prerequisites TEXT)')
    for i in range(len(x1)):
        cr.execute('INSERT INTO Courses (course_code, course_name, credit, prerequisites, section, capacity, instructor) VALUES (?, ?, ?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], a1[i], 25, i1[i]))
    for i in range(len(x1)):
        cr.execute('INSERT INTO Courses (course_code, course_name, credit, prerequisites, section, capacity, instructor) VALUES (?, ?, ?, ?, ?, ?, ?)',
               (x1[i] , y1[i], z1[i], p1[i], a2[i], 25, i1[i]))
    db.commit()
    db.close()


All_Courses = All + Semi_Shared_Courses + power + computer + communication + biomedical
All_Names = All_Courses_Names | Semi_Shared_Courses_Names | power_coursesName | computer_coursesName | communication_coursesName | biomedical_coursesName
All_Credits = PP | Semi_Shared_C | power_courses_C | computer_courses_C | communication_courses_C | biomedical_courses_C
All_Prerequisites = All_Courses_PR | Semi_Shared_PR | power_courses_PR | computer_courses_PR | communication_courses_PR | biomedical_courses_PR
All_terms = All_Terms | Semi_Shared_Terms_Biomedical | Semi_Shared_Terms_Communication | Semi_Shared_Terms_Computer | Semi_Shared_Terms_Power | computer_terms | power_terms | biomedical_terms | communication_terms

#=====================Classes-Times=========================#

B = {}

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
count = 0
SPC = 2   # how many sections there are for each course
for course in All_Courses:
    course_sections = []
    for j in range(SPC):
        first = letters[(count // 26) % 26]
        second = letters[count % 26]
        course_sections.append(first + second)
        count += 1

    B[course] = course_sections
A = loop_dict_value(B)
L = []
for i in A:
    L.append(i[0])
    L.append(i[1])
L1 = []
L2 = []
for j in range(74):
    L1.append(L[j])
    L2.append(L[j+74])
#============================================================#


db = sqlite3.connect("Users.db")
cr = db.cursor()
cr.execute("SELECT username, course_code FROM instructors")
teacher_for_course = (cr.fetchall())
new_teacher_for_course = []
for i in teacher_for_course:
    if i in new_teacher_for_course:
        continue
    new_teacher_for_course.append(i)
last_teacher_for_course = {}
for i in new_teacher_for_course:
    last_teacher_for_course[i[1]] = i[0]
db.commit()
db.close()

#============================================================#

all_courses(All_Courses,
            build_course_dict(All_Courses,All_Names),
            loop_dict_value(All_Credits),
            loop_dict_value(All_Prerequisites), 
            L1, L2, 
            loop_dict_value(last_teacher_for_course))

Times = {}
Times2 = {}
db = sqlite3.connect("courses.db")
cr = db.cursor()
cr.execute("SELECT course_code, section FROM Courses")
sections = cr.fetchall()
for i in sections:
    if i[0] not in Times:
        Times[i[0]] = i[1]
    Times2[i[0]] = i[1]
X = loop_dict_value(Times)
Y = loop_dict_value(Times2)
sections_per_course = []
for i in range(len(Times2)):
    sections_per_course.append(X[i])
    sections_per_course.append(Y[i])
db.commit()
db.close()


Classes_Times = ["9:00-9:50 , S T U", "8:00-9:15 , M W",  #MATH110
                 "10:00-10:50 , S T U", "9:30-10:45 , M W", # PHYS110
                 "11:00-11:50 , S T U", "11:00-12:45 , M W", # CHEM110
                 "9:00-9:50 , S T U", "8:00-9:15 , M W",     # CPIT110
                 "11:00-11:50 , S T U", "11:00-12:15 , M W",  # BIO110
                 "10:00-10:50 , S T U", "9:30-10:45 , M W", # STAT110
                 "1:00-2:30 , S M T W U", "1:30-3:00 , S M T W U", # ELIS110
                 "1:00-2:30 , S M T W U", "1:30-3:00 , S M T W U", # ELIS120
                 "1:00-2:15 , M W", "10:00-10:50, S T U", # MATH206
                 "9:00-10:50 , S M T W U", "11:00-12:50 , S M T W U", # IE200
                 "11:00-11:50 , S T U" , "1:00-1:50 , M W", # PHYS202
                 "2:00-4:50 , S" , "2:00-4:50 , T", # CHEM281
                 "11:00-12:15 , M W", "9:30-10:45 , M W", # EE201
                 "5:00-5:50 , S T" , "5:00-5:50 , M W", # ISLS101 
                 "6:00-6:50 , S T" , "6:00-6:50 , M W", # ARAB101
                 "9:00-10:50 , S T U" , "11:00-12:50 , S T U", # IE201
                 "9:30-10:45 , M W" , "10:00-10:50 , S T U", # IE255
                 "11:00-1:50 , T" , "11:00-1:50 , M" # MENG102
                 "1:00-2:15 , M W" , "1:00-1:50 , S T U", # MATH207
                 "2:00-4:50 , S" , "2:00-4:50 , M", # PHYS281
                 "7:00-7:50 , S T" , "6:00-6:50 , M W", # ARAB201
                 "9:30-10:45 , M W" , "11:00-12:15 , M W", # EE202
                 "9:00-9:50 , S T U" , "9:30-10:45 , M W", # EE250
                 "1:00-2:15 , M W" , "10:00-10:50 , S T U", # MATH204
                 "7:00-7:50 , S T" , "6:00-6:00 , M W", # ISLS201
                 "9:00-9:50 , S T U" , "9:00-9:15 , M W", # EE300
                 "10:00-10:50 , S T U" , "10:30-11:45 , M W", # EE301
                 "11:00-12:50 , S T U" , "12:00-1:50 , S T U", #IE202
                 "11:00-11:50 , S T U" , "1:00-1:50 , S T U", # EE321
                 "" #EE311 -- i Will finish the rest tomorrow inshallah beacause this needs planning well before getting into it.
                ]  