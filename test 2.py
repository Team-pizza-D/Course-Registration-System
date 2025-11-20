import sqlite3

# def connect_db():
#     return sqlite3.connect("students.db")

# def create_students_table():
#     db = sqlite3.connect("Users.db")
#     cr = db.cursor()
#     cr.execute("""
#     CREATE TABLE IF NOT EXISTS students (
#         username TEXT,
#         password TEXT,
#         email TEXT,
#         status TEXT,
#         Id INTEGER PRIMARY KEY,
#         GPA REAL
#     )
#     """)
#     db.commit()
#     db.close()

# def create_admin_table():
#     db = sqlite3.connect("Users.db")
#     cr = db.cursor()
#     cr.execute("""
#     CREATE TABLE IF NOT EXISTS admins (
#                username TEXT,
#                password TEXT,
#                email TEXT,
#                status TEXT
#                )
#                """)

# def insert_student(user):
#     db = connect_db()
#     cr = db.cursor()
#     cr.execute("""
#     INSERT INTO students (username, password, email, status, Id)
#     VALUES (?, ?, ?, ?, ?)
#     """, (user.username, user.password, user.email, user.status, user.Id))
#     db.commit()
#     db.close()
#     print(f"suc Added {user.username} to database.")

# def get_all_students():
#     db = connect_db()
#     cr = db.cursor()
#     cr.execute("SELECT * FROM students")
#     rows = cr.fetchall()
#     db.close()
#     return rows
# create_admin_table()
# create_students_table()
# from classes import user


# Create table if not already exists


# Get user input
# data = input("Enter username, password, email, status, Id, GPA separated by commas: ").split(",")
# data = [x.strip() for x in data]

# # Create User object
# username, password, email, status, Id, = data
# student = user(username, password, email, status, int(Id))

# Add student to database
# create_students_table()
# insert_student(student)

# Display all students
# print("\nAll students in database:")
# for row in get_all_students():
#     print(row)

db = sqlite3.connect("courses.db")
cr = db.cursor()
cr.execute("SELECT times,credit,course_code,terms FROM computer where terms <= 4")
azoz = cr.fetchall()
print(azoz)
times = [item[0].split(',')[1].strip() for item in azoz]
db.commit()
db.close()
print(times)