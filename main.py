import os
import sys
from PyQt6.QtWidgets import QApplication
from core.exception.exceptions import NoSettingsFilePresent, NoTemplateFilePresent

#paths = ["settings.json", "operators/zong/template.json"]
paths = ["settings.json"]

def files_exist(path_str: str):
    try:
        print("Checking necessary files...")
        result = [False, False]
        for index, path in enumerate(path_str):
            if not os.path.isfile(path):
                result[index] = False
            else:
                result[index] = True
            print("Required file {} is present!{}".format(path, result[index]))
        return all(result)

    except Exception as error:
        print("Error reading Files!", error)


def run():
    try:
        #if files_exist(paths):
        if True:
            from gui.source import MainWindow
            app = QApplication(sys.argv)
            credentials = {"name": "admin", "privileges": "admin"}
            win = MainWindow(**credentials)
            win.show()
            sys.exit(app.exec())
        else:
            raise NoSettingsFilePresent("No Settings File Present")
    except Exception as e:
        print(e)
    except NoSettingsFilePresent:
        print("No Settings File Present")
    except NoTemplateFilePresent:
        print("No Template File Present")

if __name__ == "__main__":
    run()
