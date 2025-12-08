from operator import index
import os
import random
import smtplib  
import sqlite3
import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QShortcut,QMessageBox,QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from classes import admin, student, user, users_db, enforce_strong_password, signup, update_password

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
        self.ForgetButton.clicked.connect(self.forget_password)

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
            admin_id, admin_name = admin_data
            self.openAdminWindow(admin_id, admin_name)
            return

        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid ID or Password.")

    def openStudentWindow(self, sid, sname, smajor):
        self.hide()
        self.main_window = StudentWindow(sid, sname, smajor)
        self.main_window.show()
        
    def openAdminWindow(self, admin_id, admin_name):
        self.hide()
        self.main_window = AdminWindow(admin_id=admin_id, admin_name=admin_name)
        self.main_window.show()

    def signupfunction(self):
        self.hide()
        self.signup_window = self.SignUpWindow()
        self.signup_window.show()
        self.signup_window.destroyed.connect(self.show)

    def forget_password(self):
        self.hide()
        self.forget_password_window = self.ForgetPassword()
        self.forget_password_window.show()
        self.forget_password_window.destroyed.connect(self.show)

    # _____________________________________________________________
    #                        ADDITIONAL WINDOWS
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

    class ForgetPassword(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            ui_path = os.path.join(os.path.dirname(__file__), "ForgetPass.ui")
            uic.loadUi(ui_path, self)

            self.setFixedWidth(577)
            self.setFixedHeight(705)

            self.BackButton.clicked.connect(self.go_back)
            self.VerifyIDButton.clicked.connect(self.verify_student_id)
            self.VerifyCodeButton.clicked.connect(self.verify_code)

            # Disable verification code until ID is validated
            self.CodeLineEdit.setEnabled(False)

        def go_back(self):
                self.close()
                self.login = LoginWindow()
                self.login.show()

        def verify_student_id(self):
            self.uni_id = self.IDLineEdit.text().strip()
            
            if not self.uni_id:
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter a University ID.")
                return
            s = user(id=self.uni_id)
            
            if not s.is_student() and not s.is_admin():
                QtWidgets.QMessageBox.warning(self, "Error", "ID not found.")
                return
            # Student exists → enable verification code field
            self.CodeLineEdit.setEnabled(True)

            QtWidgets.QMessageBox.information(
                self,
                "Success",
                "Student found. Please enter the verification code."
            )  
            self.expected_code = self.reset_password(self.uni_id)

        def verify_code(self):
            code = self.CodeLineEdit.text().strip()

            if not code:
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter the verification code.")
                return

            if code != str(self.expected_code):
                QtWidgets.QMessageBox.warning(self, "Error", "Incorrect verification code.")
                return

            # For now only display a message (you will link actual email verification later)
            if code == str(self.expected_code):
                QtWidgets.QMessageBox.information(self, "Success", "Verification code accepted.")
                self.change_pass_window = LoginWindow.ResetPassWindow(self.uni_id)
                self.change_pass_window.show()
                self.close()

        def reset_password(self, the_id):
            this_time_code = random.randint(100000,999999)
            sender_email = "pizzateamd@gmail.com"
            app_paas = "wihu xclr tdos yxxh"
            #======Getting user's email=======#
            db = sqlite3.connect("Users.db")
            cr = db.cursor()
            user_email = "viibrkk@gmail.com"  # Default email
            cr.execute("SELECT username FROM admins WHERE id = ? UNION SELECT username FROM instructors WHERE id = ? UNION SELECT username FROM students WHERE id = ?", (the_id,the_id,the_id))
            user_in_tuple = cr.fetchall()
            user_name = user_in_tuple[0][0]
            subj = "RESET YOUR PASSWORD"
            body = f"Hello {user_name}, this is an email to reset your password\nThis is your one time code: {this_time_code}, please enter it carefully\nIf you don't want to reset your password, just ignore this email"
            msgg = f"{subj}\n\n{body}"

            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(sender_email, app_paas)
            server.sendmail(sender_email, user_email, msgg)
            server.quit()
            return this_time_code

    class ResetPassWindow(QtWidgets.QMainWindow):
        def __init__(self, sid):
            super().__init__()
            ui_path = os.path.join(os.path.dirname(__file__), "ResetPass.ui")
            uic.loadUi(ui_path, self)

            self.setFixedWidth(607)
            self.setFixedHeight(648)

            self.student_id = sid
            self.checkBox_showNew10.stateChanged.connect(self.toggle_password)
            self.ChangePassButton.clicked.connect(self.change_password)

        def change_password(self):
            new_pass = self.PasslineEditNew10.text().strip()
            confirm_pass = self.PassLineEditConfirm10.text().strip()

            if not new_pass or not confirm_pass:
                QtWidgets.QMessageBox.warning(self, "Error", "All fields are required.")
                return

            if new_pass != confirm_pass:
                QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match.")
                return

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

            try:
                update_password(self.student_id, new_pass)

                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "Password changed successfully."
                )
                self.close()
                self.login = LoginWindow()
                self.login.show()

            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Error",
                    f"An error occurred:\n{e}"
                )

        def toggle_password(self):
            if self.checkBox_showNew10.isChecked():
                self.PasslineEditNew10.setEchoMode(QtWidgets.QLineEdit.Normal)
                self.PassLineEditConfirm10.setEchoMode(QtWidgets.QLineEdit.Normal)
            else:
                self.PasslineEditNew10.setEchoMode(QtWidgets.QLineEdit.Password)
                self.PassLineEditConfirm10.setEchoMode(QtWidgets.QLineEdit.Password)

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
            self.setFixedHeight(909)

            # Store student ID
            self.student_id = student_id

            # Toggle password visibility
            self.checkBox_showNew.stateChanged.connect(self.toggle_password)

            # Confirm button
            self.ConfirmButton.clicked.connect(self.process_password_change)
            self.PasslineEditNew.textChanged.connect(self.update_pass_requirements)


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


            self.update_pass_requirements()
            if not enforce_strong_password(new_pass):
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
        def update_pass_requirements(self):
            password = self.PasslineEditNew.text()

            # --------- Requirements ---------
            has_special = any(not c.isalnum() for c in password)
            long_enough = len(password) >= 8
            has_upper = any(c.isupper() for c in password)

            # "Not contain 3 consecutive numbers" (it's okay to have numbers if not consecutive)
            enforce_strong_password = lambda p: (
                len(p) < 8 or
                not any(not c.isalnum() for c in p) or
                not any(c.isupper() for c in p) or
                any(p[i:i+3].isdigit() and p[i] == p[i+1] == p[i+2] for i in range(len(p) - 2))
            )
            no_three_consecutive = enforce_strong_password

            # --------- Per-line coloring ---------
            color_special = "#00cc44" if has_special else "#cc0000"
            color_length = "#00cc44" if long_enough else "#cc0000"
            color_upper  = "#00cc44" if has_upper else "#cc0000"
            color_3digits = "#00cc44" if no_three_consecutive else "#cc0000"

            text = ""
            text += (
                f"<span style='color:{color_special}'>"
                f"{'✔️' if has_special else '❌'} Must contain a special character"
                f"</span><br>"
            )
            text += (
                f"<span style='color:{color_length}'>"
                f"{'✔️' if long_enough else '❌'} Minimum 8 characters"
                f"</span><br>"
            )
            text += (
                f"<span style='color:{color_upper}'>"
                f"{'✔️' if has_upper else '❌'} Must contain an uppercase letter"
                f"</span><br>"
            )
            text += (
                f"<span style='color:{color_3digits}'>"
                f"{'✔️' if no_three_consecutive else '❌'} No 3 consecutive digits"
                f"</span><br>"
            )

            # Keep label style (only text is colored via HTML)
            self.PassAcceptLabel.setText(text)


            
