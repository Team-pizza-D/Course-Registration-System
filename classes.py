# class subjects:
#     def __init__(self, name, code,MaxCapacity,credits):
#         self.name = name
#         self.code = code
#         self.MaxCapacity = MaxCapacity
#         self.credits = credits

#     def display_info(self):
#         return f"Subject Name: {self.name}, Subject Code: {self.code}, Max Capacity: {self.MaxCapacity}, Credits: {self.credits}"
    
    

# class students:
#     def __init__(self, name, student_id,)

class user:
    def __init__(self, username, password,  email, status, Id=None ):
        self.username = username
        self.password = password
        self.Id = Id
        self.email = email
        self.status = status

    def display_info(self):
        return f"Username: {self.username}, Email: {self.email}, Status: {self.status}, ID: {self.Id}"
