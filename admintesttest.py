from operator import index
import os
import sqlite3
import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QShortcut,QMessageBox,QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from classses2 import admin, section, student       
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

def generate_start_times():
    times = [None]
    hour = 8
    minute = 0

    # STOP BEFORE reaching 17:00
    while True:
        current = hour * 60 + minute
        if current >= 17 * 60:  # 17:00
            break

        times.append(f"{hour}:{minute:02d}")

        minute += 5
        if minute >= 60:
            minute = 0
            hour += 1

    return times


def generate_end_times():
    times = [None]
    hour = 8
    minute = 5  # OFFSET start at 8:05

    # CONTINUE UNTIL EXACTLY 17:00
    while True:
        current = hour * 60 + minute
        times.append(f"{hour}:{minute:02d}")

        if current >= 17 * 60:  # STOP exactly at 17:00
            break

        minute += 5
        if minute >= 60:
            minute = 0
            hour += 1

    return times




class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, admin_id, admin_name):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Admin_Window.ui")
        uic.loadUi(ui_path, self)
        self.Tab4_SearchBar.textChanged.connect(self.filter_tab4_table)
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

        start_times = generate_start_times()
        end_times = generate_end_times()

        self.Section_StartTime_Combo.clear()
        self.Section_StartTime_Combo.addItems(start_times)

        self.Section_EndTime_Combo.clear()
        self.Section_EndTime_Combo.addItems(end_times)
        self.map_major_to_plane = {
            "Electrical communication and electronics engineering": "ECE",
            "Electrical power and machines engineering": "PM",
            "Computer engineering": "CE",
            "Biomedical engineering": "BIO"
        }

        



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
        
        # Load Tab 4 grade table initially
        self.load_tab4_grade_table()
        # Load Tab 6 tables
        self.setup_tab6_tables()

        # ---------- Connections ----------
        self.SignOutButton.clicked.connect(self.sign_out)
        # Tab 1: add/delete student
        self.Tab1_AddStudent.clicked.connect(self.tab1_add_student)
        self.Tab1_DeleteStudent.clicked.connect(self.tab1_delete_student)

        # Tab 2: submit student
        self.Tab2Submit.clicked.connect(self.handle_submit_student)

        # Tab 2: add/remove course
        self.Tab2_AddCourse.clicked.connect(self.add_selected_course)
        self.Tab2_DeleteCourse.clicked.connect(self.remove_selected_course)

        # Tab 3: Details
        self.Tab3_MajorChoice.currentIndexChanged.connect(self.update_subjects_table)
        self.Tab3_Term.currentIndexChanged.connect(self.update_subjects_table)


        self.update_subjects_table()



        #Tab 4 : Grades
        self.Tab4_Confirm.clicked.connect(self.handle_tab4_grading)

        # Tab 5: Courses Management
        self.Tab5_CourseAdd.clicked.connect(self.logic_add_course)
        self.Tab5_CourseUpdate.clicked.connect(self.logic_update_course)
        self.Tab5_PrerequistieAdd.clicked.connect(self.tab5_add_prerequisite)
        self.Tab5_PrerequistieRemove.clicked.connect(self.tab5_remove_prerequisite)
        self.Tab5_SectionAdd.clicked.connect(self.logic_add_section)
        self.Tab5_SectionUpdate.clicked.connect(self.logic_update_section)
        self.Tab5_SectionRemove.clicked.connect(self.logic_remove_section)

        self.setup_tab6_tables()
        
        # Connect Signals
        self.Tab6_Major_combobox.currentIndexChanged.connect(self.refresh_tab6)
        self.Tab6_Term.currentIndexChanged.connect(self.refresh_tab6)
        self.Tab6_AddPlan.clicked.connect(self.add_course_to_plan)
        self.Tab6_DeletePlan.clicked.connect(self.remove_course_from_plan)

        # Initial Load
        self.refresh_tab6()




    # =========================================================
    # General 
    # =========================================================
    def sign_out(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Sign Out")
        msg.setText("Are you sure you want to sign out?")
        msg.setIcon(QtWidgets.QMessageBox.Question)

        yes_button = msg.addButton("Yes", QtWidgets.QMessageBox.YesRole)
        cancel_button = msg.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)

        msg.exec_()

        if msg.clickedButton() == yes_button:
            self.close()          # close admin window
            self.login = LoginWindow()  # return to login
            self.login.show()
    
    def filter_tab4_table(self):
        text = self.Tab4_SearchBar.text().strip().lower()

        table = self.StudentGradeTable_4
        row_count = table.rowCount()

        if text == "":
            # Show all rows when search is empty
            for row in range(row_count):
                table.setRowHidden(row, False)
            return

        for row in range(row_count):
            match_found = False

            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and text in item.text().lower():
                    match_found = True
                    break

            table.setRowHidden(row, not match_found)


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
        

        id_text = self.Tab2_StudentID.text().strip()
        if not id_text.isdigit():
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a valid numeric student ID.")
            self.clear_enrollment_tables()
            self.current_student = None
            return

        sid = int(id_text)
        stu = student(id=sid)

        if not stu.is_student():
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a valid numeric student ID.")
            self.Tab2_StudentID.clear()
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
            QMessageBox.warning(self, "Unavailable", str(schedule))
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
    # TAB 3 — Subject details 
    # =========================================================

    def update_subjects_table(self):
        # --- TABLE FORMATTING ---
        self.Subjects_details.verticalHeader().setVisible(False)
        self.Subjects_details.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Subjects_details.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.Subjects_details.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Subjects_details.setSelectionBehavior(QAbstractItemView.SelectRows)
        # ------------------------

        # 1. Get Inputs
        selected_major = self.Tab3_MajorChoice.currentText().strip()
        selected_term = self.Tab3_Term.currentText().strip()

        # Reset table
        self.Subjects_details.setRowCount(0)
        
        # NOTE: Your new SQL query returns 6 items (including 'time'), so I increased column count to 6
        self.Subjects_details.setColumnCount(6)
        self.Subjects_details.setHorizontalHeaderLabels(["Course Code", "Section ID", "Capacity", "Instructor", "Credit", "Time"])

        if not selected_term.isdigit():
            return

        # 2. Call your NEW function
        # We pass the full major name directly because your new code handles the mapping
        rows = admin.get_table_data_optimized(None, selected_major, int(selected_term))
        
        # 3. Fill the table
        if rows:
            for row_data in rows:
                row_position = self.Subjects_details.rowCount()
                self.Subjects_details.insertRow(row_position)
                
                # row_data is: (course_code, section, capacity, instructor, credit, time)
                self.Subjects_details.setItem(row_position, 0, QTableWidgetItem(str(row_data[0])))
                self.Subjects_details.setItem(row_position, 1, QTableWidgetItem(str(row_data[1])))
                self.Subjects_details.setItem(row_position, 2, QTableWidgetItem(str(row_data[2])))
                self.Subjects_details.setItem(row_position, 3, QTableWidgetItem(str(row_data[3])))
                self.Subjects_details.setItem(row_position, 4, QTableWidgetItem(str(row_data[4])))
                
                # I added this since your new query fetches 'time' as the 6th item
                self.Subjects_details.setItem(row_position, 5, QTableWidgetItem(str(row_data[5])))
                
                # Optional: Center the items
                for i in range(6):
                    self.Subjects_details.item(row_position, i).setTextAlignment(Qt.AlignCenter)


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
   
    # =========================================================
    # TAB 5 — Courses Management
    # =========================================================
    # ---------------------- ADD COURSE ----------------------
    def logic_add_course(self):

        # 1. Retrieve text from inputs
        code = self.Tab5_Course_code.text().strip()
        name = self.Tab5_Course_name.text().strip()
        credit = self.Tab5_Credit.text().strip()
        section = self.Tab5_section.text().strip()
        term = self.Tab5_term.text().strip()
        prereq = self.Tab5_prerequisite.text().strip()

        # 2. Strict Validation: Ensure NO field is empty
        if not code or not name or not credit or not section or not term or not prereq:
            QMessageBox.warning(self, "Missing Data", "For adding a course, all fields must be entered.")
            return

        # 3. Call Backend Function
        # The backend expects: (course_code, course_name, credit, sections, term, prerequisites)
        success, message = self.admin_obj.rewrite_add_course(
            course_code=code,
            course_name=name,
            credit=credit,
            sections=section,
            term=term,
            prerequisites=prereq
        )

        # 4. Show Result
        if success:
            QMessageBox.information(self, "Success", message)
            # Optional: Clear fields after successful add
            # self.Tab5_Course_code.clear()
            # self.Tab5_Course_name.clear()
            # self.Tab5_Credit.clear()
            # self.Tab5_section.clear()
            # self.Tab5_term.clear()
            # self.Tab5_prerequisite.clear()
        else:
            QMessageBox.warning(self, "Error", message)

    def logic_update_course(self):
   
        # 1. Retrieve text
        code = self.Tab5_Course_code.text().strip()
        name = self.Tab5_Course_name.text().strip()
        credit = self.Tab5_Credit.text().strip()
        section = self.Tab5_section.text().strip()
        term = self.Tab5_term.text().strip()
        prereq = self.Tab5_prerequisite.text().strip()

        # 2. Validation: Course Code is mandatory
        if not code:
            QMessageBox.warning(self, "Missing Data", "Please enter the Course Code to update.")
            return

        # 3. Prepare Data for Backend
        # If a field is empty string "", convert it to None so the backend knows not to update it.
        name_arg = name if name else None
        credit_arg = credit if credit else None
        section_arg = section if section else None
        term_arg = term if term else None
        prereq_arg = prereq if prereq else None

        # 4. Call Backend Function
        success, message = self.admin_obj.rewrite_update_course(
            course_code=code,
            course_name=name_arg,
            credit=credit_arg,
            sections=section_arg,
            term=term_arg,
            prerequisites=prereq_arg
        )

        # 5. Show Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)


    # ---------------------- ADD PREREQUISITE ----------------------
    def tab5_add_prerequisite(self):
        code = self.Tab5_Prerequistie_CourseCode.text().strip()
        prereq = self.Tab5_PrerequistieCode.text().strip()

        if not code or not prereq:
            return QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")

        ok, msg = self.admin_obj.add_prerequisite_to_course(code, prereq)

        if ok:
            QtWidgets.QMessageBox.information(self, "Add Prerequisite", msg)
        else:
            QtWidgets.QMessageBox.warning(self, "Add Prerequisite", msg)


    # ---------------------- REMOVE PREREQUISITE ----------------------
    def tab5_remove_prerequisite(self):
        code = self.Tab5_Prerequistie_CourseCode.text().strip()
        prereq = self.Tab5_PrerequistieCode.text().strip()

        if not code or not prereq:
            return QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")

        ok, msg = self.admin_obj.remove_prerequisite_from_course(code, prereq)

        if ok:
            QtWidgets.QMessageBox.information(self, "Remove Prerequisite", msg)
        else:
            QtWidgets.QMessageBox.warning(self, "Remove Prerequisite", msg)


    # ---------------------- ADD SECTION ----------------------
    def logic_add_section(self):
    # 1. Retrieve Data
        start_time = self.Section_StartTime_Combo.currentText()
        end_time = self.Section_EndTime_Combo.currentText()
        day = self.Section_Day_Combo.currentText()
        course_code = self.Tab5_Section_CourseCord.text().strip()
        section_name = self.Tab5_Section_SectionName.text().strip()
        capacity = self.Tab5_Section_Capacity.text().strip()
        instructor_id = self.Tab5_Section_Instructor.text().strip()

        # 2. Strict Validation: Ensure NO field is empty
        # Note: For Comboboxes, ensure they aren't empty (assuming they have values selected)
        if not (start_time and end_time and day and course_code and section_name and capacity and instructor_id):
            QMessageBox.warning(self, "Missing Data", "For adding a section, ALL fields must be filled.")
            return

        # 3. Call Backend
        # Backend arg order: course_code, section_name, instructor_id, capacity, start_time, end_time, day
        success, message = self.admin_obj.rewrite_add_section(
            course_code=course_code,
            section_name=section_name,
            instructor_id=instructor_id,
            capacity=capacity,
            start_time=start_time,
            end_time=end_time,
            day=day
        )

        # 4. Show Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def logic_update_section(self):
       
        # 1. Retrieve Data
        course_code = self.Tab5_Section_CourseCord.text().strip()
        section_name = self.Tab5_Section_SectionName.text().strip()
        
        # Optional fields
        capacity = self.Tab5_Section_Capacity.text().strip()
        instructor_id = self.Tab5_Section_Instructor.text().strip()
        start_time = self.Section_StartTime_Combo.currentText()
        end_time = self.Section_EndTime_Combo.currentText()
        day = self.Section_Day_Combo.currentText()

        # 2. Validation: Mandatory fields
        if not course_code or not section_name:
            QMessageBox.warning(self, "Missing Data", "Course Code and Section Name are required for updates.")
            return

        # 3. Prepare Data (Convert empty strings to None)
        cap_arg = capacity if capacity else None
        inst_arg = instructor_id if instructor_id else None
        
        # For time, if the combobox is empty or not selected, pass None.
        # Note: If your combo boxes always have a value (like "08:00"), this will pass the string.
        # If the user intentionally wants to NOT update time, they should ideally not touch them, 
        # but strictly speaking, Comboboxes usually always have a value unless you added a blank item.
        # If you have a blank item at index 0, check `if start_time == "": start_arg = None`
        start_arg = start_time if start_time else None
        end_arg = end_time if end_time else None
        day_arg = day if day else None

        # 4. Call Backend
        success, message = self.admin_obj.rewrite_update_section(
            course_code=course_code,
            section_name=section_name,
            instructor_id=inst_arg,
            capacity=cap_arg,
            start_time=start_arg,
            end_time=end_arg,
            day=day_arg
        )

        # 5. Show Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def logic_remove_section(self):
        # 1. Retrieve Data
        section_name = self.Tab5_Section_SectionName.text().strip()

        # 2. Validation
        if not section_name:
            QMessageBox.warning(self, "Missing Data", "Please enter the Section Name to remove.")
            return

        # 3. Call Backend
        # Note: backend remove_section only takes section_name
        success, message = self.admin_obj.remove_section(section_name)

        # 4. Show Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    ###############################################
    # TAB 6 — COURSE PLAN MANAGEMENT
    ###############################################

    def setup_tab6_tables(self):
        for table in (self.Tab6_CurrentPlan_table, self.Tab6_NoPlan_table):
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(
                ["Code", "Course Name", "Credit", "Term", "Prerequisites"]
            )
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def refresh_tab6(self):
        major = self.Tab6_Major_combobox.currentText()
        term_text = self.Tab6_Term.currentText()

        try:
            not_in = self.admin_obj.courses_not_in_the_plane(major) or {}
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading 'Not in plan': {e}")
            not_in = {}

        try:
            in_plan = self.admin_obj.display_subjects_by_major_plan(major) or {}
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading 'Current plan': {e}")
            in_plan = {}

        if term_text and term_text != "All":
            try:
                selected_term = str(int(term_text))
                filtered_in_plan = {
                    code: info
                    for code, info in in_plan.items()
                    if str(info.get("terms", "")).strip() == selected_term
                }
            except Exception:
                filtered_in_plan = in_plan
        else:
            filtered_in_plan = in_plan

        self._fill_tab6_table(self.Tab6_NoPlan_table, not_in)
        self._fill_tab6_table(self.Tab6_CurrentPlan_table, filtered_in_plan)

    def _fill_tab6_table(self, table, data_dict):
        rows = list(data_dict.items())
        table.setRowCount(len(rows))

        for r, (code, info) in enumerate(rows):
            item_code = QTableWidgetItem(code)
            item_name = QTableWidgetItem(str(info.get("course_name", "")))
            item_credit = QTableWidgetItem(str(info.get("credit", "")))
            item_term = QTableWidgetItem(str(info.get("terms", "")))
            item_prereq = QTableWidgetItem(str(info.get("prerequisites", "")))

            for item in (item_code, item_name, item_credit, item_term, item_prereq):
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            table.setItem(r, 0, item_code)
            table.setItem(r, 1, item_name)
            table.setItem(r, 2, item_credit)
            table.setItem(r, 3, item_term)
            table.setItem(r, 4, item_prereq)

        table.resizeColumnsToContents()

    # def add_course_to_plan(self):
    #     row = self.Tab6_NoPlan_table.currentRow()
    #     if row < 0:
    #         QMessageBox.warning(self, "Add Course", "Please select a course from 'Not in plan'.")
    #         return

    #     course_code = self.Tab6_NoPlan_table.item(row, 0).text()
    #     major = self.Tab6_Major_combobox.currentText()

    #     try:
    #         ok, msg = self.admin_obj.add_course_to_plane(course_code, major)
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Error adding course: {e}")
    #         return

    #     if ok:
    #         QMessageBox.information(self, "Add Course", str(msg))
    #         self.refresh_tab6()
    #     else:
    #         QMessageBox.warning(self, "Add Course", str(msg))
