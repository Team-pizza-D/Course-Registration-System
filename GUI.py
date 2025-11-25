import sys
import os
import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut


DB_PATH = os.path.join(os.path.dirname(__file__), "Users.db")


class LoginWindow(QMainWindow):  # Open login window
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Login.ui")
        uic.loadUi(ui_path, self)
        self.setFixedWidth(552)
        self.setFixedHeight(650)

        self.loginButton.clicked.connect(self.loginfunction)

        # ENTER triggers globally
        QShortcut(QKeySequence("Return"), self, self.loginButton.click)
        QShortcut(QKeySequence("Enter"), self, self.loginButton.click)

        # Password toggle
        self.checkBox_show.stateChanged.connect(self.toggle_password)

    # Show/hide password
    def toggle_password(self):
        if self.checkBox_show.isChecked():
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

    # --- DB Authentication ---
    # Check student credentials
    def check_student(self, uni_id, password):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            cur.execute(
                "SELECT id, username FROM students WHERE id=? AND password=?",
                (uni_id, password)
            )
            result = cur.fetchone()
            conn.close()
            return result  # tuple → (id, username) OR None
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))
            return None

    # Check admin credentials
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

    # Login logic
    def loginfunction(self):
        UniID = self.IDlineEdit.text()
        password = self.PasslineEdit.text()

        admin = self.check_admin(UniID, password)
        student = self.check_student(UniID, password)

        if admin:
            self.openAdminWindow()
            return

        if student:
            student_id, student_name = student
            self.openStudentWindow(student_name)
            return

        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid ID or Password.")
        
    def openStudentWindow(self, student_name):
        self.hide()
        self.main_window = StudentWindow(student_name)
        self.main_window.show()




class StudentWindow(QtWidgets.QMainWindow):  # Open window for student
    def __init__(self, student_name):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Student_Window.ui")
        uic.loadUi(ui_path, self)
        self.welcomeLabel.setText(f"Hello, {student_name}")



class AdminWindow(QtWidgets.QMainWindow):  # Open window for admin
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Admin_Window.ui")
        uic.loadUi(ui_path, self)


def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
