import sys
import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class LoginWindow(QMainWindow): # Open login window
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Login.ui")
        uic.loadUi(ui_path, self)
        self.setFixedWidth(552)
        self.setFixedHeight(650)
        self.loginButton.clicked.connect(self.loginfunction)
        self.checkBox_show.stateChanged.connect(self.toggle_password)
        self.PasslineEdit.returnPressed.connect(self.loginButton.click)

    def toggle_password(self): # Function to show/hide password
        if self.checkBox_show.isChecked():
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        
    def loginfunction(self): # Login function for either sudent or admin
        UniID = self.IDlineEdit.text()
        password = self.PasslineEdit.text()
        # Add your authentication logic here
        if UniID == "admin" and password == "1234":
            self.OpenMainWindow()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            
    def OpenMainWindow(self): # Hide login window and open student window
        self.hide()
        self.main_window = StudentWindow()
        self.main_window.show()
        
    

class StudentWindow(QtWidgets.QMainWindow): # Open window for student
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Student_Window.ui")
        uic.loadUi(ui_path, self)
        
        
        
        
def main():
    app = QApplication(sys.argv)  # getting arguments from prompt
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())  # Keeps the window open till it closed manually

if __name__ == "__main__":
    main()