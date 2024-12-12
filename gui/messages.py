from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon


stc_icon = "resources/style/icons/stc_logo.ico"


class messageBox:
    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def Show_message_box(cls, title, message) -> None:
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setWindowIcon(QIcon(stc_icon))
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        temp = message_box.exec()
        if temp == QMessageBox.StandardButton.Ok:
            del message_box

    @classmethod
    def Logout_message_box(cls, title, message) -> bool:
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setWindowIcon(QIcon(stc_icon))
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        temp = message_box.exec()
        #        del message_box
        if temp == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    @classmethod
    def Signup_message_box(cls, title, message) -> bool:
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setWindowIcon(QIcon(stc_icon))
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        temp = message_box.exec()
        #        del message_box
        if temp == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False
