# import hashlib
# import mysql.connector
# from mysql.connector import Error
#
#
# class sqldatabase:
#     def __init__(self):
#         self.conn = None
#
#     @staticmethod
#     def hash_password(string: str) -> str:
#         """
#         Encrypts the password to be stored in the database (one-way hashing).
#
#         Args:
#             string (str): Password in plain text
#
#         Returns:
#             str: Encrypted/Hashed Password
#         """
#         sha256 = hashlib.sha256()
#         sha256.update(string.encode("utf-8"))
#         return sha256.hexdigest()
#
#     def initializeDatabase(self):
#         try:
#             self.conn = mysql.connector.connect(
#                 user="root",
#                 password="1234",
#                 host="127.0.0.1",
#                 # port=3306,
#                 database="database1",
#             )
#             if not self.conn.is_connected():
#                 print("Unable to establish a database connection.")
#                 return None
#             else:
#                 print("Successfully established a database connection.")
#         except Error as e:
#             print("Error:", e)
#
#     def createTable(self):
#         try:
#             mycursor = self.conn.cursor()
#             create_table_sql = """
#             CREATE TABLE IF NOT EXISTS users (
#                 user_id INT AUTO_INCREMENT,
#                 user_name TEXT NOT NULL,
#                 user_pass TEXT NOT NULL,
#                 user_email TEXT NOT NULL,
#                 user_role TEXT NOT NULL,
#                 Primary key (user_id)
#             )
#             """
#             mycursor.execute(create_table_sql)
#             self.conn.commit()
#         except Error as e:
#             print("Error creating table:", e)
#
#     def insertData(
#         self, user_name: str, user_pass: str, user_email: str, user_role: str
#     ):
#         try:
#             mycursor = self.conn.cursor()
#             check_data = (user_name,)
#             check_record = "SELECT COUNT(*) FROM users WHERE user_name = %s"
#             mycursor.execute(check_record, check_data)
#             count = mycursor.fetchone()[0]
#
#             if count == 0:
#                 add_employee = """
#                 INSERT INTO users (user_name, user_pass, user_email, user_role)
#                 VALUES (%s, %s, %s, %s)
#                 """
#                 encrypted_pass = self.hash_password(user_pass)
#                 data_employee = (user_name, encrypted_pass, user_email, user_role)
#
#                 mycursor.execute(add_employee, data_employee)
#                 self.conn.commit()
#                 return "Data inserted successfully.", True
#             else:
#                 print("This username already exists.")
#                 result = "Username already exists"
#                 return result, False
#         except Error as e:
#             print("Error inserting data:", e)
#             return "Error inserting data", False
#
#     def getEmail(self, username):
#         try:
#             mycursor = self.conn.cursor()
#             get_email_query = "SELECT user_email FROM users WHERE user_name = %s"
#             get_email_data = (username,)
#             mycursor.execute(get_email_query, get_email_data)
#             email = mycursor.fetchone()[0]
#             return email
#         except Error as e:
#             print("Error retrieving email:", e)
#             return None
#
#     def getRole(self, username):
#         try:
#             mycursor = self.conn.cursor()
#             get_role_query = "SELECT user_role FROM users WHERE user_name = %s"
#             get_role_data = (username,)
#             mycursor.execute(get_role_query, get_role_data)
#             role_result = mycursor.fetchone()
#
#             if role_result is not None:
#                 role = role_result[0]
#                 print(f"The role of {username} is: {role}")
#                 return role
#             else:
#                 print(f"No entry named {username}")
#                 return None
#         except Error as e:
#             print("Error fetching role:", e)
#             return None
#
#     def checkCredentials(self, username, password):
#         try:
#             mycursor = self.conn.cursor()
#             check_credentials_query = (
#                 "SELECT * FROM users WHERE user_name = %s AND user_pass = %s"
#             )
#             password = self.hash_password(password)
#             check_credentials_data = (username, password)
#
#             mycursor.execute(check_credentials_query, check_credentials_data)
#             if len(mycursor.fetchall()) > 0:
#                 string = "Credentials match."
#                 return string, True
#             else:
#                 string = "Credentials do not match."
#                 return string, False
#         except Error as e:
#             print("Error checking credentials:", e)
#             return "Error checking credentials", False
#
#
# # Usage example:
# db = sqldatabase()
# db.initializeDatabase()
# db.createTable()
# db.insertData("admin", "admin", "admin@email.com", "admin")
# db.insertData("user", "user", "user@email.com", "user")
# # import hashlib
# # import mysql.connector
# # from getpass import getpass
# # from mysql.connector import connect, Error
# # import functools
# # import operator
#
#
# # class sqldatabase:
# #     def __init__(self) -> None:
# # #        self.conn = None
# # #        self.conn = mysql.connector()
# #         pass
#
# #     # def __del__(self):
# #     #     QSqlDatabase.removeDatabase("QSQLITE")
# #     #     print("Successfully removed DB connection.")
#
# #     @staticmethod
# #     def hash_password(string: str) -> str:
# #         """
# #         This is for encrypted password store in database
# #         This is one way mechanism cannot be reversed
#
# #         Args:
# #             string (str): Password in plain text
#
# #         Returns:
# #             string (str): Enxrypted/Hashed Password
# #         """
# #         sha256 = hashlib.sha256()
# #         sha256.update(string.encode("utf-8"))
# #         return sha256.hexdigest()
#
# #     def initializeDatabase(self):
# #         try:
# #             self.conn = mysql.connector.connect(
# #                 user="root",
# #                 password="1234",
# #                 host="127.0.0.1",
# #                 port=3306,
# #                 database="database1",
# #             )
# #             if not self.conn.is_connected():
# #                 print("Unable to establish a database connection.")
# #                 return None
# #             else:
# #                 print("Successfully established a database connection.")
# #         except Exception as e:
# #             print("Error", e)
#
# # #        return conn
#
# #     def createTable(self):
# #         mycursor = self.conn.cursor()
# #         create_table_sql = """
# #         CREATE TABLE IF NOT EXISTS users (
# #         user_id INT AUTO_INCREMENT,
# #         user_name TEXT NOT NULL,
# #         user_pass TEXT NOT NULL,
# #         user_email TEXT NOT NULL,
# #         user_role TEXT NOT NULL,
# #         Primary key (user_id)
# #         )
# #         """
#
# #         if mycursor.execute(create_table_sql):
# #             self.conn.commit()
# #         else:
# #             print("Error creating table")
#
# #     def insertData(
# #         self, user_name: str, user_pass: str, user_email: str, user_role: str
# #     ):
# #         mycursor = self.conn.cursor()
# #         check_data = (user_name,)
# #         check_record = """
# #         SELECT COUNT(*) FROM users
# #         WHERE user_name = %s
# #         """
#
# #         mycursor.execute(check_record, check_data)
# #         temp = mycursor.fetchone()
# #         self.conn.commit()
# #         str = functools.reduce(operator.add, (temp))
# #         if str == 0:
# #             print("users for this entry are :", str)
# #             add_employee = """INSERT INTO users
# #                 (user_name, user_pass, user_email, user_role)
# #                 VALUES (%s, %s, %s, %s);"""
#
# #             encrypted_pass = self.hash_password(user_pass)
#
# #             data_employee = (user_name, encrypted_pass, user_email, user_role)
#
# #             mycursor.execute(add_employee, data_employee)
# #             self.conn.commit()
# #             return "Data inserted successfully.", True
# #         else:
# #             print("This username aleady exist")
# #             result = "User Name already exists"
# #             return result, False
#
# #     def getEmail(self, username):
# #         mycursor = self.conn.cursor()
# #         get_email_query = """
# #         SELECT user_email FROM users WHERE user_name = %s
# #         """
# #         get_email_data = (username,)
# #         mycursor.execute(get_email_query, get_email_data)
# #         return mycursor.fetchone()[0]
#
# #         # # Bind values to the placeholders
# #         # query.bindValue(0, username)
# #         # # Execute the SELECT statement
# #         # if query.exec():
# #         #     if query.next():
# #         #         return query.value(0)  # Return the email
# #         #     else:
# #         #         print("Record not found")
# #         # else:
# #         #     print("Error retrieving email:", query.lastError().text())
#
# #         # return None  # Return None if no email found or an error occurred
#
# #     def getRole(self, username):
# #         mycursor = self.conn.cursor()
# #         get_role_query = "SELECT user_role FROM users WHERE user_name = %s"
# #         get_role_data = (username,)
#
# #         mycursor.execute(get_role_query, get_role_data)
# #         role_result = mycursor.fetchone()
#
# #         if role_result is not None:
# #             role = role_result[0]
# #             print(f"The role of {username} is: {role}")
# #             return role
# #         else:
# #             print(f"No entry named {username}")
# #             return None
#
# #         mycursor.close()  # Close the cursor when done
#
# #     # def getRole(self, username):
#
# #     #     mycursor=self.conn.cursor()
# #     #     get_role_query="""
# #     #     SELECT user_role FROM users WHERE user_name = %s
# #     #     """
# #     #     get_role_data=(username,)
#
# #     #     mycursor.execute(get_role_query,get_role_data)
#
# #     #     if len(mycursor.fetchone())!=0:
# #     #         print(mycursor.fetchone()[0])
# #     #     else:
# #     #         print("No entry named {}".format(username))
# #     # if query.exec():
# #     #     if query.next():
# #     #         return query.value(0)  # Return the role
# #     #     else:
# #     #         print("Record not found")
# #     # else:
# #     #     print("Error retrieving role:", query.lastError().text())
#
# #     # return None  # Return None if no email found or an error occurred
#
# #     def checkCredentials(self, username, password):
# #         mycursor = self.conn.cursor()
# #         check_credentials_query = """
# #         SELECT * FROM users WHERE user_name = %s AND user_pass = %s
# #         """
# #         password = self.hash_password(password)
# #         check_credentials_data = (username, password)
#
# #         mycursor.execute(check_credentials_query, check_credentials_data)
# #         if len((mycursor.fetchall())) > 0:
# #             string = "Credentials match."
# #             return string, True
# #         else:
# #             string = "Credentials do not match."
# #             return string, False
# #         # if query.exec():
# #         #     # Check if there's at least one row in the result set
# #         #     if query.next():
# #         #         #            print("Credentials match.")
# #         #         return "Credentials match.", True
# #         #     else:
# #         #         #            print("Credentials do not match.")
# #         #         return "Credentials do not match.", False
# #         # else:
# #         #     string = "Error checking credentials:" + query.lastError().text()
# #         #     #            print(string)
# #         #     return string, False
#
#
# # # if __name__ == "__main__":
# # db = sqldatabase()
# # db.initializeDatabase()
# # db.createTable()
# # db.insertData("admin", "admin", "admin@email.com", "admin")
# # db.insertData("user", "user", "user@email.com", "user")
# # # print(db.checkCredentials("admin", "admin"))
# # # print(db.getEmail("admin"))
#
#
# # # db.getRole("admin")
