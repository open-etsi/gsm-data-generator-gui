# from PyQt6.QtSql import QSqlDatabase, QSqlQuery
# import hashlib
#
#
# class database:
#     def __init__(self) -> None:
#         pass
#
#     def __del__(self):
#         QSqlDatabase.removeDatabase("QSQLITE")
#         print("Successfully removed DB connection.")
#
#     @staticmethod
#     def hash_password(string: str):
#         # ===========#
#         # This is one way mechanism cannot be reversed
#         sha256 = hashlib.sha256()
#         sha256.update(string.encode("utf-8"))
#         return sha256.hexdigest()
#
#     @staticmethod
#     def initializeDatabase():
#         db = QSqlDatabase.addDatabase("QSQLITE")
#         db.setDatabaseName("database.db")  # Replace with your database file name
#         db.setPassword("1234")
#
#         if not db.open():
#             print("Unable to establish a database connection.")
#             return None
#         else:
#             print("Successfully established a database connection.")
#         return db
#
#     @staticmethod
#     def createTable():
#         query = QSqlQuery()
#         create_table_sql = """
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL,
#             password TEXT NOT NULL,
#             email TEXT NOT NULL,
#             role TEXT NOT NULL
#         )
#         """
#
#         # Execute the CREATE TABLE statement
#         if query.exec(create_table_sql):
#             pass
#
#         else:
#             print("Error creating table:", query.lastError().text())
#
#     def insertData(self, username: str, password: str, email: str, role: str):
#         #    db = initializeDatabase()
#
#         query = QSqlQuery()
#         query.prepare("SELECT COUNT(*) FROM users WHERE username = ?")
#         query.bindValue(0, username)
#
#         if query.exec() and query.next():
#             username_count = query.value(0)
#
#             if username_count > 0:
#                 return "Username already exists.", False
#
#         # Prepare an SQL INSERT statement with placeholders
#         query.prepare(
#             "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)"
#         )
#
#         encrypted_pass = self.hash_password(password)
#
#         # Bind values to the placeholders
#         query.bindValue(0, username)
#         query.bindValue(1, encrypted_pass)
#         query.bindValue(2, email)
#         query.bindValue(3, role)
#
#         # Execute the INSERT statement
#         if query.exec():
#             return "Data inserted successfully.", True
#
#         else:
#             result = "Error inserting data:" + query.lastError().text()
#             return result, False
#
#     def getEmail(self, username):
#         query = QSqlQuery()
#
#         query.prepare("SELECT email FROM users WHERE username = ?")
#
#         # Bind values to the placeholders
#         query.bindValue(0, username)
#         # Execute the SELECT statement
#         if query.exec():
#             if query.next():
#                 return query.value(0)  # Return the email
#             else:
#                 print("Record not found")
#         else:
#             print("Error retrieving email:", query.lastError().text())
#
#         return None  # Return None if no email found or an error occurred
#
#     def getRole(self, username):
#         #    db = initializeDatabase()
#         query = QSqlQuery()
#
#         #    query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
#         query.prepare("SELECT role FROM users WHERE username = ?")
#
#         # Bind values to the placeholders
#         query.bindValue(0, username)
#         # Execute the SELECT statement
#         if query.exec():
#             if query.next():
#                 return query.value(0)  # Return the role
#             else:
#                 print("Record not found")
#         else:
#             print("Error retrieving role:", query.lastError().text())
#
#         return None  # Return None if no email found or an error occurred
#
#     def checkCredentials(self, username, password):
#         #    db = initializeDatabase()
#         query = QSqlQuery()
#
#         # Prepare an SQL SELECT statement with placeholders
#         query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
#         password = self.hash_password(password)
#
#         # Bind values to the placeholders
#         query.bindValue(0, username)
#         query.bindValue(1, password)
#
#         if query.exec():
#             # Check if there's at least one row in the result set
#             if query.next():
#                 #            print("Credentials match.")
#                 return "Credentials match.", True
#             else:
#                 #            print("Credentials do not match.")
#                 return "Credentials do not match.", False
#         else:
#             string = "Error checking credentials:" + query.lastError().text()
#             #            print(string)
#             return string, False
#
#
# # if __name__ == "__main__":
# db = database()
# db.initializeDatabase()
# db.createTable()
# db.insertData("admin", "admin", "admin@email.com", "admin")
# db.insertData("user", "user", "user@email.com", "user")
#
# # checkCredentials("aa","aa#")
# # getEmail("hamza")
# # getRole("user")
