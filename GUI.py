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

        # ENTER triggers login
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
    def check_student(self, uni_id, password):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "SELECT id FROM students WHERE id=? AND password=?",
                (uni_id, password)
            )
            result = cur.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))
            return False

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

        # Check admin first
        if self.check_admin(UniID, password):
            self.openAdminWindow()
            return

        # Check student
        if self.check_student(UniID, password):
            self.openStudentWindow()
            return

        # If neither matched
        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid ID or Password.")

    def openStudentWindow(self):
        self.hide()
        self.main_window = StudentWindow()
        self.main_window.show()

    def openAdminWindow(self):
        self.hide()
        self.main_window = AdminWindow()
        self.main_window.show()


class StudentWindow(QtWidgets.QMainWindow):  # Open window for student
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Student_Window.ui")
        uic.loadUi(ui_path, self)


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
