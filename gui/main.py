import os
import sys
from PyQt6.QtWidgets import QApplication
# from core.exceptions import NoSettingsFilePresent, NoTemplateFilePresent

paths = ["settings.json", "operators/zong/template.json"]

def files_exist(paths):
    try:
        print("Checking necessary files...")
        result = [False, False]
        for index, path in enumerate(paths):
            if not os.path.isfile(path):
                result[index] = False
            else:
                result[index] = True
            print("Required file {} is present!{}".format(path, result[index]))
        return all(result)

    except Exception:
        print("Error reading Files!")


def run():
#    try:
        #if files_exist(paths):
        if True:
            from source import AppController, MainWindow
            app = QApplication(sys.argv)
            credentials = {"name": "admin", "privileges": "admin"}
            win = MainWindow(**credentials)
            win.show()
#            win = AppController()
#            win.login_screen()
            sys.exit(app.exec())
    #        else:
    #            raise NoSettingsFilePresent("No Settings File Present")
#    except Exception as e:
#        print(e)
    # except NoSettingsFilePresent:
    #     print("No Settings File Present")
    # except NoTemplateFilePresent:
    #     print("No Template File Present")

if __name__ == "__main__":
    run()
