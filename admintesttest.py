import os
import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QShortcut
from PyQt5.QtGui import QKeySequence
from classses2 import admin       
from Admin_Window import AdminWindow  

class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Login.ui")
        uic.loadUi(ui_path, self)
        self.setFixedWidth(552)
        self.setFixedHeight(650)

        self.loginButton.clicked.connect(self.loginfunction)

        # Enter triggers login
        QShortcut(QKeySequence("Return"), self, self.loginButton.click)
        QShortcut(QKeySequence("Enter"), self, self.loginButton.click)

        self.checkBox_show.stateChanged.connect(self.toggle_password)

    def toggle_password(self):
        if self.checkBox_show.isChecked():
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    def check_admin(self, uni_id, password):
        """
        Uses admin + user.correct_password from classses2.py
        Returns (id, name) if admin is valid, else None.
        """
        try:
            a = admin(id=uni_id)

            # Check that this ID belongs to an admin
            if not a.is_admin():
                return None

            # Verify password
            if not a.correct_password(password):
                return None

            name = a.username
            return (uni_id, name)

        except Exception:
            return None

    def loginfunction(self):
        UniID = self.IDlineEdit.text().strip()
        password = self.PasslineEdit.text().strip()

        # Admin login
        admin_data = self.check_admin(UniID, password)
        if admin_data:
            admin_id, admin_name = admin_data
            self.openAdminWindow(admin_id, admin_name)
            return

        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid ID or Password.")

    def openAdminWindow(self, admin_id, admin_name):
        self.hide()
        self.main_window = AdminWindow(admin_id=admin_id, admin_name=admin_name)
        self.main_window.show()


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, admin_id, admin_name):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Admin_Window.ui")
        uic.loadUi(ui_path, self)
        
        self.setFixedWidth(1471)
        self.setFixedHeight(966)
        self.adminName = admin_name
        self.admin_id = admin_id
        self.admin_obj = admin(id=self.admin_id)

        self.welcomeLabel.setText(f"Welcome, {self.adminName}!")
        self.tabWidget.setCurrentIndex(0)
        self.current_student = None
        self.available_section_map = {}   # row -> section (right table)
        self.current_section_map = {}     # row -> section (left table)

        # General table settings
        for table in (
            self.StudentCourseTable,
            self.Tab2_SubjectsTable,
            getattr(self, "Tab1_StudentTable", None),
            getattr(self, "CapacityTable", None),
            getattr(self, "StudentGradeTable_4", None),
        ):
            if table is None:
                continue
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.verticalHeader().setVisible(False)

        def center_row_items(self, table, row):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)

        # Load Tab 1 student table initially
        self.load_tab1_students()
        # Load Tab 3 table initially
        self.load_capacity_table()
        # Load Tab 4 grade table initially
        self.load_tab4_grade_table()

        # ---------- Connections ----------
        # Tab 1: add/delete student
        self.Tab1_AddStudent.clicked.connect(self.tab1_add_student)
        self.Tab1_DeleteStudent.clicked.connect(self.tab1_delete_student)

        # Tab 2: submit student
        self.pushButton.clicked.connect(self.handle_submit_student)

        # Tab 2: add/remove course
        self.Tab2_AddCourse.clicked.connect(self.add_selected_course)
        self.Tab2_DeleteCourse.clicked.connect(self.remove_selected_course)

        # Tab 3: capacity
        self.Tab3_Confirm.clicked.connect(self.handle_tab3_capacity_change)

        #Tab 4 : Grades
        self.Tab4_Confirm.clicked.connect(self.handle_tab4_grading)

        # Enrollment message label
        self.EnrollmentMessege.setText("")

    # =========================================================
    # TAB 1 - Student Add/Delete
    # =========================================================

    def tab1_add_student(self):
        first = self.Tab1_FirstName.text().strip()
        last = self.Tab1_LastName.text().strip()

        if not first or not last:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill both first and last name.")
            return

        # Default major (change if needed)
        major = "Electrical communication and electronics engineering"

        ok, msg = self.admin_obj.add_student(first, last, major)

        QtWidgets.QMessageBox.information(self, "Add Student", msg)

        self.load_tab1_students()

        self.Tab1_FirstName.clear()
        self.Tab1_LastName.clear()

    def tab1_delete_student(self):
        student_id = self.Tab1_Student_ID.text().strip()

        if not student_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a valid numeric student ID.")
            return

        ok, msg = self.admin_obj.delete_student(student_id)

        QtWidgets.QMessageBox.information(self, "Delete Student", msg)

        self.load_tab1_students()

        self.Tab1_Student_ID.clear()

    def load_tab1_students(self):
        from classses2 import users_db

        rows = users_db.execute(
            "SELECT id, username, email FROM students",
            fetchall=True
        )

        table = self.Tab1_StudentTable
        table.setRowCount(0)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Student ID", "Name", "Email Address"])

        if not rows:
            return
        for r_index, (stu_id, name, email) in enumerate(rows):
            table.insertRow(r_index)

            item_id = QtWidgets.QTableWidgetItem(str(stu_id))
            item_name = QtWidgets.QTableWidgetItem(name)
            item_email = QtWidgets.QTableWidgetItem(email)

            item_id.setTextAlignment(QtCore.Qt.AlignCenter)
            item_name.setTextAlignment(QtCore.Qt.AlignCenter)
            item_email.setTextAlignment(QtCore.Qt.AlignCenter)

            table.setItem(r_index, 0, item_id)
            table.setItem(r_index, 1, item_name)
            table.setItem(r_index, 2, item_email)

        header = table.horizontalHeader()
        for col in range(table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)

    # =========================================================
    # TAB 2 — Subject Enrollment
    # =========================================================

    def handle_submit_student(self):
        self.EnrollmentMessege.setText("")

        id_text = self.Tab2_StudentID.text().strip()
        if not id_text.isdigit():
            self.EnrollmentMessege.setText("Please enter a valid numeric student ID.")
            self.clear_enrollment_tables()
            self.current_student = None
            return

        sid = int(id_text)
        stu = student(id=sid)

        if not stu.is_student():
            self.EnrollmentMessege.setText(f"Student with ID {sid} not found.")
            self.clear_enrollment_tables()
            self.current_student = None
            return

        self.current_student = stu
        self.load_student_current_courses_table()
        self.load_available_subjects_table()

    def clear_enrollment_tables(self):
        self.StudentCourseTable.clearContents()
        self.Tab2_SubjectsTable.clearContents()
        self.StudentCourseTable.setRowCount(0)
        self.Tab2_SubjectsTable.setRowCount(0)

    def load_available_subjects_table(self):
        table = self.Tab2_SubjectsTable
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["", "Course Code", "Instructor", "Section", "Time", "Credit"]
        )
        table.verticalHeader().setVisible(False)

        if self.current_student is None:
            return

        available = self.current_student.view_available_subjects()

        if isinstance(available, str) or available is None:
            self.EnrollmentMessege.setText(str(available))
            return

        self.available_section_map = {}
        table.setRowCount(len(available))

        row = 0
        for _, (section, course_code, instructor, time, credit) in available.items():
            # Checkbox
            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("margin-left: 8px;")
            checkbox.stateChanged.connect(self.on_available_checkbox_changed)
            table.setCellWidget(row, 0, checkbox)

            self.available_section_map[row] = section

            items = [
                QtWidgets.QTableWidgetItem(course_code),
                QtWidgets.QTableWidgetItem(instructor),
                QtWidgets.QTableWidgetItem(section),
                QtWidgets.QTableWidgetItem(time),
                QtWidgets.QTableWidgetItem(str(credit)),
            ]

            col = 1
            for item in items:
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)
                col += 1

            row += 1

        # Column widths
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)  # Section
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)  # Credit
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def on_available_checkbox_changed(self, state):
        table = self.Tab2_SubjectsTable
        sender = self.sender()
        clicked_row = None

        for row in range(table.rowCount()):
            if table.cellWidget(row, 0) == sender:
                clicked_row = row
                break

        if clicked_row is None:
            return

        # If unchecked -> restore all
        if state == 0:
            self.restore_available_rows()
            return

        # If checked -> gray out others
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if row != clicked_row:
                checkbox.setEnabled(False)
                self.set_available_row_gray(row)
            else:
                checkbox.setEnabled(True)
                self.set_available_row_normal(row)

    def set_available_row_gray(self, row):
        table = self.Tab2_SubjectsTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("#7a7a7a"))

    def set_available_row_normal(self, row):
        table = self.Tab2_SubjectsTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("white"))

    def restore_available_rows(self):
        table = self.Tab2_SubjectsTable

        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox:
                checkbox.setEnabled(True)
                checkbox.setChecked(False)

            for col in range(1, table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor("#001622"))
                    item.setForeground(QtGui.QColor("white"))

    def load_student_current_courses_table(self):
        table = self.StudentCourseTable
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["", "Course Code", "Instructor", "Section", "Time", "Credit"]
        )
        table.verticalHeader().setVisible(False)

        if self.current_student is None:
            return

        schedule = self.current_student.view_enrolled_subjects()

        if isinstance(schedule, str) or schedule is None:
            self.EnrollmentMessege.setText(str(schedule))
            return

        self.current_section_map = {}
        table.setRowCount(len(schedule))

        row = 0
        for section, (course_code, course_name, time_days,
                     section_name, credit, instructor) in schedule.items():

            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("margin-left: 8px;")
            checkbox.stateChanged.connect(self.on_current_checkbox_changed)
            table.setCellWidget(row, 0, checkbox)

            self.current_section_map[row] = section

            # Parse "9:00-9:50 , S T U" to "9:00-9:50, S T U"
            try:
                time_part, days_part = time_days.split(",")
                time_str = time_part.strip()
                days_str = days_part.strip()
                time_display = f"{time_str}, {days_str}"
            except ValueError:
                time_display = time_days

            items = [
                QtWidgets.QTableWidgetItem(course_code),
                QtWidgets.QTableWidgetItem(instructor),
                QtWidgets.QTableWidgetItem(section),
                QtWidgets.QTableWidgetItem(time_display),
                QtWidgets.QTableWidgetItem(str(credit)),
            ]

            col = 1
            for item in items:
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)
                col += 1

            row += 1

        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)  # Section
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)  # Credit
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def on_current_checkbox_changed(self, state):
        table = self.StudentCourseTable
        sender = self.sender()
        clicked_row = None

        for row in range(table.rowCount()):
            if table.cellWidget(row, 0) == sender:
                clicked_row = row
                break

        if clicked_row is None:
            return

        if state == 0:
            self.restore_current_rows()
            return

        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if row != clicked_row:
                checkbox.setEnabled(False)
                self.set_current_row_gray(row)
            else:
                checkbox.setEnabled(True)
                self.set_current_row_normal(row)

    def set_current_row_gray(self, row):
        table = self.StudentCourseTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("#7a7a7a"))

    def set_current_row_normal(self, row):
        table = self.StudentCourseTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("white"))

    def restore_current_rows(self):
        table = self.StudentCourseTable
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox:
                checkbox.setEnabled(True)
                checkbox.setChecked(False)

            for col in range(1, table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor("#001622"))
                    item.setForeground(QtGui.QColor("white"))

    def add_selected_course(self):
        if self.current_student is None:
            QtWidgets.QMessageBox.warning(
                self, "Enrollment", "Please submit a valid Student ID first."
            )
            return

        table = self.Tab2_SubjectsTable
        selected_section = None

        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_section = self.available_section_map.get(row)
                break

        if not selected_section:
            QtWidgets.QMessageBox.warning(self, "Enrollment", "Please select a course to add.")
            return

        try:
            ok, msg = self.admin_obj.add_subject(selected_section, self.current_student.id)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Enrollment Error",
                f"Unexpected error while enrolling in {selected_section}:\n{e}",
            )
            return

        if ok:
            QtWidgets.QMessageBox.information(self, "Enrollment", msg)
            self.load_student_current_courses_table()
            self.load_available_subjects_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Enrollment", msg)

    def remove_selected_course(self):
        if self.current_student is None:
            QtWidgets.QMessageBox.warning(
                self, "Remove Course", "Please submit a valid Student ID first."
            )
            return

        table = self.StudentCourseTable
        selected_section = None

        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_section = self.current_section_map.get(row)
                break

        if not selected_section:
            QtWidgets.QMessageBox.warning(self, "Remove Course", "Please select a course to remove.")
            return

        try:
            ok, msg = self.admin_obj.remove_subject(
                selected_section,
                str(self.current_student.id).strip()
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Remove Course Error",
                f"Unexpected error while removing {selected_section}:\n{e}",
            )
            return

        if ok:
            QtWidgets.QMessageBox.information(self, "Remove Course", msg)
            self.load_student_current_courses_table()
            self.load_available_subjects_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Remove Course", msg)
 
    # =========================================================
    # TAB 3 — Expand capacity
    # =========================================================

    def handle_tab3_capacity_change(self):
        section = self.Tab3_Section_Code.text().strip()
        new_capacity = self.Tab3_Capacity.text().strip()

        if not section or not new_capacity:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        if not new_capacity.isdigit():
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Capacity must be an integer.")
            return

        # Use the existing admin object (created from login)
        admin_obj = self.admin_obj

        message = admin_obj.expand_capacity(section, new_capacity)

        QtWidgets.QMessageBox.information(self, "Capacity Update", message)

        self.load_capacity_table()

        self.Tab3_Section_Code.clear()
        self.Tab3_Capacity.clear()

    def load_capacity_table(self):
        from classses2 import courses_db

        row = courses_db.execute(
            "SELECT course_code, section, capacity FROM Courses",
            fetchall=True
        )

        self.CapacityTable.setRowCount(0)
        self.CapacityTable.setColumnCount(3)
        self.CapacityTable.setHorizontalHeaderLabels(
            ["Course Code", "Section ID", "Capacity"]
        )

        if not row:
            return

        for r_index, (code, section, cap) in enumerate(row):
            self.CapacityTable.insertRow(r_index)

            item_code = QtWidgets.QTableWidgetItem(str(code))
            item_sec = QtWidgets.QTableWidgetItem(str(section))
            item_cap = QtWidgets.QTableWidgetItem(str(cap))

            # 🔹 CENTER the text
            item_code.setTextAlignment(QtCore.Qt.AlignCenter)
            item_sec.setTextAlignment(QtCore.Qt.AlignCenter)
            item_cap.setTextAlignment(QtCore.Qt.AlignCenter)

            self.CapacityTable.setItem(r_index, 0, item_code)
            self.CapacityTable.setItem(r_index, 1, item_sec)
            self.CapacityTable.setItem(r_index, 2, item_cap)
        header = self.CapacityTable.horizontalHeader()
        for col in range(self.CapacityTable.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    # =========================================================
    # TAB 4 — Grading
    # =========================================================

    def handle_tab4_grading(self):
        student_id = self.Tab4_Student_ID.text().strip()
        course_code = self.Tab4_Course_code.text().strip()
        grade_value = self.Tab4_Course_code_2.text().strip()

        # Validate fields
        if not student_id or not course_code or not grade_value:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        if not student_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Error", "Student ID must be numeric.")
            return

        # Grade must be numeric (0–100)
        try:
            grade_float = float(grade_value)
            if grade_float < 0 or grade_float > 100:
                QtWidgets.QMessageBox.warning(self, "Error", "Grade must be between 0 and 100.")
                return
        except:
            QtWidgets.QMessageBox.warning(self, "Error", "Grade must be a number.")
            return

        # Use the existing admin object (NEVER create admin() again)
        admin_obj = self.admin_obj

        # Call backend function
        message = admin_obj.add_grade(student_id, course_code, grade_float)

        # Show backend message
        QtWidgets.QMessageBox.information(self, "Grade Update", message)

        # Refresh table
        self.load_tab4_grade_table()

        # Clear input fields
        self.Tab4_Student_ID.clear()
        self.Tab4_Course_code.clear()
        self.Tab4_Course_code_2.clear()

    def load_tab4_grade_table(self):
        from classses2 import users_db, courses_db

        rows = users_db.execute(
            "SELECT student_id, course, Letter_grade FROM grades",
            fetchall=True
        )

        table = self.StudentGradeTable_4
        table.setRowCount(0)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(
            ["Student ID", "Course ID", "Course Name", "Course Grade"]
        )

        if not rows:
            return

        for r_index, (student_id, course_code, letter_grade) in enumerate(rows):

            # Fetch course name
            cname = courses_db.execute(
                "SELECT course_name FROM Courses WHERE course_code = ?",
                (course_code,),
                fetchone=True
            )
            course_name = cname[0] if cname else "Unknown"

            table.insertRow(r_index)

            # Create table items
            item_stu = QtWidgets.QTableWidgetItem(str(student_id))
            item_code = QtWidgets.QTableWidgetItem(course_code)
            item_name = QtWidgets.QTableWidgetItem(course_name)
            item_grade = QtWidgets.QTableWidgetItem(letter_grade)

            # Center alignment
            for item in (item_stu, item_code, item_name, item_grade):
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            # Set items
            table.setItem(r_index, 0, item_stu)
            table.setItem(r_index, 1, item_code)
            table.setItem(r_index, 2, item_name)
            table.setItem(r_index, 3, item_grade)

        # Make ALL columns stretch
        header = table.horizontalHeader()
        for col in range(table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        # Disable editing
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
