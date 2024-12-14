from typing import Annotated

from PyQt6.QtWidgets import QMessageBox, QStatusBar
from PyQt6.QtGui import QIcon


stc_icon = "resources/style/icons/stc_logo.ico"


def status(message: Annotated[str, "Enter Message"])->None:
    QStatusBar().showMessage(message=message)



def show_message_box(title, message) -> None:
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.setWindowIcon(QIcon(stc_icon))
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    temp = message_box.exec()
    if temp == QMessageBox.StandardButton.Ok:
        del message_box

def logout_message_box(title, message) -> bool:
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.setWindowIcon(QIcon(stc_icon))
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    temp = message_box.exec()
    if temp == QMessageBox.StandardButton.Yes:
        return True
    else:
        return False

def signup_message_box(cls, title, message) -> bool:
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Icon.Information)
    message_box.setWindowIcon(QIcon(stc_icon))
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
    temp = message_box.exec()
    if temp == QMessageBox.StandardButton.Yes:
        return True
    else:
        return False
