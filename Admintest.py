import sys
import os
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from classses2 import student, admin  # from classses2.py


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, admin_id=None, admin_name=None):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Admin_Window.ui")
        uic.loadUi(ui_path, self)


    


        # Match fixed size from .ui
        self.setFixedWidth(1236)
        self.setFixedHeight(966)

        # Admin object (we only need it for add_subject / remove_subject)
        self.admin_obj = admin(id=admin_id) if admin_id is not None else admin()
        self.current_student = None          # student object for Tab 2
        self.available_section_map = {}      # row -> section code (right table)
        self.current_section_map = {}        # row -> section code (left table)

        # ---------- General table settings ----------
        for table in (self.StudentCourseTable, self.Tab2_SubjectsTable,
                      getattr(self, "Tab1_StudentTable", None),
                      getattr(self, "CapacityTable", None),
                      getattr(self, "StudentGradeTable_4", None)):
            if table is None:
                continue
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.verticalHeader().setVisible(False)

        # ---------- Subject Enrollment Tab connections ----------
        # Submit button in Subject Enrollment tab
        self.pushButton.clicked.connect(self.handle_submit_student)

        # Add / Remove buttons
        self.Tab2_AddCourse.clicked.connect(self.add_selected_course)
        self.Tab2_DeleteCourse.clicked.connect(self.remove_selected_course)

        # Ensure message label starts empty
        self.EnrollmentMessege.setText("")

    # =========================================================
    #              SUBJECT ENROLLMENT (TAB 2)
    # =========================================================

    def handle_submit_student(self):
        """
        Called when the 'Submit' button next to Student ID is pressed.
        - Validates the ID
        - Creates a student object
        - Loads current courses (left table)
        - Loads available subjects (right table)
        """
        self.EnrollmentMessege.setText("")

        id_text = self.Tab2_StudentID.text().strip()
        if not id_text.isdigit():
            self.EnrollmentMessege.setText("Please enter a valid numeric student ID.")
            self.clear_enrollment_tables()
            self.current_student = None
            return

        sid = int(id_text)

        # Temporary student object to check existence
        stu = student(id=sid)
        if not stu.is_student():
            self.EnrollmentMessege.setText(f"Student with ID {sid} not found.")
            self.clear_enrollment_tables()
            self.current_student = None
            return

        # Valid student → keep object and load tables
        self.current_student = stu
        self.load_student_current_courses_table()
        self.load_available_subjects_table()

    def clear_enrollment_tables(self):
        """Clears both enrollment tables."""
        self.StudentCourseTable.clearContents()
        self.Tab2_SubjectsTable.clearContents()
        self.StudentCourseTable.setRowCount(0)
        self.Tab2_SubjectsTable.setRowCount(0)

    # ---------- Right table: Available subjects ----------

    def load_available_subjects_table(self):
        """
        Fills Tab2_SubjectsTable with subjects available for the current student
        using student.view_available_subjects().
        """
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
            # Function returned an error / message string
            self.EnrollmentMessege.setText(str(available))
            return

        self.available_section_map = {}
        table.setRowCount(len(available))

        row = 0
        for _, (section, course_code, instructor, time, credit) in available.items():
            # Checkbox in column 0
            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("margin-left: 8px;")
            checkbox.stateChanged.connect(self.on_available_checkbox_changed)
            table.setCellWidget(row, 0, checkbox)

            # Map row → section code
            self.available_section_map[row] = section

            # Other columns
            items = [
                QtWidgets.QTableWidgetItem(course_code),   # col 1
                QtWidgets.QTableWidgetItem(instructor),    # col 2
                QtWidgets.QTableWidgetItem(section),       # col 3
                QtWidgets.QTableWidgetItem(time),          # col 4
                QtWidgets.QTableWidgetItem(str(credit)),   # col 5
            ]

            col = 1
            for item in items:
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)
                col += 1

            row += 1

        # Column sizes (copy from StudentWindow logic)
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)   # Section
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)   # Credit
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        # Stretch the remaining columns
        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def on_available_checkbox_changed(self, state):
        """
        Allows only one checkbox in Tab2_SubjectsTable.
        When one is checked, all other rows are greyed & disabled.
        """
        table = self.Tab2_SubjectsTable
        sender = self.sender()
        clicked_row = None

        # Find which row contains the clicked checkbox
        for row in range(table.rowCount()):
            if table.cellWidget(row, 0) == sender:
                clicked_row = row
                break

        if clicked_row is None:
            return

        # UNCHECK → restore all rows
        if state == 0:
            self.restore_available_rows()
            return

        # CHECKED → gray out all OTHER rows
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

    # ---------- Left table: Student current courses ----------

    def load_student_current_courses_table(self):
        """
        Fills StudentCourseTable (left table) with the student's current
        enrolled subjects using student.view_enrolled_subjects().
        """
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
            # No enrolled subjects or error message
            self.EnrollmentMessege.setText(str(schedule))
            return

        self.current_section_map = {}
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
                # If format is unexpected, just show the original string
                time_display = time_days

            # Checkbox in column 0
            checkbox = QtWidgets.QCheckBox()
            checkbox.setStyleSheet("margin-left: 8px;")
            checkbox.stateChanged.connect(self.on_current_checkbox_changed)
            table.setCellWidget(row, 0, checkbox)

            # Map row → section code
            self.current_section_map[row] = section

            # Other columns
            items = [
                QtWidgets.QTableWidgetItem(course_code),    # col 1
                QtWidgets.QTableWidgetItem(instructor),     # col 2
                QtWidgets.QTableWidgetItem(section),        # col 3
                QtWidgets.QTableWidgetItem(time_display),   # col 4
                QtWidgets.QTableWidgetItem(str(credit)),    # col 5
            ]

            col = 1
            for item in items:
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(row, col, item)
                col += 1

            row += 1

        # Column widths (same logic as Student window)
        table.setColumnWidth(0, 40)
        table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(3, 70)   # Section
        table.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)

        table.setColumnWidth(5, 60)   # Credit
        table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)

        for col in [1, 2, 4]:
            table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

    def on_current_checkbox_changed(self, state):
        """
        Only one checkbox in StudentCourseTable at a time.
        When one is checked, gray out the others.
        """
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

    # ---------- Add / Remove buttons using admin methods ----------

    def add_selected_course(self):

        if self.current_student is None:
            QtWidgets.QMessageBox.warning(
                self, "Enrollment", "Please submit a valid Student ID first."
            )
            return

        table = self.Tab2_SubjectsTable
        selected_section = None

        # find the checked row
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_section = self.available_section_map.get(row)
                break

        if not selected_section:
            QtWidgets.QMessageBox.warning(self, "Enrollment", "Please select a course to add.")
            return

        # call admin.add_subject
        try:
            ok, msg = self.admin_obj.add_subject(selected_section, self.current_student.id)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Enrollment Error",
                f"Unexpected error while enrolling in {selected_section}:\n{e}",
            )
            return

        # show message
        if ok:
            QtWidgets.QMessageBox.information(self, "Enrollment", msg)
            self.load_student_current_courses_table()
            self.load_available_subjects_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Enrollment", msg)




    def remove_selected_course(self):
        """
        Uses admin.remove_subject(section_code, student_id)
        and shows QMessageBox like StudentWindow.
        """
        if self.current_student is None:
            QtWidgets.QMessageBox.warning(
                self, "Remove Course", "Please submit a valid Student ID first."
            )
            return

        table = self.StudentCourseTable
        selected_section = None

        # find which row is selected
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_section = self.current_section_map.get(row)
                break

        if not selected_section:
            QtWidgets.QMessageBox.warning(self, "Remove Course", "Please select a course to remove.")
            return

        # call admin.remove_subject
        try:
            ok, msg = self.admin_obj.remove_subject(selected_section, str(self.current_student.id).strip())
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Remove Course Error",
                f"Unexpected error while removing {selected_section}:\n{e}",
            )
            return

        # show message
        if ok:
            QtWidgets.QMessageBox.information(self, "Remove Course", msg)
            self.load_student_current_courses_table()
            self.load_available_subjects_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Remove Course", msg)


# Optional: simple launcher if you want to run this file directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AdminWindow()
    win.show()
    sys.exit(app.exec_())
