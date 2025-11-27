import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QAbstractItemView,QHeaderView , QTableWidgetItem
)
from PyQt5 import uic
from PyQt5.QtCore import Qt



class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "Admin_Window.ui")
        uic.loadUi(ui_path, self)
        self.Tab2_LoadSubjects()
        self.Button_Connctions()
        self.Tab2_SubjectsTable.itemClicked.connect(self.Tab2_SelectSubject)


        #All table settings are done here to make it look better
#------------------------------Tab 1 Student Table Settings---------------------------
        self.Tab1_StudentTable.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.Tab1_StudentTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.Tab1_StudentTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.Tab1_StudentTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.Tab1_StudentTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Tab1_StudentTable.verticalHeader().setVisible(False)                                     #Table settings for Table 1 Student Table     
        self.Tab1_StudentTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Tab1_StudentTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Tab1_StudentTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Tab1_StudentTable.horizontalHeader().setDefaultSectionSize(110)
        self.Tab1_StudentTable.verticalHeader().setDefaultSectionSize(28) 
#-----------------------------------------------------------------------------------------
        self.Tab2_SubjectsTable.verticalHeader().setVisible(False)
        self.Tab2_SubjectsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Tab2_SubjectsTable.setSelectionBehavior(QAbstractItemView.SelectRows)                      
        self.Tab2_SubjectsTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.Tab2_SubjectsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Tab2_SubjectsTable.setColumnCount(3)
        self.Tab2_SubjectsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.StudentCourseTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.StudentCourseTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.StudentCourseTable.setEditTriggers(QAbstractItemView.NoEditTriggers)               #Table settings for Tab 2 Subjects Table
        self.StudentCourseTable.verticalHeader().setVisible(False)
        self.StudentCourseTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.StudentCourseTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.StudentCourseTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.StudentCourseTable.horizontalHeader().setDefaultSectionSize(150)
        self.StudentCourseTable.verticalHeader().setDefaultSectionSize(35)

#------------------------------------------------------------------------------------------------------------------

    def Button_Connctions(self): #All buttons from all tabs are connected here

        # ----------------- TAB 1 Buttons -------------------------------
        self.Tab1_AddStudent.clicked.connect(self.Tab1_AddDelete)
        self.Tab1_DeleteStudent.clicked.connect(self.Tab1_AddDelete)
        self.Tab1_SelectStudent.clicked.connect(self.Tab1_Select)
        self.Tab1_SearchStudent.clicked.connect(self.Tab1_Search)

        # ----------------- TAB 2 Buttons -------------------------------
        self.Tab2_AddCourse.clicked.connect(self.Tab2_AddCourseFunction)
        self.Tab2_DeleteCourse.clicked.connect(self.Tab2_DeleteCourseFunction)


#---------------------------------Tab 1 functions---------------------------------
    # Tab 1 required inputs for add/delete
    def Tab1_AddDelete(self):
        StudentID = self.Tab1_StudentID.text()
        FName = self.Tab1_FirstName.text()
        LName = self.Tab1_LastName.text()
        Email = self.Tab1_Email.text()

        #Error message for empty fields
        if not StudentID or not FName or not LName or not Email:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return
    def Tab1_Select(self):
        table = self.Tab1_StudentTable
        row = table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a student from the table.")
            return
        
        self.Tab_Clear() # to clear old data before selecting new student

        StudentID = table.item(row, 0).text()
        FName = table.item(row, 1).text()
        LName = table.item(row, 2).text()                   #labels equivalent to table fields
        Email = table.item(row, 3).text()
        Status = table.item(row, 4).text()
#--------------------------------------------------------------------------------------------------------------------------
        self.Tab1_StudentID.setText(StudentID)
        self.Tab1_FirstName.setText(FName)
        self.Tab1_LastName.setText(LName)               #fills input fields with selected student data
        self.Tab1_Email.setText(Email)
        index = self.Tab1_Status.findText(Status)
        if index >= 0:
            self.Tab1_Status.setCurrentIndex(index)
#--------------------------------------------------------------------------------------------------------------------------
    # Tab 1 required inputs for search
    def Tab1_Search(self):
        StudentID = self.Tab1_StudentID.text()
        #Error message for empty fields
        if not StudentID:
            QMessageBox.warning(self, "Input Error", "Student ID is required for search.")
            return
    def Tab_Clear(self): #Clears all input fields in Tab 1 before selecting a new student to make sure no old data is left
        self.Tab1_StudentID.clear()
        self.Tab1_FirstName.clear()
        self.Tab1_LastName.clear()
        self.Tab1_Email.clear()
        self.Tab1_Status.setCurrentIndex(0)  




#---------------------------------Tab 2 functions---------------------------------
    
    def Tab2functions(self):
        StudentID = self.Tab2_StudentID.text()
        FName = self.Tab2_FirstName.text()
        LName = self.Tab2_LastName.text()
        CourseName = self.Tab2_CourseName.text()
        CourseID = self.Tab2_CourseID.currentText()
        SectionID = self.Tab2_SectionID.text()

    def Tab2_LoadSubjects(self): #####waiting for database connection to load subjects
        # subjects = 
        pass

        self.Tab2_SubjectsTable.setRowCount(0)

        for row, (code, name, section) in enumerate(subjects):  #####waiting for database connection to load subjects
            self.Tab2_SubjectsTable.insertRow(row)
            self.Tab2_SubjectsTable.setItem(row, 0, QTableWidgetItem(code))
            self.Tab2_SubjectsTable.setItem(row, 1, QTableWidgetItem(name))
            self.Tab2_SubjectsTable.setItem(row, 2, QTableWidgetItem(section))


    def Tab2_SelectSubject(self):
        row = self.Tab2_SubjectsTable.currentRow()
        if row < 0:
            return

        self.Tab_Clear()

        course_code = self.Tab2_SubjectsTable.item(row, 0).text()
        course_name = self.Tab2_SubjectsTable.item(row, 1).text()
        section_id  = self.Tab2_SubjectsTable.item(row, 2).text()

        self.Tab2_CourseCode.setText(course_code)
        self.Tab2_CourseName.setText(course_name)
        self.Tab2_SectionID.setText(section_id)
    def Tab2_AddCourseFunction(self):
        student_id = self.Tab2_StudentID.text()
        first_name = self.Tab2_FirstName.text()
        last_name  = self.Tab2_LastName.text()
        course_code = self.Tab2_CourseCode.text()
        course_name = self.Tab2_CourseName.text()
        section_id = self.Tab2_SectionID.text()
    # Error messages for empty fields
        if not student_id or not first_name or not last_name:
            QMessageBox.warning(self, "Input Error", "Student info is required.")
            return

        if not course_code or not course_name or not section_id:
            QMessageBox.warning(self, "Input Error", "Please select a course with all details.")
            return
    def Tab2_DeleteCourseFunction(self):
        pass






#---------------------------------Main Function---------------------------------
def main():
    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