#_____________________________________________________________________________________________________________________________________________________
    def add_course_to_plan(self):
        

        try:
            row = self.Tab6_NoPlan_table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "Add Course",
                                    "Please select a course from 'Not in plan'.")
                return

            item = self.Tab6_NoPlan_table.item(row, 0)
            if item is None:
                QMessageBox.warning(self, "Add Course",
                                    "Selected row has no course code.")
                return

            course_code = item.text().strip()
            if not course_code:
                QMessageBox.warning(self, "Add Course",
                                    "Course code is empty.")
                return

            major = self.Tab6_Major_combobox.currentText()

            ok, msg = self.admin_obj.add_course_to_plane(course_code, major)

            if ok:
                QMessageBox.information(self, "Add Course", str(msg))
                self.refresh_tab6()
            else:
                QMessageBox.warning(self, "Add Course", str(msg))

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            QMessageBox.critical(self, "Unexpected Error",
                                f"{e}\n\n{tb}")


  



    def remove_course_from_plan(self):
        row = self.Tab6_CurrentPlan_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Delete Course", "Please select a course from 'Current plan'.")
            return

        course_code = self.Tab6_CurrentPlan_table.item(row, 0).text()
        major = self.Tab6_Major_combobox.currentText()

        try:
            ok, msg = self.admin_obj.delete_course_from_plane(course_code, major)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error deleting course: {e}")
            return

        if ok:
            QMessageBox.information(self, "Delete Course", str(msg))
            self.refresh_tab6()
        else:
            QMessageBox.warning(self, "Delete Course", str(msg))


    







if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
