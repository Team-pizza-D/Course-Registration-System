import sqlite3
import random
from classses2 import student

# ====== Grade scale ======
def score_to_letter(score: int) -> str:
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "B+"
    elif score >= 80:
        return "B"
    elif score >= 75:
        return "C+"
    elif score >= 70:
        return "C"
    elif score >= 65:
        return "D+"
    else:
        return "D" 

def random_grade():
    score = random.randint(60, 100)
    letter = score_to_letter(score)
    return letter, score

# ====== Study plans (plan, semester) ======
# first -- computer
PLAN_COMPUTER = [
    ('IE255', 4), ('EE390', 11), ('EE462', 10), ('EE364', 8), ('BIO110', 2),
    ('CHEM110', 1), ('MENG102', 4), ('PHYS281', 4), ('EE250', 5), ('EE301', 6),
    ('ARAB101', 4), ('ISLS301', 8), ('ELIS110', 1), ('EE499', 9), ('PHYS110', 2),
    ('EE367', 8), ('EE202', 5), ('EE366', 8), ('EE360', 7), ('STAT110', 1),
    ('MATH206', 3), ('CHEM281', 3), ('ISLS101', 3), ('IE201', 4), ('MATH110', 1),
    ('EE321', 7), ('EE460', 9), ('ARAB201', 5), ('ISLS201', 5), ('IE202', 6),
    ('ELIS120', 2), ('EE332', 8), ('EE361', 8), ('ISLS401', 10), ('IE331', 6),
    ('CPIT110', 2), ('PHYS202', 3), ('EE201', 3), ('MATH204', 5), ('EE305', 7),
    ('EE306', 6), ('IE200', 3), ('COMM101', 10), ('EE331', 9), ('IE256', 7),
    ('EE311', 7), ('EE463', 10), ('EE300', 6), ('MATH207', 4)
]

# second -- power
PLAN_POWER = [
    ('IE255', 4), ('EE390', 11), ('EE441', 9), ('BIO110', 2), ('CHEM110', 1),
    ('MENG102', 4), ('PHYS281', 4), ('EE250', 5), ('EE301', 6), ('ARAB101', 4),
    ('MEP261', 6), ('EE454', 10), ('ISLS301', 8), ('ELIS110', 1), ('EE499', 9),
    ('PHYS110', 2), ('EE202', 5), ('EE366', 9), ('EE360', 7), ('STAT110', 1),
    ('MATH206', 3), ('CHEM281', 3), ('EE341', 8), ('EE451', 9), ('ISLS101', 3),
    ('IE201', 4), ('MATH110', 1), ('EE453', 10), ('EE321', 7), ('ARAB201', 5),
    ('ISLS201', 5), ('IE202', 6), ('ELIS120', 2), ('EE332', 8), ('ISLS401', 10),
    ('CPIT110', 2), ('EE302', 7), ('PHYS202', 3), ('EE303', 7), ('EE201', 3),
    ('MATH204', 5), ('EE351', 8), ('IE200', 3), ('COMM101', 10), ('EE331', 8),
    ('EE442', 9), ('EE405', 10), ('IE256', 7), ('EE404', 9), ('EE311', 7),
    ('EE300', 6), ('MATH207', 4)
]

# third -- communication
PLAN_COMM = [
    ('IE255', 4), ('EE390', 11), ('BIO110', 2), ('CHEM110', 1), ('MENG102', 4),
    ('PHYS281', 4), ('EE250', 5), ('EE301', 6), ('ARAB101', 4), ('ISLS301', 8),
    ('ELIS110', 1), ('EE499', 9), ('PHYS110', 2), ('EE423', 9), ('EE202', 5),
    ('EE366', 8), ('EE360', 7), ('STAT110', 1), ('MATH206', 3), ('CHEM281', 3),
    ('ISLS101', 3), ('IE201', 4), ('MATH110', 1), ('EE321', 7), ('ARAB201', 5),
    ('ISLS201', 5), ('IE202', 6), ('EE413', 10), ('ELIS120', 2), ('EE332', 8),
    ('ISLS401', 10), ('IE331', 7), ('CPIT110', 2), ('EE302', 6), ('PHYS202', 3),
    ('EE201', 3), ('MATH204', 5), ('EE351', 9), ('EE306', 6), ('IE200', 3),
    ('EE425', 10), ('COMM101', 10), ('EE331', 8), ('EE312', 8), ('IE256', 7),
    ('EE311', 7), ('EE300', 6), ('MATH207', 4), ('EE421', 9)
]

