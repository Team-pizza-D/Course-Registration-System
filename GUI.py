import sys
import os
import sqlite3
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence

DB_PATH = os.path.join(os.path.dirname(__file__), "Users.db")


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
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, major FROM students WHERE id=? AND password=?",
                (uni_id, password)
            )
            result = cur.fetchone()
            conn.close()
            return result   # (id, name, major)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))
            return None

    def check_admin(self, uni_id, password):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "SELECT Id FROM admins WHERE Id=? AND password=?",
                (uni_id, password)
            )
            result = cur.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))
            return False

    # __________ LOGIN LOGIC __________

    def loginfunction(self):
        UniID = self.IDlineEdit.text()
        password = self.PasslineEdit.text()

        admin = self.check_admin(UniID, password)
        student = self.check_student(UniID, password)

        if admin:
            self.openAdminWindow()
            return

        if student:
            sid, sname, smajor = student
            self.openStudentWindow(sid, sname, smajor)
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

        self.student_id = sid
        self.student_name = sname
        self.student_major = smajor

        # Set welcome text
        self.welcomeLabel.setText(f"Welcome, {self.student_name}")

        # Load student info into table
        self.load_info_table()

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
