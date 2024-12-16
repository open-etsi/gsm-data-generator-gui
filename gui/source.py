import datetime
import json
import os
import time

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QLineEdit,
    QMessageBox,
    QDialog,
)

from globals.parameters import Parameters, DataFrames
from globals.settings import SETTINGS

from gui.forms.main_ui import Ui_MainWindow
from gui.forms.login_ui import Ui_Form as login_form
from gui.screens import PreviewOutput
from gui.messages import show_message_box
from gui.table import GuiElect, GuiGraph, GuiExtractor
from gui.controller.ulits import GuiButtons, GuiCheckBox, TextLengthValidator
from gui.controller.controller import Controller
from core.executor.utils import read_json, list_2_dict
from core.parser.utils import json_loader, gui_loader, json_loader1
from core.executor.script import DataGenerationScript

debug = False
STC_ICON = "resources/stc_logo.ico"


class MainWindow(QMainWindow):
    project_path = os.getcwd()

    def __init__(self, *args, **kwargs):
        (laser_ext_path, headers_data_dict, headers_laser_dict, header_server_dict) = (None, None, None, None)
        super(MainWindow, self).__init__()
        self.config_holder = None
        self.global_elect_check = None
        self.default_graph = None
        self.default_elect = None
        self.e_combo_box = None
        self.source_widget = None
        self.target_widget = None
        self.combo_box = None
        self.global_prod_check = None
        self.global_graph_check = None
        self.w = None
        user_name = kwargs.get("name")
        user_role = kwargs.get("privileges")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        # self.setAttribute(
        #     Qt.WidgetAttribute.WA_DeleteOnClose
        # )  # to handle timer issues upon exiting app

        self.ui.textEdit.setFontFamily("Cascadia Mono")
        self.ui.textEdit.setFontPointSize(10)
        self.setWindowIcon(QIcon(STC_ICON))
        self.parameters = Parameters.get_instance()
        self.dataframes = DataFrames.get_instance()

        self.sett = SETTINGS(self.ui)

        #        self.elect_gui = GuiElect(self.ui)
        #        self.graph_gui = GuiGraph(self.ui)
        #        self.button_gui = GuiButtons(self.ui)
        #        self.checkbox_gui = GuiCheckBox(self.ui)
        #        self.extractor_gui = GuiExtractor(self.ui)
        self.text_validator = TextLengthValidator(self.ui)

        self.controller = Controller(self.ui)

        self.user_privileges = user_role
        self.ui.lbl_username.setText(user_name)
        self.ui.lbl_userrole.setText(user_role)

        # this must not be here | remove in revision

        # data = read_json("settings.json")
        # if data:
        #     header_server_dict = list_2_dict(data["PARAMETERS"]["server_variables"])
        #     headers_laser_dict = data["PARAMETERS"]["laser_variables"]
        #     headers_data_dict = list_2_dict(data["PARAMETERS"]["data_variables"])
        #     laser_ext_path = data["PATHS"]["OUTPUT_FILES_LASER_EXT"]
        #
        # self.parameters.set_LASER_EXT_PATH(laser_ext_path)
        # self.parameters.set_ELECT_DICT(headers_data_dict)
        # self.parameters.set_GRAPH_DICT(headers_laser_dict)
        # self.parameters.set_SERVER_DICT(header_server_dict)

        # ==========================================#
        # ============DEFAULT VALUES================#
        # ==========================================#
        self.input_path = ""
        self.default_transport_key = (
            "0C556CE733FA0E53FE2DCF14A5006D2E0C556CE733FA0E53FE2DCF14A5006D2E"
        )
        # default values
        self.default_operator_key = "0C556CE733FA0E53FE2DCF14A5006D2E"

        # Move To Controller Class
        self.ui.main_generate.clicked.connect(self.main_generate_function)
        self.ui.main_save.clicked.connect(self.save_files_function)
        self.ui.browse_button.clicked.connect(self.browse_button_func)
        self.ui.preview_in_file.clicked.connect(self.show_input_files)
        self.ui.save_seting_button.clicked.connect(self.save_settings_func)
        self.ui.load_seting_button.clicked.connect(self.load_settings_func)

    extractor_columns = []

    def save_settings_func(self):
        self.controller.gui_to_global_params()
        self.sett.save_global_params_to_settings()

        self.ui.textEdit.clear()
        self.progress_bar()
        show_message_box("Information", "Settings saved successfully.")
        self.progress_bar_init()
        self.ui.textEdit.append("Settings Saved!")

    def load_settings_func(self):
        self.sett.load_settings_to_global()
        self.sett.set_gui_from_settings()

        self.progress_bar()
        show_message_box("Information", "Settings Loaded successfully.")
        self.progress_bar_init()
        self.ui.textEdit.clear()
        self.ui.textEdit.append("Settings Loaded!")

    #         self.ui.demo_data.setChecked(self.parameters.get_DEMO_CHECK())
    #         self.ui.elect_data.setChecked(self.parameters.get_ELECT_CHECK())
    #         self.ui.graph_data.setChecked(self.parameters.get_GRAPH_CHECK())

    # def extractor_function(self, dest, src):
    #     print(self.dataframes._INPUT_DF)

    @staticmethod
    def create_folder(folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def main_generate_function(self):
        self.ui.textEdit.clear()
        #        self.update_all()
        #        temp = self.parameters.get_all_params_dict()
        #        print("----->", temp)
        try:
            self.controller.gui_to_global_params()
            t = self.controller.global_params_to_json()
            c = json_loader1(t)
            d = DataGenerationScript(c)
            d.json_to_global_params()
            (dfs, keys) = d.generate_all_data()

            # print("-----> ", self.parameters.get_SERVER_DICT())
            # print("-----> ", self.parameters.get_SERVER_CHECK())
            self.dataframes.ELECT_DF = dfs["ELECT"]
            self.dataframes.GRAPH_DF = dfs["GRAPH"]
            self.dataframes.SERVER_DF = dfs["SERVER"]

            print("-----> ", self.parameters.get_ELECT_CHECK(), self.parameters.get_GRAPH_CHECK(),
                  self.parameters.get_SERVER_CHECK())
            #            print("------------------------------------>", dfs["SERVER"])

            show_message_box("Information", "Data has been generated successfully.")

        except Exception as e:
            self.ui.textEdit.clear()
            self.ui.textEdit.append("--->")
            self.ui.textEdit.append(str(e))

        if self.parameters.check_params():
            pass
            #            try:
            # s = DataGenerationScript()
            # (
            #     self.dataframes.__ELECT_DF,
            #     self.dataframes.__GRAPH_DF,
            #     self.dataframes.__SERVR_DF,
            #     self.dataframes.__KEYS,
            # ) = s._preview_files_gets()
            # print("data generated")

        #     if self.user_privileges == "admin":
        #         self.progress_bar()
        #         show_message_box(
        #             "Information", "Data has been generated successfully."
        #         )
        #         self.progress_bar_init()
        try:
            print(self.dataframes.ELECT_DF)

            self.w = PreviewOutput(
                self.dataframes.ELECT_DF,
                self.dataframes.GRAPH_DF,
                self.dataframes.SERVER_DF,
                self.parameters.get_ELECT_CHECK(),
                self.parameters.get_GRAPH_CHECK(),
                self.parameters.get_SERVER_CHECK()
            )
            self.w.show()
        except Exception as e:
            #            self.ui.textEdit.clear()
            self.ui.textEdit.append("===>")
            self.ui.textEdit.append(str(e))
        #
        #     else:
        #         show_message_box(
        #             "Information",
        #             "Data has been generated successfully.\nHowever, access to view this data is restricted to "
        #             "administrators only.\nPlease click the 'SAVE' to save the files in the designated directory."
        #             # "Data is generated but only admin has access to view data\nPress GENERATE to save files in
        #             # DIR",
        #         )
        # #            except Exception as e:
        # #                messageBox.Show_message_box(
        # #                    "Error", "Error! Maybe Input file is missing..."
        # #                )
        # #                self.ui.textEdit.append("Error! Maybe Input file is missing...")
        # #                self.ui.textEdit.append(str(e))
        # else:
        #     show_message_box("Error", " Check Missing Input Parameters...")

    def create_output_folder(self):
        try:

            parent_folder = self.parameters.get_OUTPUT_FILES_DIR()
            sub_folder = self.parameters.get_file_name()
            nested_folder = os.path.join(parent_folder, sub_folder)
            os.makedirs(nested_folder, exist_ok=True)

            elect_com_path = nested_folder + "/DATA_{}.txt".format(self.parameters.get_file_name())
            graph_com_path = nested_folder + "/LASER_{}.txt".format(self.parameters.get_file_name())
            server_com_path = nested_folder + "/{}.out".format(self.parameters.get_file_name())
            print(elect_com_path)
            print(self.parameters.get_OUTPUT_FILES_DIR())

            #            os.makedirs(self.parameters.get_OUTPUT_FILES_DIR(), exist_ok=True)
            if self.parameters.get_ELECT_CHECK():
                self.dataframes.get_ELECT_DF().to_csv(elect_com_path, sep=self.parameters.get_ELECT_SEP(), index=False)
            if self.parameters.get_GRAPH_CHECK():
                self.dataframes.get_GRAPH_DF().to_csv(graph_com_path, sep=self.parameters.get_GRAPH_SEP(), index=False)
            if self.parameters.get_SERVER_CHECK():
                self.dataframes.get_SERVER_DF().to_csv(server_com_path, sep=self.parameters.get_SERVER_SEP(),
                                                       index=False)

        except Exception as e:
            self.ui.textEdit.append("===>", e)
        # m_zong = ZongFileWriter()
        # m_zong.set_json_to_UI()
        # m_zong.Generate_laser_file(
        #     dict_2_list(self.parameters.get_GRAPH_DICT()), self.dataframes.__GRAPH_DF
        # )
        # m_zong.Generate_servr_file(
        #     dict_2_list(self.parameters.get_SERVER_DICT()), self.dataframes.__SERVR_DF
        # )
        # m_zong.Generate_elect_file(
        #     dict_2_list(self.parameters.get_ELECT_DICT()), self.dataframes.__ELECT_DF
        # )

        # com_path = os.path.join(self.parameters.get_OUTPUT_FILES_DIR(),
        #                         "{}.txt".format(self.parameters.get_file_name()))
        #
        # show_message_box(
        #     "Information",
        #     "Generated Data has been saved to {} successfully.".format(com_path),
        # )
        #        self.progress_bar_init()

        self.ui.textEdit.append("==================================")
        #        self.ui.textEdit.append(f"Created folder '{folder_name}'")
        #        p_time = time.strftime("%H_%M_%S", time.localtime())
        #        p_date = datetime.date.today().strftime("%Y_%m_%d")
        #        date_time = f"{p_date}_{p_time}"

        # self.ui.textEdit.append(
        #     f"Directory Name: " + f'<a href="{com_path}" style="color: black;">{com_path}</a>'
        # )

        # self.ui.textEdit.append("Path: " + os.path.join(os.getcwd(), com_path))
        self.ui.textEdit.append("==================================")

    # def len_check(self, text, key_type, widget):
    #     var = int(parameter_len(text))
    #     if (var + 1) > len(key_type):
    #         widget.setStyleSheet(style_sheet_bad)
    #     else:
    #         widget.setStyleSheet(style_sheet_good)

    def browse_button_func(self):
        try:
            path = self.project_path
            path = os.path.join(path, "Json File")
            filters = "JSON (*.json)"

            fname, _ = QFileDialog.getOpenFileNames(self, "Load Json Input File", path, filter=filters)
            self.ui.textEdit.append(str(fname))
            if len(fname) != 0:
                self.ui.filename.setText(", ".join(fname))
                #            self.ui.textEdit.append(str(fname))
                self.ui.textEdit.append(f"Selected {len(fname)} file(s).")
                #            self.global_input_path=fname[0]
                #            self.parameters.set_INPUT_PATH(fname[0])
                self.parameters.set_INPUT_FILE_PATH(fname[0])

                self.config_holder = json_loader(fname[0])
        except Exception as e:
            self.ui.textEdit.append(str(e))
            # s = DataGenerationScript(config_holder=config_holder)
            # s.SET_ALL_DISP_PARAMS()  # testing
            # (dfs, keys) = s.generate_all_data()
            #
            # # print(s.generate_all_data())
            # print(dfs["ELECT"].to_csv("ELECT.csv"))
            # print(dfs["GRAPH"].to_csv("GRAPH.csv"))
            # print(dfs["SERVER"].to_csv("SERVER.csv"))

    def show_input_files(self):
        try:
            self.controller.json_to_global_params(self.config_holder, self.parameters)
            self.controller.global_params_to_gui(self.parameters)
        except Exception as e:
            print(e)
            self.ui.textEdit.append(str(e))

    def save_files_function(self):
        self.progress_bar()
        self.create_output_folder()

    def progress_bar(self):
        float_value = 0
        integer_value = 0
        while integer_value < 100:
            time.sleep(0.0001)
            float_value += 1
            integer_value = int(
                float_value
            )  # Map the float value to the 0-100 integer range
            self.ui.progressBar.setValue(integer_value)

    def progress_bar_init(self):
        self.ui.progressBar.setValue(0)

    def closeEvent(self, event):
        print("AUTOMATIC SETTING SAVED SUCCESSFULLY")

    def close(self):
        self.hide()


class LoginWindow(QDialog):
    credentials = None

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = login_form()
        self.ui.setupUi(self)
        self.ui.label.setPixmap(QPixmap(STC_ICON))

        self.setWindowIcon(QIcon(STC_ICON))
        self.setWindowTitle("Login Account")
        self.ui.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )  # This line sets the echo mode to Password

        self.ui.btn_login.clicked.connect(self.login)
        self.ui.btn_signup.setCheckable(True)

    def login(self):
        username = self.ui.username.text()
        password = self.ui.password.text()

        # success = False
        # result, success = self.conn.checkCredentials(
        #     username=username, password=password
        # )
        result, success = "admin", True

        if success:
            #            global user_role
            # user_role = self.conn.getRole(username=username)
            #            global user_name
            user_role = "admin"

            user_name = username
            credentials = {"name": user_name, "privileges": user_role}
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", result)