# fourth -- biomedical
PLAN_BIO = [
    ('IE255', 4), ('EE390', 11), ('BIO110', 2), ('CHEM110', 1), ('MENG102', 4),
    ('PHYS281', 4), ('EE250', 5), ('EE301', 6), ('ARAB101', 4), ('EE471', 9),
    ('EE470', 9), ('EE370', 8), ('ISLS301', 9), ('ELIS110', 1), ('EE499', 9),
    ('PHYS110', 2), ('EE374', 7), ('EE202', 5), ('EE366', 8), ('EE360', 7),
    ('STAT110', 1), ('MATH206', 3), ('CHEM281', 3), ('ISLS101', 3), ('IE201', 4),
    ('MATH110', 1), ('EE321', 8), ('ARAB201', 5), ('ISLS201', 5), ('IE202', 6),
    ('ELIS120', 2), ('ISLS401', 10), ('CPIT110', 2), ('EE302', 7), ('BIO321', 6),
    ('EE472', 10), ('EE474', 10), ('PHYS202', 3), ('EE201', 3), ('MATH204', 5),
    ('EE306', 6), ('IE200', 3), ('COMM101', 10), ('EE372', 7), ('EE312', 8),
    ('IE256', 8), ('EE311', 7), ('EE300', 6), ('MATH207', 4)
]

MAJOR_COMPUTER = "Electrical computer engineering"
MAJOR_POWER = "Electrical power and machines engineering"
MAJOR_COMM = "Electrical communication and electronics engineering"
MAJOR_BIO = "Electrical biomedical engineering"

PLAN_BY_MAJOR = {
    MAJOR_COMPUTER: PLAN_COMPUTER,
    MAJOR_POWER: PLAN_POWER,
    MAJOR_COMM: PLAN_COMM,
    MAJOR_BIO: PLAN_BIO,
}

def insert_grades_for_student(student_id: str, major: str, current_term: int):
    plan = PLAN_BY_MAJOR[major]
    completed_courses = [c for (c, sem) in plan if sem <= current_term]

    rows = []
    for course in completed_courses:
        letter, score = random_grade()
        rows.append((student_id, course, letter, score))

    db = sqlite3.connect("Users.db")
    cr = db.cursor()
    cr.executemany(
        "INSERT INTO grades (student_id, course, letter_grade, numeric_grade) VALUES (?, ?, ?, ?)",
        rows
    )
    db.commit()
    db.close()


