import sys
import os
import sqlite3
import bcrypt
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence
from classses2 import Database,  student, admin, user, subject, section, instructor, enforce_strong_password, signup


# _____________________________________________________________
#                         Login WINDOW
# _____________________________________________________________
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Login.ui")
        uic.loadUi(ui_path, self)
        self.setFixedWidth(552)
        self.setFixedHeight(650)

        self.loginButton.clicked.connect(self.loginfunction)
        self.SignUpButton.clicked.connect(self.signupfunction)

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

    def check_admin(self, uni_id, password):
        try:
            a = admin(id=uni_id)

            if not a.is_admin():
                return None
            
            if not a.correct_password(password):
                return None
            name = a.username


            return (uni_id, name)

        except:
            return None

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
        admin_data = self.check_admin(UniID, password)
        if admin_data:
            self.openAdminWindow()
            return

        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid ID or Password.")

    def openStudentWindow(self, sid, sname, smajor):
        self.hide()
        self.main_window = StudentWindow(sid, sname, smajor)
        self.main_window.show()
        
    def openAdminWindow(self):
        self.hide()
        self.main_window = AdminWindow()
        self.main_window.show()

    def signupfunction(self):
        self.hide()
        self.signup_window = self.SignUpWindow()
        self.signup_window.show()
        self.signup_window.destroyed.connect(self.show)


    # _____________________________________________________________
    #                        SIGN UP WINDOW
    # _____________________________________________________________
    class SignUpWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            ui_path = os.path.join(os.path.dirname(__file__), "SignUp.ui")
            uic.loadUi(ui_path, self)

            self.setFixedWidth(585)
            self.setFixedHeight(820)

            self.checkBox_show1.stateChanged.connect(self.toggle_password)
            self.BackButton.clicked.connect(self.go_back)

            # CONNECT SIGNUP BUTTON
            self.CreateButton.clicked.connect(self.process_signup)

        def toggle_password(self):
            if self.checkBox_show1.isChecked():
                self.NewPassLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
                self.ConfirmPassLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            else:
                self.NewPassLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
                self.ConfirmPassLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        def go_back(self):
                self.close()
                self.login = LoginWindow()
                self.login.show()

        # _____________________________________________________________
        #                SIGN UP PROCESS USING signup()
        # _____________________________________________________________

        def process_signup(self):
            FN = self.FirstNameLineEdit.text().strip()
            LN = self.LastNameLineEdit.text().strip()
            new_pass = self.NewPassLineEdit.text().strip()
            confirm_pass = self.ConfirmPassLineEdit.text().strip()

            MAJOR_MAP = {
                "Power & Machines" : "Electrical power and machines engineering",
                "Communication" : "Electrical communication and electronics engineering",
                "Computer" : "Electrical computer engineering",
                "Biomedical" : "Electrical biomedical engineering"
            }


            # ========== CHECK EMPTY FIELDS ==========
            if not FN or not LN or not new_pass or not confirm_pass:
                QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
                return

            # ========== CHECK PASSWORD MATCH ==========
            if new_pass != confirm_pass:
                QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match.")
                return

            # ========== CHECK PASSWORD STRENGTH ==========
            from classses2 import enforce_strong_password, signup

            if not enforce_strong_password(new_pass):
                QtWidgets.QMessageBox.warning(
                    self,
                    "Weak Password",
                    "Password must:\n"
                    "- Have 1 special character\n"
                    "- Be at least 8 characters\n"
                    "- Contain an uppercase letter\n"
                    "- Not contain 3 consecutive numbers"
                )
                return
            

            # ===== GET SELECTED MAJOR =====
            selected_major_ui = self.MajorComboBox.currentText()
            if selected_major_ui not in MAJOR_MAP:
                QtWidgets.QMessageBox.warning(self, "Error", "Please select a valid major.")
                return
            
            selected_major = MAJOR_MAP[selected_major_ui]

            
            # ========== PERFORM SIGNUP ==========
            try:
                lines = signup(FN, LN, new_pass, selected_major)
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "Account created successfully! You may now log in."
                    f"\nYour University ID is: {lines.return_id()}"
                )
                self.close()
                self.login = LoginWindow()
                self.login.show()

            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Signup Failed",
                    f"An error occurred:\n{e}"
                )




