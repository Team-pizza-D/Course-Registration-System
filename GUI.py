import sys
import os
import sqlite3
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from classses2 import Database,  student, admin, user, subject, section, instructor



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

    # __________ DATABASE CHECKS __________

    def check_student(self, uni_id, password):
        try:
            # Create a student object using the ID
            s = student(id=uni_id)

            # Check if the ID belongs to a real student
            if not s.is_student():
                return None  # Not a student

            # Verify password using existing function in user class
            if not s.correct_password(password):
                return None  # Password wrong

            # Fetch username and major from DB
            name = s.username
            major = s.major

            return (uni_id, name, major)

        except:
            return None

    
    def check_admin(self, uni_id):
        pass

    # __________ LOGIN LOGIC __________

    def loginfunction(self):
        UniID = self.IDlineEdit.text().strip()
        password = self.PasslineEdit.text().strip()

        # Check student login using functions from classses2.py
        student_data = self.check_student(UniID, password)

        if student_data:
            sid, sname, smajor = student_data
            self.openStudentWindow(sid, sname, smajor)
            return

        # Admin login (you said you will implement it later)
        admin_data = self.check_admin(UniID)
        if admin_data:
            self.openAdminWindow()
            return

        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid ID or Password.")


    def openStudentWindow(self, sid, sname, smajor):
        self.hide()
        self.main_window = StudentWindow(sid, sname, smajor)
        self.main_window.show()
        