# _____________________________________________________________
#                        ADMIN WINDOW
# _____________________________________________________________
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
        self.setFixedWidth(1471)
        self.setFixedHeight(966)
        self.adminName = admin_name
        self.admin_id = admin_id
        self.admin_obj = admin(id=self.admin_id)
        self.welcomeLabel.setText(f"Welcome, {self.adminName}!")
        self.tabWidget.setCurrentIndex(0)
        self.current_student = None
        self.available_section_map = {}   
        self.current_section_map = {}     

        # tab 5 - Section time combo boxes
        start_times = generate_start_times()
        end_times = generate_end_times()
        self.Section_StartTime_Combo.clear()
        self.Section_StartTime_Combo.addItems(start_times)
        self.Section_EndTime_Combo.clear()
        self.Section_EndTime_Combo.addItems(end_times)


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


        # Load Tab 1 student table initially
        self.load_tab1_students()
        # Load Tab 3 table initially
        self.update_subjects_table()
        # Load Tab 4 grade table initially
        self.load_tab4_grade_table()
        # Load Tab 6 tables
        self.setup_tab6_tables()
        self.setup_tab6_tables()
        self.refresh_tab6()
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
        
        #Tab 4 : Grades
        self.Tab4_Confirm.clicked.connect(self.handle_tab4_grading)
        self.Tab4_SearchBar.textChanged.connect(self.filter_tab4_table)

        # Tab 5: Courses Management
        self.Tab5_CourseAdd.clicked.connect(self.logic_add_course)
        self.Tab5_CourseUpdate.clicked.connect(self.logic_update_course)
        self.Tab5_PrerequistieAdd.clicked.connect(self.tab5_add_prerequisite)
        self.Tab5_PrerequistieRemove.clicked.connect(self.tab5_remove_prerequisite)
        self.Tab5_SectionAdd.clicked.connect(self.logic_add_section)
        self.Tab5_SectionUpdate.clicked.connect(self.logic_update_section)
        self.Tab5_SectionRemove.clicked.connect(self.logic_remove_section)

        # Tab6
        self.Tab6_Major_combobox.currentIndexChanged.connect(self.refresh_tab6)
        self.Tab6_Term.currentIndexChanged.connect(self.refresh_tab6)
        self.Tab6_AddPlan.clicked.connect(self.add_course_to_plan)
        self.Tab6_DeletePlan.clicked.connect(self.remove_course_from_plan)

        

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
    
    #tab4 search filter
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

    ###############################################
    # TAB 1 — Student add/delete
    ###############################################

    def tab1_add_student(self):
        first = self.Tab1_FirstName.text().strip()
        last = self.Tab1_LastName.text().strip()

        if not first or not last:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill both first and last name.")
            return

        # Major combo box
        major = self.Tab1_Major.currentText()

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

    ###############################################
    # TAB 2 — Subject Enrollment
    ###############################################

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

        #table settings
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        table.setColumnWidth(3, 70)  
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        table.setColumnWidth(5, 60)  
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

        # If unchecked restores it to normal
        if state == 0:
            self.restore_available_rows()
            return

        # If a box is checked  no checkbox can be checked until unchecked again
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
        if self.current_student is None:    #checks if a student is selected
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

        if not selected_section: #checks if a course is selected
            QtWidgets.QMessageBox.warning(self, "Enrollment", "Please select a course to add.")
            return

        #calls backend function
        try:
            ok, msg = self.admin_obj.add_subject(selected_section, self.current_student.id)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Enrollment Error",
                f"Unexpected error while enrolling in {selected_section}:\n{e}",
            )
            return

        #result
        if ok:
            QtWidgets.QMessageBox.information(self, "Enrollment", msg)
            self.load_student_current_courses_table()
            self.load_available_subjects_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Enrollment", msg)

    def remove_selected_course(self):
        if self.current_student is None: #checks if a student is selected
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

        if not selected_section: #checks if a course is selected
            QtWidgets.QMessageBox.warning(self, "Remove Course", "Please select a course to remove.")
            return

        #calls backend function
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

        #result
        if ok:
            QtWidgets.QMessageBox.information(self, "Remove Course", msg)
            self.load_student_current_courses_table()
            self.load_available_subjects_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Remove Course", msg)
 
    ###############################################
    # TAB 3 — Section Details
    ###############################################

    def update_subjects_table(self):
        # Table settings
        self.Subjects_details.verticalHeader().setVisible(False)
        self.Subjects_details.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Subjects_details.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.Subjects_details.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Subjects_details.setSelectionBehavior(QAbstractItemView.SelectRows)

        #Get Inputs
        selected_major = self.Tab3_MajorChoice.currentText().strip()
        selected_term = self.Tab3_Term.currentText().strip()

        # Reset table
        self.Subjects_details.setRowCount(0)
        
        #sets columns
        self.Subjects_details.setColumnCount(6)
        self.Subjects_details.setHorizontalHeaderLabels(["Course Code", "Section ID", "Capacity", "Instructor", "Credit", "Time"])

        if not selected_term.isdigit():
            return
        #gets data from backend
        rows = admin.get_table_data_optimized(None, selected_major, int(selected_term))
        
        #fills the table
        if rows:
            for row_data in rows:
                row_position = self.Subjects_details.rowCount()
                self.Subjects_details.insertRow(row_position)
                                #1             #2      #3         #4        #5      #6
                # row postion (course_code, section, capacity, instructor, credit, time)
                self.Subjects_details.setItem(row_position, 0, QTableWidgetItem(str(row_data[0])))
                self.Subjects_details.setItem(row_position, 1, QTableWidgetItem(str(row_data[1])))
                self.Subjects_details.setItem(row_position, 2, QTableWidgetItem(str(row_data[2])))
                self.Subjects_details.setItem(row_position, 3, QTableWidgetItem(str(row_data[3])))
                self.Subjects_details.setItem(row_position, 4, QTableWidgetItem(str(row_data[4])))
                self.Subjects_details.setItem(row_position, 5, QTableWidgetItem(str(row_data[5])))
                
                #To center all columns
                for i in range(6):
                    self.Subjects_details.item(row_position, i).setTextAlignment(Qt.AlignCenter)

    ###############################################
    # TAB 4 — Grading
    ###############################################

    def handle_tab4_grading(self):
        admin_obj = self.admin_obj
        student_id = self.Tab4_Student_ID.text().strip()
        course_code = self.Tab4_Course_code.text().strip()
        grade_value = self.Tab4_Course_code_2.text().strip()

        # To make sure all fields are filled
        if not student_id or not course_code or not grade_value:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        if not student_id.isdigit():
            QtWidgets.QMessageBox.warning(self, "Error", "Student ID must be numeric.")
            return

        # Grade must be numbers ranging from 0 to 100
        try:
            grade_float = float(grade_value)
            if grade_float < 0 or grade_float > 100:
                QtWidgets.QMessageBox.warning(self, "Error", "Grade must be between 0 and 100.")
                return
        except:
            QtWidgets.QMessageBox.warning(self, "Error", "Grade must be a number.")
            return

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
        from classes import users_db, courses_db

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

            # gets course name from the data base
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

            # Centers the alignment
            for item in (item_stu, item_code, item_name, item_grade):
                item.setTextAlignment(QtCore.Qt.AlignCenter)

            # Set items
            table.setItem(r_index, 0, item_stu)
            table.setItem(r_index, 1, item_code)
            table.setItem(r_index, 2, item_name)
            table.setItem(r_index, 3, item_grade)

        # table settings
        header = table.horizontalHeader()
        for col in range(table.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)
   
    ###############################################
    # TAB 5 — COURSE Management
    ###############################################

    def logic_add_course(self): #creates course

        # inputs
        code = self.Tab5_Course_code.text().strip()
        name = self.Tab5_Course_name.text().strip()
        credit = self.Tab5_Credit.text().strip()
        section = self.Tab5_section.text().strip()
        term = self.Tab5_term.text().strip()
        prereq = self.Tab5_prerequisite.text().strip()

        # Ensures that no fields are empty
        if not code or not name or not credit or not section or not term or not prereq:
            QMessageBox.warning(self, "Missing Data", "For adding a course, all fields must be entered.")
            return

        # Calls backend function
        success, message = self.admin_obj.rewrite_add_course(
            course_code=code,
            course_name=name,
            credit=credit,
            sections=section,
            term=term,
            prerequisites=prereq
        )

        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def logic_update_course(self):
   
        # inputs
        code = self.Tab5_Course_code.text().strip()
        name = self.Tab5_Course_name.text().strip()
        credit = self.Tab5_Credit.text().strip()
        section = self.Tab5_section.text().strip()
        term = self.Tab5_term.text().strip()
        prereq = self.Tab5_prerequisite.text().strip()

        # checks required fields
        if not code:
            QMessageBox.warning(self, "Missing Data", "Please enter the Course Code to update.")
            return

         # Call backend function
        name_arg = name if name else None
        credit_arg = credit if credit else None
        section_arg = section if section else None
        term_arg = term if term else None
        prereq_arg = prereq if prereq else None

        success, message = self.admin_obj.rewrite_update_course(
            course_code=code,
            course_name=name_arg,
            credit=credit_arg,
            sections=section_arg,
            term=term_arg,
            prerequisites=prereq_arg
        )

        #Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def tab5_add_prerequisite(self):
        #inputs
        code = self.Tab5_Prerequistie_CourseCode.text().strip()
        prereq = self.Tab5_PrerequistieCode.text().strip()

        # checks required fields
        if not code or not prereq:
            return QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")

        # Call backend function
        ok, msg = self.admin_obj.add_prerequisite_to_course(code, prereq)

        #result
        if ok:
            QtWidgets.QMessageBox.information(self, "Add Prerequisite", msg)
        else:
            QtWidgets.QMessageBox.warning(self, "Add Prerequisite", msg)

    def tab5_remove_prerequisite(self):
        # inputs
        code = self.Tab5_Prerequistie_CourseCode.text().strip()
        prereq = self.Tab5_PrerequistieCode.text().strip()

        # checks required fields
        if not code or not prereq:
            return QtWidgets.QMessageBox.warning(self, "Error", "Please fill all fields.")

        # Call backend function
        ok, msg = self.admin_obj.remove_prerequisite_from_course(code, prereq)

        # Result
        if ok:
            QtWidgets.QMessageBox.information(self, "Remove Prerequisite", msg)
        else:
            QtWidgets.QMessageBox.warning(self, "Remove Prerequisite", msg)

    def logic_add_section(self):
        # inputs
        start_time = self.Section_StartTime_Combo.currentText()
        end_time = self.Section_EndTime_Combo.currentText()
        day = self.Section_Day_Combo.currentText()
        course_code = self.Tab5_Section_CourseCord.text().strip()
        section_name = self.Tab5_Section_SectionName.text().strip()
        capacity = self.Tab5_Section_Capacity.text().strip()
        instructor_id = self.Tab5_Section_Instructor.text().strip()

        # required fields
        if not (start_time and end_time and day and course_code and section_name and capacity and instructor_id):
            QMessageBox.warning(self, "Missing Data", "For adding a section, ALL fields must be filled.")
            return

        # Call Backend function
        success, message = self.admin_obj.rewrite_add_section(
            course_code=course_code,
            section_name=section_name,
            instructor_id=instructor_id,
            capacity=capacity,
            start_time=start_time,
            end_time=end_time,
            day=day
        )

        #Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def logic_update_section(self):
       
        #inputs
        course_code = self.Tab5_Section_CourseCord.text().strip()
        section_name = self.Tab5_Section_SectionName.text().strip()
        
        # Optional fields
        capacity = self.Tab5_Section_Capacity.text().strip()
        instructor_id = self.Tab5_Section_Instructor.text().strip()
        start_time = self.Section_StartTime_Combo.currentText()
        end_time = self.Section_EndTime_Combo.currentText()
        day = self.Section_Day_Combo.currentText()

        # required fields
        if not course_code or not section_name:
            QMessageBox.warning(self, "Missing Data", "Course Code and Section Name are required for updates.")
            return

        # Call Backend function
        cap_arg = capacity if capacity else None
        inst_arg = instructor_id if instructor_id else None
        start_arg = start_time if start_time else None
        end_arg = end_time if end_time else None
        day_arg = day if day else None
        success, message = self.admin_obj.rewrite_update_section(
            course_code=course_code,
            section_name=section_name,
            instructor_id=inst_arg,
            capacity=cap_arg,
            start_time=start_arg,
            end_time=end_arg,
            day=day_arg
        )

        #Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def logic_remove_section(self):
        # inputs
        section_name = self.Tab5_Section_SectionName.text().strip()

        # required fields
        if not section_name:
            QMessageBox.warning(self, "Missing Data", "Please enter the Section Name to remove.")
            return

        # Call Backend function
        success, message = self.admin_obj.remove_section(section_name)

        #Result
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    ###############################################
    # TAB 6 — PLAN MANAGEMENT
    ###############################################

    def setup_tab6_tables(self):
        #prepare tables
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
        #update tables
        major = self.Tab6_Major_combobox.currentText()
        term_text = self.Tab6_Term.currentText()

        #call backend functions
        try:
            not_in = self.admin_obj.courses_not_in_the_plan(major) or {}
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

        #updates tables
        self._fill_tab6_table(self.Tab6_NoPlan_table, not_in)
        self._fill_tab6_table(self.Tab6_CurrentPlan_table, filtered_in_plan)

    def _fill_tab6_table(self, table, data_dict):
        #Turns off sorting while we update to prevent glitches some glitches we faced 
        table.setSortingEnabled(False)
      
        # Convert to list and SORT IT clearly
        rows = list(data_dict.items())
        rows.sort(key=lambda x: (int(x[1].get("terms", 0) or 0), x[0]))

        # Clears the table completely first
        table.setRowCount(0)
        table.setRowCount(len(rows))

        for r, (code, info) in enumerate(rows):
            item_code = QTableWidgetItem(str(code))
            item_name = QTableWidgetItem(str(info.get("course_name", "")))
            item_credit = QTableWidgetItem(str(info.get("credit", "")))
            item_term = QTableWidgetItem(str(info.get("terms", "")))
            item_prereq = QTableWidgetItem(str(info.get("prerequisites", "")))

            # Centers everything
            for item in (item_code, item_name, item_credit, item_term, item_prereq):
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            table.setItem(r, 0, item_code)
            table.setItem(r, 1, item_name)
            table.setItem(r, 2, item_credit)
            table.setItem(r, 3, item_term)
            table.setItem(r, 4, item_prereq)

        table.resizeColumnsToContents()
        
        # Re-enables sorting after avoiding glitches
        table.setSortingEnabled(True)

    def add_course_to_plan(self):
        # Adds a selected course from Not in plan to the current plan
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

            #gets the major 
            major = self.Tab6_Major_combobox.currentText()

            ok, msg = self.admin_obj.add_course_to_plan(course_code, major)

             #calls backend function
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
        row = self.Tab6_CurrentPlan_table.currentRow() #checks if a row is selected
        if row < 0:
            QMessageBox.warning(self, "Delete Course", "Please select a course from 'Current plan'.")
            return

        #checks inputs from the combo box 
        course_code = self.Tab6_CurrentPlan_table.item(row, 0).text()
        major = self.Tab6_Major_combobox.currentText()

        #calls backend function
        try:
            ok, msg = self.admin_obj.delete_course_from_plan(course_code, major)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error deleting course: {e}")
            return

        if ok:
            QMessageBox.information(self, "Delete Course", str(msg))
            self.refresh_tab6()
        else:
            QMessageBox.warning(self, "Delete Course", str(msg))
            