# ====== TERM 1 (starts with 26) ======
st51 = student('2610001', 'ahmed',   'ahmed2610001@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st52 = student('2610002', 'omar',    'omar2610002@stu.kau.edu.sa',    MAJOR_POWER, database=True)
st53 = student('2610003', 'saad',    'saad2610003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st54 = student('2610004', 'ali',     'ali2610004@stu.kau.edu.sa',     MAJOR_BIO, database=True)

st55 = student('2610005', 'khalid',  'khalid2610005@stu.kau.edu.sa',  MAJOR_COMPUTER, database=True)
st56 = student('2610006', 'fahad',   'fahad2610006@stu.kau.edu.sa',   MAJOR_POWER, database=True)
st57 = student('2610007', 'sultan',  'sultan2610007@stu.kau.edu.sa',  MAJOR_COMM, database=True)
st58 = student('2610008', 'yousef',  'yousef2610008@stu.kau.edu.sa',  MAJOR_BIO, database=True)

st59 = student('2610009', 'ibrahim', 'ibrahim2610009@stu.kau.edu.sa', MAJOR_COMPUTER, database=True)
st60 = student('2610010', 'nasser',  'nasser2610010@stu.kau.edu.sa',  MAJOR_POWER, database=True)
st61 = student('2610011', 'turki',   'turki2610011@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st62 = student('2610012', 'hamad',   'hamad2610012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term1_students = [st51, st52, st53, st54, st55, st56, st57, st58, st59, st60, st61, st62]

# ====== TERM 2 (starts with 26) ======
st63 = student('2620001', 'majed',    'majed2620001@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st64 = student('2620002', 'anas',     'anas2620002@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st65 = student('2620003', 'rayan',    'rayan2620003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st66 = student('2620004', 'salem',    'salem2620004@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st67 = student('2620005', 'hassan',   'hassan2620005@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st68 = student('2620006', 'hadi',     'hadi2620006@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st69 = student('2620007', 'bandar',   'bandar2620007@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st70 = student('2620008', 'talal',    'talal2620008@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st71 = student('2620009', 'nawaf',    'nawaf2620009@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st72 = student('2620010', 'mohammed', 'mohammed2620010@stu.kau.edu.sa', MAJOR_POWER, database=True)
st73 = student('2620011', 'abdullah', 'abdullah2620011@stu.kau.edu.sa', MAJOR_COMM, database=True)
st74 = student('2620012', 'yazeed',   'yazeed2620012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term2_students = [st63, st64, st65, st66, st67, st68, st69, st70, st71, st72, st73, st74]

# ====== TERM 3 (starts with 25) ======
st75 = student('2510001', 'ahmed',   'ahmed2510001@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st76 = student('2510002', 'omar',    'omar2510002@stu.kau.edu.sa',    MAJOR_POWER, database=True)
st77 = student('2510003', 'saad',    'saad2510003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st78 = student('2510004', 'ali',     'ali2510004@stu.kau.edu.sa',     MAJOR_BIO, database=True)

st79 = student('2510005', 'khalid',  'khalid2510005@stu.kau.edu.sa',  MAJOR_COMPUTER, database=True)
st80 = student('2510006', 'fahad',   'fahad2510006@stu.kau.edu.sa',   MAJOR_POWER, database=True)
st81 = student('2510007', 'sultan',  'sultan2510007@stu.kau.edu.sa',  MAJOR_COMM, database=True)
st82 = student('2510008', 'yousef',  'yousef2510008@stu.kau.edu.sa',  MAJOR_BIO, database=True)

st83 = student('2510009', 'ibrahim', 'ibrahim2510009@stu.kau.edu.sa', MAJOR_COMPUTER, database=True)
st84 = student('2510010', 'nasser',  'nasser2510010@stu.kau.edu.sa',  MAJOR_POWER, database=True)
st85 = student('2510011', 'turki',   'turki2510011@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st86 = student('2510012', 'hamad',   'hamad2510012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term3_students = [st75, st76, st77, st78, st79, st80, st81, st82, st83, st84, st85, st86]

# ====== TERM 4 (starts with 25) ======
st87 = student('2520001', 'majed',    'majed2520001@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st88 = student('2520002', 'anas',     'anas2520002@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st89 = student('2520003', 'rayan',    'rayan2520003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st90 = student('2520004', 'salem',    'salem2520004@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st91  = student('2520005', 'hassan',   'hassan2520005@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st92  = student('2520006', 'hadi',     'hadi2520006@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st93  = student('2520007', 'bandar',   'bandar2520007@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st94  = student('2520008', 'talal',    'talal2520008@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st95  = student('2520009', 'nawaf',    'nawaf2520009@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st96  = student('2520010', 'mohammed', 'mohammed2520010@stu.kau.edu.sa', MAJOR_POWER, database=True)
st97  = student('2520011', 'abdullah', 'abdullah2520011@stu.kau.edu.sa', MAJOR_COMM, database=True)
st98  = student('2520012', 'yazeed',   'yazeed2520012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term4_students = [st87, st88, st89, st90, st91, st92, st93, st94, st95, st96, st97, st98]

# ====== TERM 6 (starts with 24) ======
st99  = student('2460001', 'ahmed',   'ahmed2460001@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st100 = student('2460002', 'omar',    'omar2460002@stu.kau.edu.sa',    MAJOR_POWER, database=True)
st101 = student('2460003', 'saad',    'saad2460003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st102 = student('2460004', 'ali',     'ali2460004@stu.kau.edu.sa',     MAJOR_BIO, database=True)

st103 = student('2460005', 'khalid',  'khalid2460005@stu.kau.edu.sa',  MAJOR_COMPUTER, database=True)
st104 = student('2460006', 'fahad',   'fahad2460006@stu.kau.edu.sa',   MAJOR_POWER, database=True)
st105 = student('2460007', 'sultan',  'sultan2460007@stu.kau.edu.sa',  MAJOR_COMM, database=True)
st106 = student('2460008', 'yousef',  'yousef2460008@stu.kau.edu.sa',  MAJOR_BIO, database=True)

st107 = student('2460009', 'ibrahim', 'ibrahim2460009@stu.kau.edu.sa', MAJOR_COMPUTER, database=True)
st108 = student('2460010', 'nasser',  'nasser2460010@stu.kau.edu.sa',  MAJOR_POWER, database=True)
st109 = student('2460011', 'turki',   'turki2460011@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st110 = student('2460012', 'hamad',   'hamad2460012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term6_students = [st99, st100, st101, st102, st103, st104, st105, st106, st107, st108, st109, st110]

# ====== TERM 7 (starts with 23) ======
st111 = student('2310001', 'majed',    'majed2310001@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st112 = student('2310002', 'anas',     'anas2310002@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st113 = student('2310003', 'rayan',    'rayan2310003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st114 = student('2310004', 'salem',    'salem2310004@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st115 = student('2310005', 'hassan',   'hassan2310005@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st116 = student('2310006', 'hadi',     'hadi2310006@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st117 = student('2310007', 'bandar',   'bandar2310007@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st118 = student('2310008', 'talal',    'talal2310008@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st119 = student('2310009', 'nawaf',    'nawaf2310009@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st120 = student('2310010', 'mohammed', 'mohammed2310010@stu.kau.edu.sa', MAJOR_POWER, database=True)
st121 = student('2310011', 'abdullah', 'abdullah2310011@stu.kau.edu.sa', MAJOR_COMM, database=True)
st122 = student('2310012', 'yazeed',   'yazeed2310012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term7_students = [st111, st112, st113, st114, st115, st116, st117, st118, st119, st120, st121, st122]

# ====== TERM 8 (starts with 23) ======
st123 = student('2320001', 'ahmed',   'ahmed2320001@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st124 = student('2320002', 'omar',    'omar2320002@stu.kau.edu.sa',    MAJOR_POWER, database=True)
st125 = student('2320003', 'saad',    'saad2320003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st126 = student('2320004', 'ali',     'ali2320004@stu.kau.edu.sa',     MAJOR_BIO, database=True)

st127 = student('2320005', 'khalid',  'khalid2320005@stu.kau.edu.sa',  MAJOR_COMPUTER, database=True)
st128 = student('2320006', 'fahad',   'fahad2320006@stu.kau.edu.sa',   MAJOR_POWER, database=True)
st129 = student('2320007', 'sultan',  'sultan2320007@stu.kau.edu.sa',  MAJOR_COMM, database=True)
st130 = student('2320008', 'yousef',  'yousef2320008@stu.kau.edu.sa',  MAJOR_BIO, database=True)

st131 = student('2320009', 'ibrahim', 'ibrahim2320009@stu.kau.edu.sa', MAJOR_COMPUTER, database=True)
st132 = student('2320010', 'nasser',  'nasser2320010@stu.kau.edu.sa',  MAJOR_POWER, database=True)
st133 = student('2320011', 'turki',   'turki2320011@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st134 = student('2320012', 'hamad',   'hamad2320012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term8_students = [st123, st124, st125, st126, st127, st128, st129, st130, st131, st132, st133, st134]

# ====== TERM 9 (starts with 22) ======
st135 = student('2210001', 'majed',    'majed2210001@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st136 = student('2210002', 'anas',     'anas2210002@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st137 = student('2210003', 'rayan',    'rayan2210003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st138 = student('2210004', 'salem',    'salem2210004@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st139 = student('2210005', 'hassan',   'hassan2210005@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st140 = student('2210006', 'hadi',     'hadi2210006@stu.kau.edu.sa',     MAJOR_POWER, database=True)
st141 = student('2210007', 'bandar',   'bandar2210007@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st142 = student('2210008', 'talal',    'talal2210008@stu.kau.edu.sa',    MAJOR_BIO, database=True)

st143 = student('2210009', 'nawaf',    'nawaf2210009@stu.kau.edu.sa',    MAJOR_COMPUTER, database=True)
st144 = student('2210010', 'mohammed', 'mohammed2210010@stu.kau.edu.sa', MAJOR_POWER, database=True)
st145 = student('2210011', 'abdullah', 'abdullah2210011@stu.kau.edu.sa', MAJOR_COMM, database=True)
st146 = student('2210012', 'yazeed',   'yazeed2210012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term9_students = [st135, st136, st137, st138, st139, st140, st141, st142, st143, st144, st145, st146]

# ====== TERM 10 (starts with 22) ======
st147 = student('2220001', 'ahmed',   'ahmed2220001@stu.kau.edu.sa',   MAJOR_COMPUTER, database=True)
st148 = student('2220002', 'omar',    'omar2220002@stu.kau.edu.sa',    MAJOR_POWER, database=True)
st149 = student('2220003', 'saad',    'saad2220003@stu.kau.edu.sa',    MAJOR_COMM, database=True)
st150 = student('2220004', 'ali',     'ali2220004@stu.kau.edu.sa',     MAJOR_BIO, database=True)

st151 = student('2220005', 'khalid',  'khalid2220005@stu.kau.edu.sa',  MAJOR_COMPUTER, database=True)
st152 = student('2220006', 'fahad',   'fahad2220006@stu.kau.edu.sa',   MAJOR_POWER, database=True)
st153 = student('2220007', 'sultan',  'sultan2220007@stu.kau.edu.sa',  MAJOR_COMM, database=True)
st154 = student('2220008', 'yousef',  'yousef2220008@stu.kau.edu.sa',  MAJOR_BIO, database=True)

st155 = student('2220009', 'ibrahim', 'ibrahim2220009@stu.kau.edu.sa', MAJOR_COMPUTER, database=True)
st156 = student('2220010', 'nasser',  'nasser2220010@stu.kau.edu.sa',  MAJOR_POWER, database=True)
st157 = student('2220011', 'turki',   'turki2220011@stu.kau.edu.sa',   MAJOR_COMM, database=True)
st158 = student('2220012', 'hamad',   'hamad2220012@stu.kau.edu.sa',   MAJOR_BIO, database=True)

term10_students = [st147, st148, st149, st150, st151, st152, st153, st154, st155, st156, st157, st158]


all_terms = [
    (1, term1_students),
    (2, term2_students),
    (3, term3_students),
    (4, term4_students),
    (6, term6_students),
    (7, term7_students),
    (8, term8_students),
    (9, term9_students),
    (10, term10_students),
]

# for term_number, students_in_term in all_terms:
#     for s in students_in_term:
#         insert_grades_for_student(s.Id, s.major, term_number)
