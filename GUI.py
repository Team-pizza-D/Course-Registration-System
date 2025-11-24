import sys
import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Login.ui")
        uic.loadUi(ui_path, self)
        self.setFixedWidth(552)
        self.setFixedHeight(650)
        self.loginButton.clicked.connect(self.loginfunction)
        self.checkBox_show.stateChanged.connect(self.toggle_password)
        self.PasslineEdit.returnPressed.connect(self.loginButton.click)

    def toggle_password(self):
        if self.checkBox_show.isChecked():
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.PasslineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        
    def loginfunction(self):
        UniID = self.IDlineEdit.text()
        password = self.PasslineEdit.text()
        # Add your authentication logic here
        if UniID == "admin" and password == "1234":
            self.OpenMainWindow()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            
    def OpenMainWindow(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
        
    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "tstMain.ui")
        uic.loadUi(ui_path, self)
        
        
        
        
def main():
    app = QApplication(sys.argv)  # getting arguments from prompt
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())  # Keeps the window open till it closed manually

if __name__ == "__main__":
    main()