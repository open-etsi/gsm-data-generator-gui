# from PyQt6.QtGui import QIcon, QPixmap
# from PyQt6.QtWidgets import (
#     QLineEdit,
#     QMessageBox,
#     QDialog,
# )
#
# from gui.messages import messageBox
# from gui.forms.login_ui import Ui_Form as login_form
# from gui.forms.signup_ui import Ui_Form as sign_up_form
# from gui.source import MainWindow
#
# STC_ICON = "resources/stc_logo.ico"
#
# class AppController(LoginWindow, MainWindow, SignUp):
#     def __init__(self):
#         pass
#
#     def login_screen(self):
#         win = LoginWindow()
#         win.exec()
#
#     def main_screen(self):
#         global credentials
#         win = MainWindow(**credentials)
#         win.show()
#
#     def signup_screen(self):
#         win = SignUp()
#         win.exec()
#
# class SignUp(QDialog, messageBox):
#     def __init__(self):
#         super(SignUp, self).__init__()
#         self.ui = sign_up_form()
#         self.ui.setupUi(self)
#         self.ui.label.setPixmap(QPixmap(STC_ICON))
#         #        self.db=database()
#
#         self.setWindowIcon(QIcon(STC_ICON))
#         self.setWindowTitle("Create Login Account")
#
#         #        self.conn = sqldatabase()
#         #        self.conn.initializeDatabase()
#
#         self.ui.btn_signup.clicked.connect(self.signup_2_login_func)
#         self.ui.btn_login.clicked.connect(self.createAccount)
#
#     def signup_2_login_func(self):
#         self.hide()
#         win = AppController()
#         win.login_screen()
#
#     #        win.signup_2_login()
#
#     @staticmethod
#     def Emailvalidator(email):
#         import re
#
#         regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
#         result = True if re.fullmatch(regex, email) else False
#         return result
#
#     def createAccount(self):
#         username = self.ui.username.text()
#         password = self.ui.password.text()
#         re_password = self.ui.re_password.text()
#         email = self.ui.email.text()
#
#         #        SignUp.Emailvalidator(email=email)
#
#         if SignUp.Emailvalidator(email=email) is False:
#             self.Show_message_box("Message", "Enter Valid Email")
#             return
#
#             # if password == re_password:
#             #     result, success = self.conn.insertData(
#             #         user_name=username,
#             #         user_pass=password,
#             #         user_email=email,
#             #         user_role="user",
#             #     )
#
#             # if success is True:
#             #     self.Show_message_box("Message", "Login Created Successfully")
#             #
#             # else:
#             #     self.Show_message_box("Message", result)
#
#         else:
#             self.Show_message_box("Message", "Password do not match!")
#
#     def close(self):
#         self.hide()
#
#
# # import qdarktheme
# # import sys
# # app = QApplication(sys.argv)
# # win = SignUp()
# # qdarktheme.setup_theme("dark")
# # win.show()
# # sys.exit(app.exec())
#
#
# class LoginWindow(QDialog, messageBox):
#     def __init__(self):
#         super(LoginWindow, self).__init__()
#         self.ui = login_form()
#         self.ui.setupUi(self)
#         self.ui.label.setPixmap(QPixmap(STC_ICON))
#
#         #        self.conn = sqldatabase()
#         #        self.conn.initializeDatabase()
#
#         self.setWindowIcon(QIcon(STC_ICON))
#         self.setWindowTitle("Login Account")
#         self.ui.password.setEchoMode(
#             QLineEdit.EchoMode.Password
#         )  # This line sets the echo mode to Password
#
#         self.ui.btn_login.clicked.connect(self.login)
#         self.ui.btn_signup.setCheckable(True)
#         self.ui.btn_signup.clicked.connect(self.sign_up_form)
#
#     def login(self):
#         username = self.ui.username.text()
#         password = self.ui.password.text()
#
#         # success = False
#         # result, success = self.conn.checkCredentials(
#         #     username=username, password=password
#         # )
#         result, success = "admin", True
#
#         if success:
#             #            global user_role
#             # user_role = self.conn.getRole(username=username)
#             #            global user_name
#             user_role = "admin"
#
#             user_name = username
#             global credentials
#             credentials = {"name": user_name, "privilidges": user_role}
#             self.accept()
#             self.main_form()
#         else:
#             QMessageBox.warning(self, "Login Failed", result)
#
#     def sign_up_form(self):
#         self.hide()
#         win = AppController()
#         win.signup_screen()
#         # self.Show_message_box("Alert", "Signup option is unavailable!")
#         del win
#
#     def main_form(self):
#         win = AppController()
#         win.main_screen()
#         del win
#
#