# _____________________________________________________________
#                        STUDENT WINDOW
# _____________________________________________________________
class StudentWindow(QtWidgets.QMainWindow):
    def __init__(self, sid, sname, smajor):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Student_Window.ui")
        uic.loadUi(ui_path, self)

        self.setFixedWidth(1248)    
        self.setFixedHeight(975)

        self.student_id = sid
        self.student_name = sname
        self.student_major = smajor
        self.infoTable.verticalHeader().setVisible(False)
        self.AddButton.clicked.connect(self.add_selected_course)
        self.RemoveButton.clicked.connect(self.remove_selected_course)
        self.AcademicRadio.toggled.connect(self.switch_schedule_view)
        self.WeeklyRadio.toggled.connect(self.switch_schedule_view)
        self.AcademicRadio.setChecked(True)
        self.WeeklySchTable.hide()
        self.SignOutButton.clicked.connect(self.sign_out)
        self.ChangePassButton.clicked.connect(self.open_change_pass)

        
      
        # Call the GPA function from classses2.py
        self.student_obj = student(self.student_id)
        gpa_value = self.student_obj.calculate_GPA()
        self.update_GPA_table(gpa_value)


        # Set welcome text
        self.welcomeLabel.setText(f"Welcome, {self.student_name}")
        self.tabWidget.setCurrentIndex(1)
        
        # General table setup
        self.setup_current_courses_table()
        self.setup_current_schedule_table()
        # Load student info into table
        self.load_info_table()
        # Load transcript tables
        self.load_transcript_tables()
        # Load current schedule
        self.load_current_schedule()
        # Load weekly schedule
        self.load_weekly_schedule()
        # Load available courses
        self.load_available_courses()
        # Load current courses
        self.load_current_courses_table()
        # Load total credit
        self.load_total_credit()
        # Setup weekly schedule header
        self.setup_weekly_header()
        # Load student information tab
        self.load_student_information()


    # __________General__________
    def setup_current_courses_table(self):
        table = self.Current_CoursesTable

        # Always start from a clean, empty table
        table.clear()
        table.setRowCount(0)

        # 6 columns: checkbox + course info
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["", "Course Code", "Instructor", "Section", "Time", "Credit"]
        )

        # Hide row numbers
        table.verticalHeader().setVisible(False)

        # Column sizes (same as after you add/remove a subject)
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)   # Section
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)   # Credit
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        # Stretch the other columns
        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def setup_current_schedule_table(self):
        table = self.CurrentSchTable

        # Completely reset the table look
        table.clear()
        table.setRowCount(0)

        # 5 columns: Code, Name, Section, Days, Time
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Course Code", "Course Name", "Section", "Days", "Time"
        ])

        table.verticalHeader().setVisible(False)

        # Stretch nicely (same layout you want)
        table.horizontalHeader().setStretchLastSection(True)

        # Course Name column should be wider
        table.setColumnWidth(1, 350)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)

        # Other columns stretch
        for col in [0, 2, 3, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

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

    def refresh_all_tables(self):
        self.load_info_table()
        self.load_transcript_tables()
        self.load_current_schedule()
        self.load_available_courses()
        self.load_current_courses_table()
        self.load_weekly_schedule()
        self.load_total_credit() 
   
    def open_change_pass(self):
        self.change_pass_window = self.ChangePassWindow(self.student_id)
        self.change_pass_window.show()

    # __________Transcript Tab__________
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
    
    # __________Schedule Tab__________
    def load_current_schedule(self):

        table = self.CurrentSchTable
        table.clearContents()


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
        self.CurrentSchTable.horizontalHeader().setStretchLastSection(True)
        self.CurrentSchTable.resizeColumnToContents(1)
        table.setColumnWidth(1, 350)
        table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        
    def switch_schedule_view(self):
        if self.AcademicRadio.isChecked():
            self.CurrentSchTable.show()
            self.WeeklySchTable.hide()
        else:
            self.CurrentSchTable.hide()
            self.WeeklySchTable.show()

    def load_weekly_schedule(self):
        table = self.WeeklySchTable
        table.clear()
        table.resizeRowsToContents()


        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        table.setColumnCount(len(days) + 1)
        table.setHorizontalHeaderLabels(["Time"] + days)
        table.verticalHeader().setVisible(False)

        # Chronological master list (start at 8:00 always)
        ALL_TIME_SLOTS = [
            "8:00-8:50", "8:00-9:15",
            "9:00-9:50", "9:00-9:15",
            "9:30-10:45",
            "10:00-10:50",
            "11:00-11:50", "11:00-12:15", "11:00-12:50",
            "1:00-1:50", "1:00-2:15",
            "2:00-4:50",
            "5:00-5:50",
            "6:00-6:50",
            "7:00-7:50"
        ]

        schedule = self.student_obj.view_enrolled_subjects()

        if isinstance(schedule, str):
            table.setRowCount(0)
            return

        time_slots_found = set()
        parsed_subjects = []

        # Parse schedule
        for section, (course_code, course_name, time_days,
                    credit, section_name, instructor) in schedule.items():

            # "9:00-9:50 , S T U"
            time_part, days_part = time_days.split(",")
            time_range = time_part.strip()
            letters = days_part.strip().split()

            # Map letters → full day names
            map_days = {
                "S": "Sunday",
                "M": "Monday",
                "T": "Tuesday",
                "W": "Wednesday",
                "U": "Thursday"
            }
            full_days = [map_days[d] for d in letters]

            time_slots_found.add(time_range)
            parsed_subjects.append((course_code, section, full_days, time_range))

        # Build CHRONOLOGICAL time order
        time_slots = []
        for t in ALL_TIME_SLOTS:
            if any(t in slot for slot in time_slots_found):
                time_slots.append(t)

        # Row count
        table.setRowCount(len(time_slots))

        # Set time labels
        for r, t in enumerate(time_slots):
            item = QtWidgets.QTableWidgetItem(t)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(r, 0, item)

        # Insert subjects in correct cells
        for course_code, section, full_days, time_range in parsed_subjects:
            row = 0
            for i, slot in enumerate(time_slots):
                if time_range.startswith(slot.split("-")[0]):
                    row = i
                    break

            for d in full_days:
                col = days.index(d) + 1

                text = f"{course_code}\n({section})"
                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackground(QtGui.QColor("#00334e"))
                item.setForeground(QtGui.QColor("white"))

                table.setItem(row, col, item)

        # Stretch columns
        for c in range(table.columnCount()):
            table.horizontalHeader().setSectionResizeMode(c, QtWidgets.QHeaderView.Stretch)
        
        # Allow wrapping inside cells
        self.WeeklySchTable.setWordWrap(True)
        
        # Automatically resize all rows to fit text (multiline)
        self.WeeklySchTable.resizeRowsToContents()
        
        # Minimum height so blocks look clean
        for r in range(self.WeeklySchTable.rowCount()):
            self.WeeklySchTable.setRowHeight(r, max(self.WeeklySchTable.rowHeight(r), 45))

    def load_total_credit(self):
            table = self.TotalCreditTable

            total = 0
            schedule = self.student_obj.view_enrolled_subjects()
            if isinstance(schedule, dict):
                for sec, (course_code, course_name, time_days,
                        section_name, credit, instructor) in schedule.items():
                    total += credit

            # Configure header and structure
            table.setColumnCount(2)
            table.setRowCount(1)
            table.setHorizontalHeaderLabels(["Total Credit", str(total)])
            table.verticalHeader().setVisible(False)

            # Stretch layout
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def setup_weekly_header(self):
        table = self.WeeklySchTable

        # Only headers, no rows
        table.setRowCount(0)

        # Set 6 columns
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Time", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"
        ])

        # Stretch all columns to fill full width
        header = table.horizontalHeader()
        for col in range(table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

        # Disable all user editing
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setFocusPolicy(QtCore.Qt.NoFocus)

        # Hide vertical rows (since there are none)
        table.verticalHeader().setVisible(False)

    # __________Add/Remove Tab__________
    def load_available_courses(self):
        table = self.Available_CoursesTable
        table.clearContents()


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
        table.clearContents()



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
                    section_name,credit, instructor) in schedule.items():

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

        # Use section.enroll_student_in_section to get (ok, msg)
        try:
            self.student_obj = student(self.student_id)  # Refresh student object
            ok, msg = self.student_obj.enroll_subject(selected_section)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Enrollment Error",
                f"Unexpected error while enrolling in {selected_section}:\n{e}"
            )
            return

        if ok:
            QtWidgets.QMessageBox.information(self, "Enrollment", msg)
            self.refresh_all_tables()
        else:
            QtWidgets.QMessageBox.warning(self, "Enrollment", msg)

    def remove_selected_course(self):
        table = self.Current_CoursesTable

        selected_section = None

        # Find which row is checked
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_section = self.current_section_map[row]   # section code (e.g. "AW")
                break

        if not selected_section:
            QtWidgets.QMessageBox.warning(self, "Remove Course", "Please select a course to remove.")
            return

        # Use section.remove_student_from_section to get (ok, msg)
        try:
            self.student_obj = student(self.student_id)  # Refresh student object
            ok, msg = self.student_obj.drop_subject(selected_section)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Remove Course Error",
                f"Unexpected error while removing {selected_section}:\n{e}"
            )
            return

        if ok:
            QtWidgets.QMessageBox.information(self, "Remove Course", msg)
            self.refresh_all_tables()
        else:
            QtWidgets.QMessageBox.warning(self, "Remove Course", msg)
  
    # __________Student Information Tab__________
    def load_student_information(self):

        # student object (comes from classses2.py)
        s = self.student_obj

        self.sinfoTable.setColumnCount(4)
        self.sinfoTable.setRowCount(1)
        self.sinfoTable.setHorizontalHeaderLabels(["Name", "ID", "Major","Email"])

        # Insert data
        self.sinfoTable.setItem(0, 0, QtWidgets.QTableWidgetItem(self.student_name))
        self.sinfoTable.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.student_id)))
        self.sinfoTable.setItem(0, 2, QtWidgets.QTableWidgetItem(self.student_major))
        self.sinfoTable.setItem(0, 3, QtWidgets.QTableWidgetItem(s.email))

        # Adjust column widths
        self.sinfoTable.setColumnWidth(0, 180)   # Name
        self.sinfoTable.setColumnWidth(1, 180)    # ID  (smaller)
        self.sinfoTable.setColumnWidth(2, 500)   # Major (bigger)
        self.sinfoTable.setColumnWidth(3, 200)   # Email

        # Allow columns to stretch after setting min widths
        for col in range(4):
            self.sinfoTable.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)


        # Make columns stretch evenly
        self.sinfoTable.horizontalHeader().setStretchLastSection(True)
        self.sinfoTable.verticalHeader().setVisible(False)
        

        # Center align header text
        header = self.sinfoTable.horizontalHeader()
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)

        # Center align all cell text
        for col in range(4):
            self.sinfoTable.item(0, col).setTextAlignment(QtCore.Qt.AlignCenter)
            
        # ---------------- Term Table ----------------
        self.TermTable.setRowCount(1)
        self.TermTable.setColumnCount(1)
        self.TermTable.setHorizontalHeaderLabels(["Current Term"])

        # Fetch term from database
        conn = sqlite3.connect("Users.db")
        cur = conn.cursor()
        row = cur.execute("SELECT term FROM students WHERE id = ?", (s.id,)).fetchone()
        conn.close()

        term_value = row[0] if row else "?"

        item = QtWidgets.QTableWidgetItem(str(term_value))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.TermTable.setItem(0, 0, item)
        self.TermTable.verticalHeader().setVisible(False)
        self.TermTable.horizontalHeader().setStretchLastSection(True)

    # _____________________________________________________________
    #                      CHANGE PASSWORD WINDOW
    # _____________________________________________________________
    class ChangePassWindow(QtWidgets.QMainWindow):
        def __init__(self, student_id):
            super().__init__()
            ui_path = os.path.join(os.path.dirname(__file__), "ChangePass.ui")
            uic.loadUi(ui_path, self)

            self.setFixedWidth(664)
            self.setFixedHeight(705)

            # Store student ID
            self.student_id = student_id

            # Toggle password visibility
            self.checkBox_showNew.stateChanged.connect(self.toggle_password)

            # Confirm button
            self.ConfirmButton.clicked.connect(self.process_password_change)

            # ENTER key triggers confirm
            QShortcut(QKeySequence("Return"), self, self.ConfirmButton.click)
            QShortcut(QKeySequence("Enter"), self, self.ConfirmButton.click)


        def toggle_password(self):
            mode = QtWidgets.QLineEdit.Normal if self.checkBox_showNew.isChecked() else QtWidgets.QLineEdit.Password
            self.OldLineEdit.setEchoMode(mode)
            self.PasslineEditNew.setEchoMode(mode)
            self.PassLineEditConfirm.setEchoMode(mode)


        def process_password_change(self):
            old_pass = self.OldLineEdit.text().strip()
            new_pass = self.PasslineEditNew.text().strip()
            confirm_pass = self.PassLineEditConfirm.text().strip()

            # Empty fields check
            if not old_pass or not new_pass or not confirm_pass:
                QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
                return


            if enforce_strong_password(new_pass):
                # Match check
                if new_pass != confirm_pass:
                    QtWidgets.QMessageBox.warning(self, "Error", "New password and confirmation do not match.")
                    return

                # Student object
                stu = student(self.student_id)

                # Verify old password
                if not stu.correct_password(old_pass):
                    QtWidgets.QMessageBox.warning(self, "Error", "Old password is incorrect.")
                    return
                # Change password using classses2.py
                ok, msg = stu.change_password(old_pass, new_pass)

                if ok:
                    QtWidgets.QMessageBox.information(self, "Success", msg)
                    self.close()
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", msg)
            else: 
                QtWidgets.QMessageBox.warning(
                    self,
                    "Weak Password",
                    "Password must:\n"
                    "- Have 1 special character\n"
                    "- Be at least 8 characters\n"
                    "- Contain an uppercase letter\n"
                    "- Not contain 3 consecutive numbers"
                )
                return

            
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
