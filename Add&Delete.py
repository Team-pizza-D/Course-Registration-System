import sqlite3

db = sqlite3.connect("courses.db")
cr = db.cursor()

cr.execute("""
CREATE TABLE IF NOT EXISTS StudentCourses (
    student_id TEXT,
    course_code TEXT,
    PRIMARY KEY (student_id, course_code)
)
""")

db.commit()
db.close()
def add_course(student_id, course_code, transcript):
    db = sqlite3.connect("courses.db")
    cr = db.cursor()

    # 1. Check course capacity
    cr.execute(f"SELECT capacity FROM {transcript} WHERE course_code = ?", (course_code,))
    row = cr.fetchone()

    if row is None:
        print("❌ Course not found in transcript.")
        db.close()
        return
    
    capacity = row[0]

    if capacity <= 0:
        print("❌ Course is full.")
        db.close()
        return

    # 2. Add to StudentCourses
    try:
        cr.execute(
            "INSERT INTO StudentCourses (student_id, course_code) VALUES (?, ?)",
            (student_id, course_code)
        )
    except sqlite3.IntegrityError:
        print("⚠ Student already registered in that course.")
        db.close()
        return

    # 3. Reduce capacity
    cr.execute(
        f"UPDATE {transcript} SET capacity = capacity - 1 WHERE course_code = ?",
        (course_code,)
    )

    db.commit()
    db.close()
    print("✅ Course added, capacity reduced.")

def drop_course(student_id, course_code, transcript):
    db = sqlite3.connect("courses.db")
    cr = db.cursor()

    # 1. Delete row from StudentCourses
    cr.execute(
        "DELETE FROM StudentCourses WHERE student_id = ? AND course_code = ?",
        (student_id, course_code)
    )

    if cr.rowcount == 0:
        print("❌ Student is not registered in that course.")
        db.close()
        return

    # 2. Increase capacity
    cr.execute(
        f"UPDATE {transcript} SET capacity = capacity + 1 WHERE course_code = ?",
        (course_code,)
    )

    db.commit()
    db.close()
    print("🔄 Course deleted, capacity increased.")
def get_student_courses(student_id):
    db = sqlite3.connect("courses.db")
    cr = db.cursor()
    
    cr.execute("SELECT course_code FROM StudentCourses WHERE student_id = ?", (student_id,))
    courses = cr.fetchall()
    
    db.close()
    return [c[0] for c in courses]
# print(get_student_courses(""))


# c = get_course_object("Communication", "EE421")
# print(c.name, c.credit)
drop_course("2020555", "EE331", "Power")
drop_course("2480110", "EE331", "Power")
drop_course("2480110", "EE300", "Power")