# _____________________________________________________________
#                        STUDENT WINDOW
# _____________________________________________________________
class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self, sid, sname, smajor):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Student_Window.ui")
        uic.loadUi(ui_path, self)

        # self.setFixedWidth(1216)
        # self.setFixedHeight(966)

        self.student_id = sid
        self.student_name = sname
        self.student_major = smajor
        self.infoTable.verticalHeader().setVisible(False)
        self.AddButton.clicked.connect(self.add_selected_course)

        
        # Call the GPA function from classses2.py
        self.student_obj = student(self.student_id)
        gpa_value = self.student_obj.calculate_GPA()
        self.update_GPA_table(gpa_value)


        # Set welcome text
        self.welcomeLabel.setText(f"Welcome, {self.student_name}")

        # Load student info into table
        self.load_info_table()
        # Load transcript tables
        self.load_transcript_tables()
        # Load current schedule
        self.load_current_schedule()
        # Load available courses
        self.load_available_courses()
        # Load current courses
        self.load_current_courses_table()
      
    def load_info_table(self):
        # Prepare table
        self.infoTable.setColumnCount(3)
        self.infoTable.setRowCount(1)
        self.infoTable.setHorizontalHeaderLabels(["Name", "ID", "Major"])

        # Insert data
        self.infoTable.setItem(0, 0, QtWidgets.QTableWidgetItem(self.student_name))
        self.infoTable.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.student_id)))
        self.infoTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.student_major))

        # Make columns stretch evenly
        self.infoTable.horizontalHeader().setStretchLastSection(True)
        self.infoTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Center align header text
        header = self.infoTable.horizontalHeader()
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)

        # Center align all cell text
        for col in range(3):
            self.infoTable.item(0, col).setTextAlignment(QtCore.Qt.AlignCenter)

    def update_GPA_table(self, gpa):
        self.GpaTable.setRowCount(1)
        self.GpaTable.setColumnCount(1)
        self.GpaTable.setHorizontalHeaderLabels(["GPA"])

        item = QtWidgets.QTableWidgetItem(str(gpa))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.GpaTable.setItem(0, 0, item)

        # Clean look
        self.GpaTable.verticalHeader().setVisible(False)
        self.GpaTable.horizontalHeader().setStretchLastSection(True)
    
    def load_transcript_tables(self):

        # Get dictionary: { course_code : (term_number, grade) }
        transcript = self.student_obj.transcript()

        if isinstance(transcript, str):
            print(transcript)
            return

        # Organize by term
        terms_dict = {i: [] for i in range(1, 11)}

        for course_code, (term, grade) in transcript.items():
            if isinstance(term, int) and 1 <= term <= 10:
                terms_dict[term].append((course_code, grade))

        # INSERT DATA INTO EACH TABLE
        for term in range(1, 11):
            # Find table inside scrollAreaWidgetContents
            table = self.scrollAreaWidgetContents.findChild(
                QtWidgets.QTableWidget,
                f"term{term}"
            )

            if table is None:
                print(f"[Error] Table term{term} not found.")
                continue

            # Determine suffix (st, nd, rd, th)
            if term == 1:
                suffix = "st"
            elif term == 2:
                suffix = "nd"
            elif term == 3:
                suffix = "rd"
            else:
                suffix = "th"

            # Configure table
            table.clear()
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels([f"{term}{suffix} Term", "Grade"])
            table.verticalHeader().setVisible(False)

            course_list = terms_dict[term]
            table.setRowCount(len(course_list))

            # Fill rows
            for row_idx, (course_code, grade) in enumerate(course_list):
                item_course = QtWidgets.QTableWidgetItem(course_code)
                item_grade = QtWidgets.QTableWidgetItem(grade)

                # Center text
                item_course.setTextAlignment(QtCore.Qt.AlignCenter)
                item_grade.setTextAlignment(QtCore.Qt.AlignCenter)

                table.setItem(row_idx, 0, item_course)
                table.setItem(row_idx, 1, item_grade)

            # Adjust columns
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    
    def load_current_schedule(self):

        table = self.CurrentSchTable
        table.clear()

        # Updated column order
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Course Code", "Course Name", "Section", "Days", "Time"])
        table.verticalHeader().setVisible(False)

        # Load data from classes2.py
        schedule = self.student_obj.view_enrolled_subjects()

        if isinstance(schedule, str):
            table.setRowCount(0)
            return

        table.setRowCount(len(schedule))

        row = 0
        for section, (course_code, course_name, time_days, credit, section_name, instructor) in schedule.items():
            
            # Parse "9:00-9:50 , S T U"
            time_part, days_part = time_days.split(",")
            time_part = time_part.strip()
            days_part = days_part.strip()

            # Create table items
            item_code = QtWidgets.QTableWidgetItem(course_code)
            item_name = QtWidgets.QTableWidgetItem(course_name)
            item_section = QtWidgets.QTableWidgetItem(section)
            item_days = QtWidgets.QTableWidgetItem(days_part)
            item_time = QtWidgets.QTableWidgetItem(time_part)

            # Center align text
            for item in [item_code, item_name, item_section, item_days, item_time]:
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            # Insert into the table (updated order)
            table.setItem(row, 0, item_code)
            table.setItem(row, 1, item_name)
            table.setItem(row, 2, item_section)
            table.setItem(row, 3, item_days)
            table.setItem(row, 4, item_time)

            row += 1

        # Stretch columns to fit nicely
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        table.setColumnWidth(1, 350) 

    def load_available_courses(self):
        table = self.Available_CoursesTable
        table.clear()

        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["", "Course Code", "Instructor", "Section", "Time", "Credit"]
        )
        table.verticalHeader().setVisible(False)

        available = self.student_obj.view_available_subjects()

        if isinstance(available, str):
            table.setRowCount(0)
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

            # Store mapping row → section name
            self.available_section_map[row] = section

            # Fill row
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

        # Column sizes
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)  # section column
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)  # credit column
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        # Stretch rest
        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def on_available_checkbox_changed(self, state):
        table = self.Available_CoursesTable
        sender = self.sender()
        clicked_row = None

        # Find clicked row
        for row in range(table.rowCount()):
            if table.cellWidget(row, 0) == sender:
                clicked_row = row
                break

        if clicked_row is None:
            return

        # If UNCHECKED → restore everything
        if state == 0:
            self.restore_all_rows()
            return

        # CHECKED → gray all other rows
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)

            if row != clicked_row:
                checkbox.setEnabled(False)
                self.set_row_gray(row)
            else:
                checkbox.setEnabled(True)
                self.set_row_normal(row)   

    def set_row_gray(self, row):
        table = self.Available_CoursesTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("#7a7a7a"))

    def set_row_normal(self, row):
        table = self.Available_CoursesTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))  # table background
                item.setForeground(QtGui.QColor("white"))

    def restore_all_rows(self):
        table = self.Available_CoursesTable

        # Re-enable all checkboxes + restore row colors
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            checkbox.setEnabled(True)
            checkbox.setChecked(False)

            for col in range(1, table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor("#001622"))
                    item.setForeground(QtGui.QColor("white"))

    def load_current_courses_table(self):

        table = self.Current_CoursesTable
        table.clear()

        # Same header layout as Available_CoursesTable
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["", "Course Code", "Instructor", "Section", "Time", "Credit"]
        )
        table.verticalHeader().setVisible(False)

        schedule = self.student_obj.view_enrolled_subjects()

        # If function returned an error string
        if isinstance(schedule, str):
            table.setRowCount(0)
            return

        self.current_section_map = {}   # row -> section name
        table.setRowCount(len(schedule))

        row = 0
        for section, (course_code, course_name, time_days,
                    section_name, credit, instructor) in schedule.items():

            # time_days example: "9:00-9:50 , S T U"
            try:
                time_part, days_part = time_days.split(",")
                time_str = time_part.strip()
                days_str = days_part.strip()
                time_display = f"{time_str}, {days_str}"
            except ValueError:
                # fallback if format is weird
                time_display = time_days

            # --- Checkbox in column 0 ---
            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("margin-left: 8px;")

            # Connect checkbox to handler
            checkbox.stateChanged.connect(self.on_current_checkbox_changed)

            table.setCellWidget(row, 0, checkbox)


            # Map row -> section to use later with Remove button
            self.current_section_map[row] = section

            # --- Other columns ---
            items = [
                QtWidgets.QTableWidgetItem(course_code),       # col 1
                QtWidgets.QTableWidgetItem(instructor),        # col 2
                QtWidgets.QTableWidgetItem(section),           # col 3
                QtWidgets.QTableWidgetItem(time_display),      # col 4
                QtWidgets.QTableWidgetItem(str(credit)),       # col 5
            ]

            col = 1
            for item in items:
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)
                col += 1

            row += 1

        # -------- Column widths: copy from Available_CoursesTable --------
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)   # Section column
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)   # Credit column
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        # Stretch same columns as Available_CoursesTable: 1,2,4
        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def on_current_checkbox_changed(self, state):
        table = self.Current_CoursesTable
        sender = self.sender()
        clicked_row = None

        # Find which row checkbox belongs to
        for row in range(table.rowCount()):
            if table.cellWidget(row, 0) == sender:
                clicked_row = row
                break

        if clicked_row is None:
            return

        # UNCHECK → restore all rows
        if state == 0:
            self.restore_current_rows()
            return

        # CHECKED → gray out all OTHER rows
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)

            if row != clicked_row:
                checkbox.setEnabled(False)
                self.set_current_row_gray(row)
            else:
                checkbox.setEnabled(True)
                self.set_current_row_normal(row)

    def set_current_row_gray(self, row):
        table = self.Current_CoursesTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("#7a7a7a"))

    def set_current_row_normal(self, row):
        table = self.Current_CoursesTable
        for col in range(1, table.columnCount()):
            item = table.item(row, col)
            if item:
                item.setBackground(QtGui.QColor("#001622"))
                item.setForeground(QtGui.QColor("white"))

    def restore_current_rows(self):
        table = self.Current_CoursesTable

        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            checkbox.setEnabled(True)
            checkbox.setChecked(False)

            for col in range(1, table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setBackground(QtGui.QColor("#001622"))
                    item.setForeground(QtGui.QColor("white"))

    def add_selected_course(self):
        table = self.Available_CoursesTable

        selected_section = None

        # Find which row is checked
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_section = self.available_section_map[row]   # section code (e.g. "AW")
                break

        if not selected_section:
            QtWidgets.QMessageBox.warning(self, "Enrollment", "Please select a course to add.")
            return

        # --- USE enroll_subject(section_code) AND GET ok/message ---
        try:
            ok, msg = self.student_obj.enroll_subject(selected_section)
        except Exception as e:
            # In case enroll_subject fails in some unexpected way
            QtWidgets.QMessageBox.critical(
                self,
                "Enrollment Error",
                f"Unexpected error while enrolling in {selected_section}:\n{e}"
            )
            return

        # Show the exact message coming from enroll_subject
        if ok:
            # Success message from your logic
            QtWidgets.QMessageBox.information(self, "Enrollment", msg)
            # Refresh everything only if enrollment actually happened
            self.refresh_all_tables()
        else:
            # Failure / constraint message from your logic
            QtWidgets.QMessageBox.warning(self, "Enrollment", msg)

    def refresh_all_tables(self):
        self.load_info_table()
        self.load_transcript_tables()
        self.load_current_schedule()
        self.load_available_courses()
        self.load_current_courses_table()



# _____________________________________________________________
#                        ADMIN WINDOW
# _____________________________________________________________
class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Admin_Window.ui")
        uic.loadUi(ui_path, self)


# _____________________________________________________________
#                            MAIN
# _____________________________________________________________
def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
