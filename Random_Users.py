import sqlite3
from classses2 import admin, instructor
from Programs import All_Courses, L, L1, L2

#------------5 Admins-----------------
# admin5 = admin(username="Ahmed Alrajhi", database=True)
# admin1 = admin(username="Mohammed Jeddawi", database=True)
# admin2 = admin(username="Ayman Felemban", database=True)
# admin3 = admin(username="Abdullah Alzahrani", database=True)
# admin4 = admin(username="Ali Alqarni", database=True)  
#------------74 Teachers--------------
Teachers = ["Ahmed Alqahtani" , "Ali alqarni" , "Ayman Alharbi", "Khalid Hassan", "Mohammed Ajour",
            "Raad Alqarni", "Mohammed Alghamdi", "Salem Alotaibi", "Faisal Alzahrani", "Fahad Alharthi",
            "Turki Alqarni", "Yasser Alamri", "Hazem Alshamrani", "Habeeb Khan", "Abdulateef Noor",
            "Khalid Alharbi", "Mohanned Alkhaldi", "Ayman Madbouly", "Abdulrahman Hakami", "Waseem Saeed",
            "Alaa Alghamdi", "Nawaf Algthmi", "Abdullah Alghamdi", "Nawab Hussain", "Hassan Ali",
            "Maher Bahaddad", "Mohammed Alnoqaiti", "Ameen Alshekh", "Abdulaziz Tefouti", "Ahmed Albargi",
            "Azzam Ahmed", "Azad Khan", "Ammar Alamri", "Mohammed Babkeer", "Abdulrahman Banawass",
            "Elyas Felfelan", "Roger Junior", "Mustafa Alharbi", "Rakan Althahri", "Eyad Fouad",
            "Anas Aljahmi", "Abdullah Bokhari", "Yazeed Althagafi", "Hammam Alqarni", "Mishary Asery",
            "Moath Alshareef", "Ibraheem Ahmed", "Tariq Rashad", "Osama Alyamani",  "Nayef Alqahtani",
            "Omar Alqahtani", "Rayan Almasmomi", "Zaher Kamel", "Baraa Alaamodi", "Jamal Alaa",
            "Ziyad Aljahmi", "Nizar Abdo", "Moayad Osama", "Jehad Alfarran", "Qasim Abdulaleem",
            "Aseel bahatheg", "Hamed Alklbani", "Kamil Alamri", "Saad Alzahrani", "Saeed Alghamdi",
            "Thamer Alshmrani", "Emad Alzahrani", "Shaker Alshamrani", "Basel Alqarni", "Yousef Alhashmi",
            "Taher Alshahrani", "Faris Awad", "Essam Alshawali", "Khalil Albloushi"]


# db = sqlite3.connect("Users.db")
# cr = db.cursor()
# cr.execute("DELETE FROM instructors")
# db.commit()
# db.close()
# T = []
# for i in range(len(Teachers)):
#     inst = instructor(Teachers[i], All_Courses[i], L1[i], database=True)
#     inst.add_section(All_Courses[i], L2[i])
#     T.append(inst)  
