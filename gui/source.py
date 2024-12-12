import datetime
import os
import time

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QTableWidgetItem,
    QMainWindow,
    QLineEdit,
    QMessageBox,
    QDialog,
)

from globals.parameters import PARAMETERS, DATA_FRAMES
from gui.screens import PreviewInput, PreviewOutput
from gui.messages import messageBox

# from datagen.operators.zong.FileWriter import ZongFileWriter
# from datagen.operators.zong.FileParser import ZongFileParser
#from core.json_utils import JsonHandler
#from core.settings import SETTINGS
from gui.settings import SETTINGS
from gui.styleSheets import style_sheet_good, style_sheet_bad, style_sheet_disabled
from gui.forms.main_ui import Ui_MainWindow
from gui.forms.login_ui import Ui_Form as login_form
#from gui.forms import Ui_Form as sign_up_form


debug = False
STC_ICON = "resources/style/icons/stc_logo.ico"
# CONFIGURATION_FILE_PATH = "settings.json"


class MainWindow(QMainWindow):
    project_path = os.getcwd()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
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
        user_role = kwargs.get("privilidges")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setAttribute(
            Qt.WidgetAttribute.WA_DeleteOnClose
        )  # to handle timer issues upon exiting app

        self.ui.textEdit.setFontFamily("Cascadia Mono")
        self.ui.textEdit.setFontPointSize(10)
        self.setWindowIcon(QIcon(STC_ICON))
        self.parameters = PARAMETERS.get_instance()
        self.dataframes = DATA_FRAMES.get_instance()
        self.sett = SETTINGS()
        #        self.sec = messageBox()

#        self.m_json = JsonHandler()
#        self.m_json.read_paths()
#        self.m_json.read_variables()
        #        data_generator_instance = DataGenerationScript()
        #        self.ui.textEdit.append(data_generator_instance.SET_HEADERS())
        #        del data_generator_instance

        self.user_privilges = user_role
        self.ui.lbl_username.setText(user_name)
        self.ui.lbl_userrole.setText(user_role)
        self.ui.btn_logout.clicked.connect(self.logout_func)

        # this must not be here | remove in revision

        # m_zong = ZongGenerateHandle()
        # m_zong.set_json_to_UI()
        # data = read_json(CONFIGURATION_FILE_PATH)
        # if data:
        #     header_server_dict = list_2_dict(data["PARAMETERS"]["server_variables"])
        #     headers_laser_dict = data["PARAMETERS"]["laser_variables"]
        #     headers_data_dict = list_2_dict(data["PARAMETERS"]["data_variables"])
        #     laser_ext_path = data["PATHS"]["OUTPUT_FILES_LASER_EXT"]

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
        self.default_init_imsi = 789000000000000
        self.default_init_iccid = 899222333444555000
        self.default_PIN1 = "1234"
        self.default_data_size = 25
        self.default_elect_check = True
        self.default_graph_check = True
        self.default_prod_check = True

        # self.default_headers = [
        #     "ICCID",
        #     "IMSI",
        #     "PIN1",
        #     "PUK1",
        #     "PIN2",
        #     "PUK2",
        #     "KI",
        #     "EKI",
        #     "OPC",
        #     "ADM1",
        #     "ADM6",
        #     "ACC",
        # ]

        # self.parameters.set_ELECT_CHECK(self.default_elect_check)
        # self.parameters.set_GRAPH_CHECK(self.default_graph_check)
        # self.parameters.set_PRODUCTION_CHECK(self.default_prod_check)
        # self.parameters.set_DEFAULT_HEADER(self.default_headers)

        tableWidgetHeader = ["Variables", "Clip", "length"]
        self.ui.tableWidget.setHorizontalHeaderLabels(tableWidgetHeader)
        self.ui.e_tableWidget.setHorizontalHeaderLabels(tableWidgetHeader)
        self.ui.de_tableWidget.setHorizontalHeaderLabels(tableWidgetHeader)
        self.ui.de_comboBox.addItems(self.extractor_columns)

        self.ui.main_generate.clicked.connect(self.main_generate_function)
        self.ui.main_save.clicked.connect(self.save_files_function)

        self.ui.production_data.setChecked(self.default_prod_check)
        self.ui.elect_data.setChecked(self.default_elect_check)
        self.ui.graph_data.setChecked(self.default_graph_check)
        self.ui.server_data.setChecked(True)

        self.ui.add_text.clicked.connect(self.add_text_to_table)
        self.ui.del_text.clicked.connect(self.delete_selected_row)
        self.ui.up_button.clicked.connect(self.move_selected_row_up)
        self.ui.dn_button.clicked.connect(self.move_selected_row_down)
        self.ui.g_default.clicked.connect(self.g_setDefault)
        self.ui.g_save.clicked.connect(self.g_getDefault)

        self.ui.e_add_text.clicked.connect(self.e_add_text_to_table)
        self.ui.e_del_text.clicked.connect(self.e_delete_selected_row)
        self.ui.e_up_button.clicked.connect(self.e_move_selected_row_up)
        self.ui.e_dn_button.clicked.connect(self.e_move_selected_row_down)
        self.ui.e_default.clicked.connect(self.e_setDefault)
        self.ui.e_save.clicked.connect(self.e_getDefault)

        self.ui.browse_button.clicked.connect(self.browse_button_func)
        self.ui.preview_in_file.clicked.connect(self.show_input_files)

        self.ui.graph_data.stateChanged.connect(self.check_state_changed)
        self.ui.elect_data.stateChanged.connect(self.check_state_changed)
        self.ui.server_data.stateChanged.connect(self.check_state_changed)
        self.check_state_changed()

        self.ui.production_data.stateChanged.connect(self.check_state_prod_data)
        self.check_state_prod_data()

        self.ui.op_key_auto.clicked.connect(self.auto_op_func)
        self.ui.k4_key_auto.clicked.connect(self.auto_k4_func)
        self.ui.op_key_fetch.clicked.connect(self.fetch_op_func)
        self.ui.k4_key_fetch.clicked.connect(self.fetch_k4_func)
        self.ui.data_size_auto.clicked.connect(self.auto_data_size_func)
        self.ui.imsi_auto.clicked.connect(self.auto_imsi_func)
        self.ui.iccid_auto.clicked.connect(self.auto_iccid_func)

        self.ui.k4_key_text.textChanged.connect(
            lambda: self.len_check(
                "K4", self.ui.k4_key_text.text(), self.ui.k4_key_text
            )
        )
        self.ui.op_key_text.textChanged.connect(
            lambda: self.len_check(
                "OP", self.ui.op_key_text.text(), self.ui.op_key_text
            )
        )
        self.ui.data_size_text.textChanged.connect(
            lambda: self.len_check(
                "SIZE", self.ui.data_size_text.text(), self.ui.data_size_text
            )
        )
        self.ui.imsi_text.textChanged.connect(
            lambda: self.len_check("IMSI", self.ui.imsi_text.text(), self.ui.imsi_text)
        )
        self.ui.iccid_text.textChanged.connect(
            lambda: self.len_check(
                "ICCID_MIN", self.ui.iccid_text.text(), self.ui.iccid_text
            )
        )
        self.ui.pin1_text.textChanged.connect(
            lambda: self.len_check("PIN1", self.ui.pin1_text.text(), self.ui.pin1_text)
        )
        self.ui.pin2_text.textChanged.connect(
            lambda: self.len_check("PIN2", self.ui.pin2_text.text(), self.ui.pin2_text)
        )
        self.ui.puk1_text.textChanged.connect(
            lambda: self.len_check("PUK1", self.ui.puk1_text.text(), self.ui.puk1_text)
        )
        self.ui.puk2_text.textChanged.connect(
            lambda: self.len_check("PUK2", self.ui.puk2_text.text(), self.ui.puk2_text)
        )
        self.ui.adm1_text.textChanged.connect(
            lambda: self.len_check("ADM1", self.ui.adm1_text.text(), self.ui.adm1_text)
        )
        self.ui.adm6_text.textChanged.connect(
            lambda: self.len_check("ADM6", self.ui.adm6_text.text(), self.ui.adm6_text)
        )

        self.ui.pin1_rand_check.stateChanged.connect(self.pin1_rand_check)
        self.ui.pin2_rand_check.stateChanged.connect(self.pin2_rand_check)
        self.ui.puk1_rand_check.stateChanged.connect(self.puk1_rand_check)
        self.ui.puk2_rand_check.stateChanged.connect(self.puk2_rand_check)
        self.ui.adm1_rand_check.stateChanged.connect(self.adm1_rand_check)
        self.ui.adm6_rand_check.stateChanged.connect(self.adm6_rand_check)

        self.ui.pin1_auto.clicked.connect(self.auto_pin1_func)
        self.ui.pin2_auto.clicked.connect(self.auto_pin2_func)
        self.ui.puk1_auto.clicked.connect(self.auto_puk1_func)
        self.ui.puk2_auto.clicked.connect(self.auto_puk2_func)
        self.ui.adm1_auto.clicked.connect(self.auto_adm1_func)
        self.ui.adm6_auto.clicked.connect(self.auto_adm6_func)

        self.ui.save_seting_button.clicked.connect(self.save_settings_func)
        self.ui.load_seting_button.clicked.connect(self.load_settings_func)

        self.ui.de_browse_button.clicked.connect(self.de_browse_button_func)
        self.ui.de_preview_in_file.clicked.connect(self.de_show_input_files)

        self.ui.de_add_text.clicked.connect(self.de_add_text_to_table)
        self.ui.de_del_text.clicked.connect(self.de_delete_selected_row)
        self.ui.de_up_button.clicked.connect(self.de_move_selected_row_up)
        self.ui.de_dn_button.clicked.connect(self.de_move_selected_row_down)
        self.ui.de_default.clicked.connect(self.de_setDefault)

        self.ui.de_main_preview.clicked.connect(self.de_main_generate_function)
        self.ui.de_generate_button.clicked.connect(self.de_save_files_function)

    extractor_columns = []

    def save_settings_func(self):
        self.UPDATE_ALL()
        #        self.parameters.print_all_global_parameters()
        self.sett.save_settings()
        self.ui.textEdit.clear()
        self.progress_bar()
        messageBox.Show_message_box("Information", "Settings saved successfully.")
        self.progress_bar_init()
        self.ui.textEdit.append("Settings Saved!")

    def load_settings_func(self):
        self.sett.load_settings()
        #         self.parameters.print_all_global_parameters()
        self.SET_ALL_FROM_SETT()
        self.progress_bar()
        messageBox.Show_message_box("Information", "Settings Loaded successfully.")
        self.progress_bar_init()
        self.ui.textEdit.clear()
        self.ui.textEdit.append("Settings Loaded!")

    #         self.ui.demo_data.setChecked(self.parameters.get_DEMO_CHECK())
    #         self.ui.elect_data.setChecked(self.parameters.get_ELECT_CHECK())
    #         self.ui.graph_data.setChecked(self.parameters.get_GRAPH_CHECK())
    @staticmethod
    def is_valid_iccid(iccid):
        iccid_length = len(str(iccid))
        return iccid_length in [18, 19, 20]

    @staticmethod
    def is_valid_imsi(imsi):
        return len(str(imsi)) == 15

    def extractor_function(self, dest, src):
        print(self.dataframes._INPUT_DF)

    @staticmethod
    def parameter_len(param):
        """Function printing python version."""
        length = 0
        # fmt: off

        match param:
            case "ICCID_MIN":
                length = 18
            case "ICCID":
                length = 20
            case "IMSI":
                length = 15
            case "PIN1" | "PIN2" | "ACC":
                length = 4
            case "PUK1" | "PUK2" | "ADM1" | "ADM6":
                length = 8
            case "KI" | "EKI" | "OPC":
                length = 32
            case "K4":
                length = 64
            case "SIZE":
                length = 1
            case _:
                length = 32
        return str(length - 1)

    @staticmethod
    def create_folder(folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def logout_func(self):
        self.close()
        app_controller = AppController()
        result = messageBox.Logout_message_box(
            "Logged Out", "You have successfully logged out! \n Proceed to Login?"
        )
        if result:
            app_controller.login_screen()
        else:
            exit()

    def update_pin1_text(self):
        var = self.ui.pin1_text.text()
        if len(var) == 4:
            self.parameters.set_PIN1(var)
        else:
            self.parameters.set_PIN1("")
            self.ui.textEdit.append("Enter valid PIN1")

    def update_pin2_text(self):
        var = self.ui.pin2_text.text()
        if len(var) == 4:
            self.parameters.set_PIN2(var)
        else:
            self.parameters.set_PIN2("")
            self.ui.textEdit.append("Enter valid PIN2")

    def update_puk1_text(self):
        var = self.ui.puk1_text.text()
        if len(var) == 8:
            self.parameters.set_PUK1(var)
        else:
            self.parameters.set_PUK1("")
            self.ui.textEdit.append("Enter valid PUK1")

    def update_puk2_text(self):
        var = self.ui.puk2_text.text()
        if len(var) == 8:
            self.parameters.set_PUK2(var)
        else:
            self.parameters.set_PUK2("")
            self.ui.textEdit.append("Enter valid PUK2")

    def update_adm1_text(self):
        var = self.ui.adm1_text.text()
        if len(var) == 8:
            self.parameters.set_ADM1(var)
        else:
            self.parameters.set_ADM1("")
            self.ui.textEdit.append("Enter valid ADM1")

    def update_adm6_text(self):
        var = self.ui.adm6_text.text()
        if len(var) == 8:
            self.parameters.set_ADM6(var)
        else:
            self.parameters.set_ADM6("")
            self.ui.textEdit.append("Enter valid ADM6")

    def auto_pin1_func(self):
        # string = generate_4_Digit()
        string = "0000"
        self.ui.pin1_text.setText(string)

    def pin1_rand_check(self):
        if self.ui.pin1_rand_check.isChecked():
            self.parameters.set_PIN1_RAND(True)
        else:
            self.parameters.set_PIN1_RAND(False)

    def auto_pin2_func(self):
#        string = generate_4_Digit()
        string = "0000"
        self.ui.pin2_text.setText(string)

    def pin2_rand_check(self):
        if self.ui.pin2_rand_check.isChecked():
            self.parameters.set_PIN2_RAND(True)
        else:
            self.parameters.set_PIN2_RAND(False)

    def auto_puk1_func(self):
#        string = generate_8_Digit()
        string = "00000000"
        self.ui.puk1_text.setText(string)

    def puk1_rand_check(self):
        if self.ui.puk1_rand_check.isChecked():
            self.parameters.set_PUK1_RAND(True)
        else:
            self.parameters.set_PUK1_RAND(False)

    def auto_puk2_func(self):
#        string = generate_8_Digit()
        string = "00000000"
        self.ui.puk2_text.setText(string)

    def puk2_rand_check(self):
        if self.ui.puk2_rand_check.isChecked():
            self.parameters.set_PUK2_RAND(True)
        else:
            self.parameters.set_PUK2_RAND(False)

    def auto_adm1_func(self):
#        string = generate_8_Digit()
        string = "00000000"
        self.ui.adm1_text.setText(string)

    def adm1_rand_check(self):
        if self.ui.adm1_rand_check.isChecked():
            self.parameters.set_ADM1_RAND(True)
        else:
            self.parameters.set_ADM1_RAND(False)

    def auto_adm6_func(self):
#        string = generate_8_Digit()
        string = "00000000"
        self.ui.adm6_text.setText(string)

    def adm6_rand_check(self):
        if self.ui.adm6_rand_check.isChecked():
            self.parameters.set_ADM6_RAND(True)
        else:
            self.parameters.set_ADM6_RAND(False)

    def SET_ALL_FROM_SETT(self):
        self.ui.imsi_text.setText(self.parameters.get_IMSI())
        self.ui.iccid_text.setText(self.parameters.get_ICCID())
        self.ui.pin1_text.setText(self.parameters.get_PIN1())
        self.ui.puk1_text.setText(self.parameters.get_PUK1())
        self.ui.pin2_text.setText(self.parameters.get_PIN2())
        self.ui.puk2_text.setText(self.parameters.get_PUK2())
        self.ui.adm1_text.setText(self.parameters.get_ADM1())
        self.ui.adm6_text.setText(self.parameters.get_ADM6())
        self.ui.k4_key_text.setText(self.parameters.get_K4())
        self.ui.op_key_text.setText(self.parameters.get_OP())
        self.ui.data_size_text.setText(self.parameters.get_DATA_SIZE())
        self.ui.pin1_rand_check.setChecked(bool(self.parameters.get_PIN1_RAND()))
        self.ui.pin2_rand_check.setChecked(bool(self.parameters.get_PIN2_RAND()))
        self.ui.puk1_rand_check.setChecked(bool(self.parameters.get_PUK1_RAND()))
        self.ui.puk2_rand_check.setChecked(bool(self.parameters.get_PUK2_RAND()))
        self.ui.adm1_rand_check.setChecked(bool(self.parameters.get_ADM1_RAND()))
        self.ui.adm6_rand_check.setChecked(bool(self.parameters.get_ADM6_RAND()))

    def UPDATE_ALL(self):
        if self.ui.production_data.isChecked() is False:
            self.get_iccid_func()
            self.get_imsi_func()
            self.get_data_size_func()

        self.pin1_rand_check()
        self.pin2_rand_check()
        self.puk1_rand_check()
        self.puk2_rand_check()
        self.adm1_rand_check()
        self.adm6_rand_check()

        self.update_pin1_text()
        self.update_pin2_text()
        self.update_puk1_text()
        self.update_puk2_text()
        self.update_adm1_text()
        self.update_adm6_text()

        self.get_k4_func()
        self.get_op_func()

    def g_setDefault(self):
        d = self.parameters.get_GRAPH_DICT()
        for items in d:
            self.g_table_append(d[items][0], d[items][2])

    def g_getDefault(self):
        self.default_graph = self.get_data_from_table()
        # print(str(self.default_graph))

    def main_generate_function(self):
        self.ui.textEdit.clear()
        # debug = False
        self.UPDATE_ALL()

        self.ui.textEdit.append("==================================")
        if debug:
            self.ui.textEdit.append("=============DEBUG================")
            temp = self.parameters.GET_ALL_PARAMS_DICT()
            self.ui.textEdit.append(str(temp))

        self.ui.textEdit.append("==================================")

        self.parameters.set_GRAPH_DICT(self.get_data_from_table())
        self.parameters.set_ELECT_DICT(self.e_get_data_from_table())
        #        self.parameters.set_SERVER_DICT(header_server_dict)

        #        self.parameters.dict1 is test dictionary
        if self.parameters.check_params():
            #            try:
            # s = DataGenerationScript()
            # (
            #     self.dataframes.__ELECT_DF,
            #     self.dataframes.__GRAPH_DF,
            #     self.dataframes.__SERVR_DF,
            #     self.dataframes.__KEYS,
            # ) = s._preview_files_gets()
            # print("data generated")

            if self.user_privilges == "admin":
                self.progress_bar()
                messageBox.Show_message_box(
                    "Information", "Data has been generated successfully."
                )
                self.progress_bar_init()
                self.w = PreviewOutput(
                    self.dataframes.__ELECT_DF,
                    self.dataframes.__GRAPH_DF,
                    self.dataframes.__SERVR_DF,
                    True,
                    False,
                    True,
                )
                self.w.show()

            else:
                messageBox.Show_message_box(
                    "Information",
                    "Data has been generated successfully.\nHowever, access to view this data is restricted to "
                    "administrators only.\nPlease click the 'SAVE' to save the files in the designated directory."
                    # "Data is generated but only admin has access to view data\nPress GENERATE to save files in
                    # DIR",
                )
        #            except Exception as e:
        #                messageBox.Show_message_box(
        #                    "Error", "Error! Maybe Input file is missing..."
        #                )
        #                self.ui.textEdit.append("Error! Maybe Input file is missing...")
        #                self.ui.textEdit.append(str(e))
        else:
            messageBox.Show_message_box("Error", " Check Missing Input Parameters...")

    def de_main_generate_function(self):
        self.ui.de_textEdit.clear()
        # debug = True
        # self.UPDATE_ALL()

        self.ui.de_textEdit.append("==================================")
        if debug:
            self.ui.de_textEdit.append("=============DEBUG================")
        #            temp=self.parameters.GET_ALL_PARAMS_DICT()
        #            self.ui.textEdit.append(str(temp))

        self.ui.de_textEdit.append("==================================")

        #        laser=self.get_data_from_table()
        #        elect=self.e_get_data_from_table()
        try:
            # elect = {}  # initialize
            elect = self.de_get_data_from_table()
            self.ui.de_textEdit.append(str(elect))

            self.parameters.set_EXTRACTOR_DICT(self.de_get_data_from_table())
            # s = DataGenerationScript()
            # #            if self.parameters.check_params():
            # self.dataframes._GRAPH_DF = s.__LASER_DATA_EXTRACTOR(
            #     elect, self.dataframes._INPUT_DF, True, True, ""
            # )
            # self.w = PreviewInput(self.dataframes._GRAPH_DF)
            # self.w.show()

            # print(self.dataframes._GRAPH_DF)
        except KeyError:
            self.ui.de_textEdit.append(
                "Error : Check Input File Format \n It should be encoded and space seperated Only"
            )

    def create_output_folder(self):
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

        # com_path = os.path.join(m_zong.get_output_dir())
        # messageBox.Show_message_box(
        #     "Information",
        #     "Generated Data has been saved to {} successfully.".format(com_path),
        # )
        # self.progress_bar_init()

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

    def len_check(self, text, key_type, widget):
        var = int(self.parameter_len(text))
        if (var + 1) > len(key_type):
            widget.setStyleSheet(style_sheet_bad)
        else:
            widget.setStyleSheet(style_sheet_good)

    # def read_json(file_path: str):
    #     with open(file_path, "r") as json_file:
    #         data = json.load(json_file)
    #     return dict(data)

    def fetch_op_func(self):
        try:
            # Define the path to the JSON file
            path = "keys.json"

            # Check if the file exists
            if os.path.isfile(path):
                # Read the JSON file
#                keys = read_json(path)
                keys = {"op": "55555555555555555555555555555555","k4": "6666666666666666666666666666666666666666666666666666666666666666"}
                # Check if the JSON is not empty
                if keys:
                    op_key = keys.get("op")
                    if len(op_key) == 32:
                        # Set the op_key_text field in the UI
                        self.ui.op_key_text.setText(str(op_key))
                        self.statusBar().showMessage(
                            "Loaded OP sucessfully :{} Length : {}".format(
                                op_key, len(op_key)
                            ),
                            2000,
                        )
                    else:
                        self.ui.textEdit.append("length of OP is invalid!")
                        self.statusBar().showMessage(
                            "Loaded OP Error ! :{} Length : {}".format(
                                op_key, len(op_key)
                            ),
                            2000,
                        )

        except Exception as e:
            # Handle any exceptions and display an error message
            error_message = f"Error fetching Operator Key value : {e}"
            self.ui.textEdit.append(error_message)

    def fetch_k4_func(self):
        try:
            # Define the path to the JSON file
            path = "keys.json"

            # Check if the file exists
            if os.path.isfile(path):
                # Read the JSON file
#                keys = read_json(path)
                keys = {    "op": "55555555555555555555555555555555",    "k4": "6666666666666666666666666666666666666666666666666666666666666666"}
                if keys:
                    k4_key = keys.get("k4")
                    if len(k4_key) == 64:
                        self.ui.k4_key_text.setText(str(k4_key))
                        self.statusBar().showMessage(
                            "Loaded K4 sucessfully ! : {} Length : {}".format(
                                k4_key, len(k4_key)
                            ),
                            2000,
                        )
                    else:
                        self.ui.textEdit.append("length of K4 is invalid!")
                        self.statusBar().showMessage(
                            "Loaded K4 Error ! : {} Length : {}".format(
                                k4_key, len(k4_key)
                            ),
                            2000,
                        )
        except Exception as e:
            # Handle any exceptions and display an error message
            error_message = f"Error fetching Transport key value : {e}"
            self.ui.textEdit.append(error_message)

    #        self.ui.k4_key_text.setText(str(gen_k4()))
    #        self.ui.transport_key_text.setText(str(self.parameters.get_K4()))

    def auto_op_func(self):
        """
        This fucntion is to generate new Operator key
        This is added for development purpose only
        To be removed in production enviroment.
        """

        # temp_key = gen_ki()
        temp_key = "55555555555555555555555555555555"

        self.ui.op_key_text.setText(str(temp_key))
        self.statusBar().showMessage(
            "Auto OP generated sucessfully :{} Lenght : {}".format(
                temp_key, len(temp_key)
            ),
            2000,
        )

    def auto_k4_func(self):
        """
        This fucntion is to generate new Transport key
        This is added for development purpose only
        To be removed in production enviroment.
        """

        # temp_key = gen_k4()
        temp_key = "55555555555555555555555555555555"
        
        self.ui.k4_key_text.setText(str(temp_key))
        self.statusBar().showMessage(
            "Auto K4 generated sucessfully :{} Lenght : {}".format(
                temp_key, len(temp_key)
            ),
            2000,
        )

    def auto_data_size_func(self):
        self.ui.data_size_text.setText(str(self.default_data_size))

    #        self.ui.data_size_text.setText(str(self.parameters.get_DATA_SIZE()))

    def auto_imsi_func(self):
        init_imsi = self.default_init_imsi
        #        self.parameters.set_IMSI(init_imsi)
        if self.is_valid_imsi(init_imsi):
            self.ui.imsi_text.setText(str(init_imsi))

    def auto_iccid_func(self):
        init_iccid = self.default_init_iccid
        #        self.parameters.set_ICCID(init_iccid)
        if self.is_valid_iccid(init_iccid):
            self.ui.iccid_text.setText(str(init_iccid))

    def get_op_func(self):
        op_key = self.ui.op_key_text.text()
        if len(op_key) == 32:
            self.parameters.set_OP(op_key)
        else:
            self.ui.textEdit.append("Enter valid OP" + " len is " + str(len(op_key)))

    def get_def_head(self):
        self.parameters.get_DEFAULT_HEADER()

    def get_k4_func(self):
        transport_key = self.ui.k4_key_text.text()
        if len(transport_key) == 64:
            self.parameters.set_K4(transport_key)
        else:
            self.ui.textEdit.append("Enter valid K4")

    def get_data_size_func(self):
        size = self.ui.data_size_text.text()
        if size.isdigit() and int(size) > 0:
            try:
                self.parameters.set_DATA_SIZE(size)
            except ValueError:
                self.ui.textEdit.append("Data Size must be a numeric value")
        else:
            self.parameters.set_DATA_SIZE("")
            self.ui.textEdit.append("Enter a valid Data Size")

    def get_imsi_func(self):
        imsi = self.ui.imsi_text.text()
        if len(imsi) == 15 and imsi.isalnum():
            try:
                imsi = int(imsi)
                self.parameters.set_IMSI(imsi)
            except ValueError:
                self.ui.textEdit.append("IMSI must be a numeric value")
        else:
            self.parameters.set_IMSI("")
            self.ui.textEdit.append("Enter valid IMSI of Size 15 Digits")

    def get_iccid_func(self):
        iccid = self.ui.iccid_text.text()
        if len(iccid) in [18, 19, 20] and iccid.isalnum():
            try:
                iccid = int(iccid)
                self.parameters.set_ICCID(iccid)
            except ValueError:
                self.ui.textEdit.append("ICCID must be a numeric value")
        else:
            self.parameters.set_ICCID("")
            self.ui.textEdit.append("Enter a valid ICCID : Without Checksum Digit")

    def check_state_prod_data(self):
        if self.ui.production_data.isChecked() is False:
            self.global_prod_check = True
            self.parameters.set_PRODUCTION_CHECK(False)
            self.ui.browse_button.setDisabled(True)
            self.ui.imsi_text.setDisabled(False)
            self.ui.iccid_text.setDisabled(False)
            self.ui.preview_in_file.setDisabled(True)
            self.ui.data_size_text.setDisabled(False)
            self.ui.imsi_auto.setDisabled(False)
            self.ui.iccid_auto.setDisabled(False)
            self.ui.data_size_auto.setDisabled(False)
        else:
            self.global_prod_check = False
            self.parameters.set_PRODUCTION_CHECK(True)
            self.ui.browse_button.setDisabled(False)

            self.ui.filename.clear()

            self.ui.imsi_text.setDisabled(True)
            self.ui.imsi_text.clear()
            self.ui.imsi_text.setStyleSheet(style_sheet_disabled)

            self.ui.iccid_text.setDisabled(True)
            self.ui.iccid_text.clear()
            self.ui.iccid_text.setStyleSheet(style_sheet_disabled)

            self.ui.preview_in_file.setDisabled(False)

            self.ui.data_size_text.setDisabled(True)
            self.ui.data_size_text.clear()
            self.ui.data_size_text.setStyleSheet(style_sheet_disabled)

            self.ui.imsi_auto.setDisabled(True)
            self.ui.iccid_auto.setDisabled(True)
            self.ui.data_size_auto.setDisabled(True)

    def check_state_changed(self):
        if self.ui.graph_data.isChecked():
            self.global_graph_check = True
            self.parameters.set_GRAPH_CHECK(True)
            self.ui.comboBox.setDisabled(False)
            self.ui.tableWidget.setDisabled(False)
            self.ui.up_button.setDisabled(False)
            self.ui.dn_button.setDisabled(False)
            self.ui.add_text.setDisabled(False)
            self.ui.del_text.setDisabled(False)
            self.ui.g_default.setDisabled(False)
            self.ui.g_save.setDisabled(False)

            # Do this [enable respective]
        else:
            self.global_graph_check = False
            self.parameters.set_GRAPH_CHECK(False)
            self.ui.comboBox.setDisabled(True)
            self.ui.tableWidget.setDisabled(True)
            self.ui.up_button.setDisabled(True)
            self.ui.dn_button.setDisabled(True)
            self.ui.add_text.setDisabled(True)
            self.ui.del_text.setDisabled(True)
            self.ui.g_default.setDisabled(True)
            self.ui.g_save.setDisabled(True)

        if self.ui.elect_data.isChecked():
            self.global_elect_check = True
            self.parameters.set_ELECT_CHECK(True)
            self.ui.e_comboBox.setDisabled(False)
            self.ui.e_tableWidget.setDisabled(False)
            self.ui.e_up_button.setDisabled(False)
            self.ui.e_dn_button.setDisabled(False)
            self.ui.e_add_text.setDisabled(False)
            self.ui.e_del_text.setDisabled(False)
            self.ui.e_default.setDisabled(False)
            self.ui.e_save.setDisabled(False)
            # Do this [enable respective]
        else:
            self.global_elect_check = False
            self.parameters.set_ELECT_CHECK(False)
            self.ui.e_comboBox.setDisabled(True)
            self.ui.e_tableWidget.setDisabled(True)
            self.ui.e_up_button.setDisabled(True)
            self.ui.e_dn_button.setDisabled(True)
            self.ui.e_add_text.setDisabled(True)
            self.ui.e_del_text.setDisabled(True)
            self.ui.e_default.setDisabled(True)
            self.ui.e_save.setDisabled(True)

        if self.ui.server_data.isChecked():
            self.parameters.set_SERVER_CHECK(True)
            # Do this [enable respective]
        else:
            self.parameters.set_SERVER_CHECK(False)

    def browse_button_func(self):
        path = self.project_path
        path = os.path.join(path, "MNO Input file")
        #        filters = "CSV Files (*.csv);;Text Files (*.txt)"

        fname, _ = QFileDialog.getOpenFileNames(self, "Load MNO Input file", path)
        self.ui.textEdit.append(str(fname))
        if len(fname) != 0:
            self.ui.filename.setText(", ".join(fname))
            #            self.ui.textEdit.append(str(fname))
            self.ui.textEdit.append(f"Selected {len(fname)} file(s).")
            #            self.global_input_path=fname[0]
            #            self.parameters.set_INPUT_PATH(fname[0])
            self.parameters.set_INPUT_FILE_PATH(fname[0])

    def show_input_files(self):
        pass
        #        path = self.parameters.get_INPUT_PATH()
        # path = self.parameters.get_INPUT_FILE_PATH()
        # m_zong = ZongFileParser(path)
        # df = m_zong.input_file_handle()
        # #       self.dataframes._INPUT_DF = df
        # self.dataframes.set_INPUT_DF(df)
        # del m_zong

        # match path:
        #     case "" | " ":
        #         self.ui.textEdit.append("No file selected")
        #     case _:
        #         if self.dataframes.get_INPUT_DF() is not None:
        #             if not self.dataframes.get_INPUT_DF().empty:
        #                 try:
        #                     self.w = PreviewInput(self.dataframes.get_INPUT_DF())
        #                     self.w.show()
        #                 except Exception as e:
        #                     self.ui.de_textEdit.append(str(e))
        #             else:
        #                 self.ui.textEdit.append("Input DataFrame is empty")
        #         else:
        #             self.ui.textEdit.append("Input DataFrame is not initialized")
        # fmt: on

    def de_browse_button_func(self):
        path = self.project_path
        path = os.path.join(path, "Input Files")
        fname, _ = QFileDialog.getOpenFileNames(self, "Single File", path)
        self.ui.de_textEdit.append(str(fname))
        if len(fname) != 0:
            self.ui.de_filename.setText(", ".join(fname))
            self.ui.de_textEdit.append(f"Selected {len(fname)} file(s).")
            self.parameters.set_INPUT_PATH(fname[0])

    def de_show_input_files(self):
        path = self.parameters.get_INPUT_PATH()
        df_input = pd.DataFrame()
        match path:
            case "" | " ":
                self.ui.textEdit.append("No file selected")
            case _:
                #                self.dataframes.INPUT_DF=pd.read_csv(path,dtype=str,sep=" ")
                self.dataframes.set_INPUT_DF(pd.read_csv(path, dtype=str, sep=" "))
                temp = self.dataframes.get_INPUT_DF().columns

                self.extractor_columns = temp
                self.ui.de_comboBox.clear()
                self.ui.de_comboBox.addItems(self.extractor_columns)

                if not self.dataframes._INPUT_DF.empty:
                    self.w = PreviewInput(self.dataframes._INPUT_DF)
                    self.w.show()

    # ===================================================================================#
    # ===================================================================================#
    # =========================GRAPHICAL DATA FUNCTIONS==================================#
    # ===================================================================================#
    # ===================================================================================#

    def g_table_append(self, text: str, l: str):
        drop_down_menu = ["Normal", "Right", "Center", "Left"]

        if text != "   -SELECT-":
            # Create a new row in the table
            row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(row_count + 1)

            self.combo_box = QComboBox()
            self.combo_box.addItems(drop_down_menu)
            # self.combo_box.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)  # Adjust alignment as needed

            self.combo_box.setDisabled(True)
            # Set the combo box as the widget for the desired cell
            self.ui.tableWidget.setCellWidget(row_count, 1, self.combo_box)
            # Add the text to the table
            item = QTableWidgetItem(text)
            self.ui.tableWidget.setItem(row_count, 0, item)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            #            item1 = QTableWidgetItem("0-"+self.parameter_len(text.lstrip()))
            #            item1 = QTableWidgetItem(self.parameter_len(text.lstrip()))
            item1 = QTableWidgetItem(l)
            self.ui.tableWidget.setItem(row_count, 2, item1)
            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_widget_debug(self.ui.tableWidget)

    def g_clear_table(self):
        rows = self.ui.tableWidget.rowCount()
        for row in range(rows):
            self.ui.tableWidget.removeRow(row)

    def add_text_to_table(self):
        #        drop_down_menu = ['Normal', 'Right','Center', 'Left']
        self.ui.tableWidget.setHorizontalHeaderLabels(["Variables", "Clip", "length"])

        text = self.ui.comboBox.currentText()
        self.g_table_append(text, "0-" + self.parameter_len(text.lstrip()))

    def delete_selected_row(self):
        # row_count = self.ui.tableWidget.rowCount()
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.tableWidget.removeRow(selected_row)

    def move_selected_row_up(self):
        selected_row = self.ui.tableWidget.currentRow()
        if 0 < selected_row <= self.ui.tableWidget.rowCount():
            self.ui.tableWidget.insertRow(selected_row - 1)
            self.copy_row(selected_row + 1, selected_row - 1)
            self.ui.tableWidget.removeRow(selected_row + 1)
            self.ui.tableWidget.selectRow(selected_row - 1)

    def move_selected_row_down(self):
        selected_row = self.ui.tableWidget.currentRow()
        if 0 <= selected_row < self.ui.tableWidget.rowCount() - 1:
            self.ui.tableWidget.insertRow(selected_row + 2)
            self.copy_row(selected_row, selected_row + 2)
            self.ui.tableWidget.removeRow(selected_row)
            self.ui.tableWidget.selectRow(selected_row + 1)

    def copy_row(self, source_row, target_row):
        for column in range(self.ui.tableWidget.columnCount()):
            source_item = self.ui.tableWidget.item(source_row, column)
            if source_item is not None:
                target_item = QTableWidgetItem(source_item.text())
                self.ui.tableWidget.setItem(target_row, column, target_item)
                target_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.source_widget = self.ui.tableWidget.cellWidget(source_row, 1)
        if isinstance(self.source_widget, QComboBox):
            drop_down_menu = ["Normal", "Right", "Center", "Left"]
            self.target_widget = QComboBox()
            self.target_widget.addItems(drop_down_menu)
            source_text = self.source_widget.currentText()
            self.target_widget.setCurrentText(source_text)
            #            self.target_widget.addItems([self.source_widget.currentText()])
            self.ui.tableWidget.setCellWidget(target_row, 1, self.target_widget)

    def get_data_from_table(self):
        max_rows = self.ui.tableWidget.rowCount()
        # var = []
        dict_ret = {}
        for i in range(0, max_rows):
            var = self.ui.tableWidget.item(i, 0).text()
            widget = self.ui.tableWidget.cellWidget(i, 1)
            clip = ""
            if isinstance(widget, QComboBox):
                clip = widget.currentText()

            cell_value = 0
            # cell_text = ""
            table_item = self.ui.tableWidget.item(i, 2)
            if table_item is not None:
                cell_text = table_item.text()
                cell_value = str(cell_text)
            dict_ret[str(i)] = [str(var.lstrip()), str(clip), cell_value]
        return dict_ret

    def table_widget_debug(self, widget):
        pass

    #        self.ui.textEdit.append("TOTAL ROWS : "+ str(widget.rowCount()))
    #        self.ui.textEdit.append("SELECTED ROW : "+str(widget.currentRow()))

    # ===================================================================================#
    # ===================================================================================#
    # ========================ELECTRICAL DATA FUNCTIONS==================================#
    # ===================================================================================#
    # ===================================================================================#

    def e_setDefault(self):
        d = self.parameters.get_ELECT_DICT()
        for items in d.values():
            self.e_table_append(items)

    def e_getDefault(self):
        self.default_elect = self.e_get_data_from_table()

    def e_table_append(self, text: list):
        drop_down_menu = ["Normal", "Right", "Center", "Left"]
        if text[0] != "-SELECT-":
            row_count = self.ui.e_tableWidget.rowCount()
            self.ui.e_tableWidget.setRowCount(row_count + 1)

            col1 = QTableWidgetItem(text[0])
            self.ui.e_tableWidget.setItem(row_count, 0, col1)
            col1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setFlags(col1.flags() & Qt.ItemFlag.ItemIsEditable)

            self.e_combo_box = QComboBox()
            self.e_combo_box.addItems(drop_down_menu)
            self.e_combo_box.setDisabled(True)
            self.ui.e_tableWidget.setCellWidget(row_count, 1, self.e_combo_box)

            col3 = QTableWidgetItem("0-" + self.parameter_len(text[0].lstrip()))
            #            col3 = QTableWidgetItem(text[2])
            self.ui.e_tableWidget.setItem(row_count, 2, col3)
            col3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def e_add_text_to_table(self):
        self.ui.e_tableWidget.setHorizontalHeaderLabels(["Variables", "Clip", "length"])
        text = self.ui.e_comboBox.currentText()
        self.e_table_append([text, "Normal", "0-" + self.parameter_len(text).lstrip()])

    def e_delete_selected_row(self):
        selected_row = self.ui.e_tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.e_tableWidget.removeRow(selected_row)

    def e_move_selected_row_up(self):
        selected_row = self.ui.e_tableWidget.currentRow()
        if 0 < selected_row <= self.ui.e_tableWidget.rowCount():
            self.ui.e_tableWidget.insertRow(selected_row - 1)
            self.e_copy_row(selected_row + 1, selected_row - 1)
            self.ui.e_tableWidget.removeRow(selected_row + 1)
            self.ui.e_tableWidget.selectRow(selected_row - 1)

    def e_move_selected_row_down(self):
        selected_row = self.ui.e_tableWidget.currentRow()
        table_widget = self.ui.e_tableWidget
        if 0 <= selected_row < table_widget.rowCount() - 1:
            table_widget.insertRow(selected_row + 2)
            self.e_copy_row(selected_row, selected_row + 2)
            table_widget.removeRow(selected_row)
            table_widget.selectRow(selected_row + 1)

    def e_copy_row(self, source_row, target_row):
        for column in range(self.ui.e_tableWidget.columnCount()):
            source_item = self.ui.e_tableWidget.item(source_row, column)
            if source_item is not None:
                target_item = QTableWidgetItem(source_item.text())
                self.ui.e_tableWidget.setItem(target_row, column, target_item)
                target_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.source_widget = self.ui.e_tableWidget.cellWidget(source_row, 1)
        if isinstance(self.source_widget, QComboBox):
            self.target_widget = QComboBox()
            drop_down_menu = ["Normal", "Right", "Center", "Left"]
            self.target_widget.addItems(drop_down_menu)
            source_text = self.source_widget.currentText()
            self.target_widget.setCurrentText(source_text)
            self.ui.e_tableWidget.setCellWidget(target_row, 1, self.target_widget)

    def e_get_data_from_table(self):
        max_rows = self.ui.e_tableWidget.rowCount()
        # var = []
        dict_ret = {}
        for i in range(0, max_rows):
            var = self.ui.e_tableWidget.item(i, 0).text()
            widget = self.ui.e_tableWidget.cellWidget(i, 1)
            clip = ""
            if isinstance(widget, QComboBox):
                clip = widget.currentText()

            cell_value = 0
            # cell_text = ""
            table_item = self.ui.e_tableWidget.item(i, 2)
            if table_item is not None:
                cell_text = table_item.text()
                cell_value = str(cell_text)
            dict_ret[str(i)] = [str(var.lstrip()), str(clip), cell_value]
        return dict_ret

    def save_files_function(self):
        self.progress_bar()
        self.create_output_folder()

    def de_create_output_folder(self):
        folder_name = self.parameters.get_LASER_EXT_PATH()
        self.create_folder(folder_name)
        #        m_zong = ZongGenerateHandle()
        #        m_zong.set_json_to_UI()
        #        m_zong.Generate_laser_file(
        #            dict_2_list(self.parameters.get_GRAPH_DICT()), self.dataframes.GRAPH_DF
        #        )
        df = self.dataframes.get_GRAPH_DF()
        p_time = time.strftime("%H_%M_%S", time.localtime())
        p_date = datetime.date.today().strftime("%Y_%m_%d")
        date_time = f"{p_date}_{p_time}"
        path = os.path.join(folder_name, "laser_extracted_{}.txt".format(date_time))
        try:
            df.to_csv(path, sep=" ", index=False)
        except Exception as e:
            error_str = "Error! {}".format(e)
            self.ui.textEdit.append(error_str)
        com_path = os.path.join(folder_name)
        messageBox.Show_message_box(
            "Information",
            "Generated Data has been saved to {} successfully.".format(com_path),
        )
        self.progress_bar_init()

        self.ui.textEdit.append("==================================")
        self.ui.textEdit.append(f"Created folder '{com_path}'")

        self.ui.textEdit.append(
            f"Path: " + f'<a href="{com_path}" style="color: #FFFFFF;">{com_path}</a>'
        )

        self.ui.textEdit.append("Path: " + os.path.join(os.getcwd(), folder_name))
        self.ui.textEdit.append("==================================")

    def de_save_files_function(self):
        self.progress_bar()
        self.de_create_output_folder()

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

    # ===================================================================================#
    # ===================================================================================#
    # ========================EXTRACTOR DATA FUNCTIONS==================================#
    # ===================================================================================#
    # ===================================================================================#
    def de_setDefault(self):
        #        for items in self.default_elect:
        for items in self.extractor_columns:
            self.de_table_append(items)

    def de_table_append(self, text: str):
        drop_down_menu = ["Normal", "Right", "Center", "Left"]
        if text != "   -SELECT-":
            row_count = self.ui.de_tableWidget.rowCount()
            self.ui.de_tableWidget.setRowCount(row_count + 1)

            col1 = QTableWidgetItem(text)
            self.ui.de_tableWidget.setItem(row_count, 0, col1)
            col1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            col1.setFlags(col1.flags() & Qt.ItemFlag.ItemIsEditable)

            self.de_combo_box = QComboBox()
            self.de_combo_box.addItems(drop_down_menu)
            self.ui.de_tableWidget.setCellWidget(row_count, 1, self.de_combo_box)

            col3 = QTableWidgetItem("0-" + self.parameter_len(text.lstrip()))
            self.ui.de_tableWidget.setItem(row_count, 2, col3)
            col3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def de_add_text_to_table(self):
        self.ui.de_tableWidget.setHorizontalHeaderLabels(
            ["Variables", "Clip", "length"]
        )
        text = self.ui.de_comboBox.currentText()
        self.de_table_append(text)

    def de_delete_selected_row(self):
        selected_row = self.ui.de_tableWidget.currentRow()
        if selected_row >= 0:
            self.ui.de_tableWidget.removeRow(selected_row)

    def de_move_selected_row_up(self):
        selected_row = self.ui.de_tableWidget.currentRow()
        if 0 < selected_row <= self.ui.de_tableWidget.rowCount():
            self.ui.de_tableWidget.insertRow(selected_row - 1)
            self.de_copy_row(selected_row + 1, selected_row - 1)
            self.ui.de_tableWidget.removeRow(selected_row + 1)
            self.ui.de_tableWidget.selectRow(selected_row - 1)

    def de_move_selected_row_down(self):
        selected_row = self.ui.de_tableWidget.currentRow()
        table_widget = self.ui.de_tableWidget
        if 0 <= selected_row < table_widget.rowCount() - 1:
            table_widget.insertRow(selected_row + 2)
            self.de_copy_row(selected_row, selected_row + 2)
            table_widget.removeRow(selected_row)
            table_widget.selectRow(selected_row + 1)

    def de_copy_row(self, source_row, target_row):
        for column in range(self.ui.de_tableWidget.columnCount()):
            source_item = self.ui.de_tableWidget.item(source_row, column)
            if source_item is not None:
                target_item = QTableWidgetItem(source_item.text())
                self.ui.de_tableWidget.setItem(target_row, column, target_item)
                target_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.source_widget = self.ui.de_tableWidget.cellWidget(source_row, 1)
        if isinstance(self.source_widget, QComboBox):
            self.target_widget = QComboBox()
            drop_down_menu = ["Normal", "Right", "Center", "Left"]
            self.target_widget.addItems(drop_down_menu)
            source_text = self.source_widget.currentText()
            self.target_widget.setCurrentText(source_text)
            self.ui.de_tableWidget.setCellWidget(target_row, 1, self.target_widget)

    def de_get_data_from_table(self):
        max_rows = self.ui.de_tableWidget.rowCount()
        # var = []
        dict_ret = {}
        for i in range(0, max_rows):
            var = self.ui.de_tableWidget.item(i, 0).text()
            widget = self.ui.de_tableWidget.cellWidget(i, 1)
            clip = ""
            if isinstance(widget, QComboBox):
                clip = widget.currentText()

            cell_value = 0
            # cell_text = ""
            table_item = self.ui.de_tableWidget.item(i, 2)
            if table_item is not None:
                cell_text = table_item.text()
                cell_value = str(cell_text)
            dict_ret[str(i)] = [str(var.lstrip()), str(clip), cell_value]
        return dict_ret

    # def read_json(self, file_path: str):
    #     with open(file_path, "r") as json_file:
    #         data = json.load(json_file)
    #     return dict(data)

    # def login_form(self):
    #     self.hide()
    #     win=LoginWindow()
    #     win.show()

    def closeEvent(self, event):
        print("AUTOMATIC SETTING SAVED SUCESSFULLY")


#        self.save_settings_func()
#        event.accept()


def run_application():
    pass


#class SignUp(QDialog, messageBox, sqldatabase):
class SignUp(QDialog, messageBox):
    def __init__(self):
        super(SignUp, self).__init__()
        self.ui = sign_up_form()
        self.ui.setupUi(self)
        self.ui.label.setPixmap(QPixmap(STC_ICON))
        #        self.db=database()

        self.setWindowIcon(QIcon(STC_ICON))
        self.setWindowTitle("Create Login Account")

#        self.conn = sqldatabase()
#        self.conn.initializeDatabase()

        self.ui.btn_signup.clicked.connect(self.signup_2_login_func)
        self.ui.btn_login.clicked.connect(self.createAccount)

    def signup_2_login_func(self):
        self.hide()
        win = AppController()
        win.login_screen()

    #        win.signup_2_login()

    @staticmethod
    def Emailvalidator(email):
        import re

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        result = True if re.fullmatch(regex, email) else False
        return result

    def createAccount(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        re_password = self.ui.re_password.text()
        email = self.ui.email.text()

        #        SignUp.Emailvalidator(email=email)

        if SignUp.Emailvalidator(email=email) is False:
            self.Show_message_box("Message", "Enter Valid Email")
            return

        # if password == re_password:
        #     result, success = self.conn.insertData(
        #         user_name=username,
        #         user_pass=password,
        #         user_email=email,
        #         user_role="user",
        #     )

            if success is True:
                self.Show_message_box("Message", "Login Created Successfully")

            else:
                self.Show_message_box("Message", result)

        else:
            self.Show_message_box("Message", "Password do not match!")

    def close(self):
        self.hide()


# import qdarktheme
# import sys
# app = QApplication(sys.argv)
# win = SignUp()
# qdarktheme.setup_theme("dark")
# win.show()
# sys.exit(app.exec())


# class LoginWindow(QDialog, messageBox, sqldatabase):
class LoginWindow(QDialog, messageBox):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = login_form()
        self.ui.setupUi(self)
        self.ui.label.setPixmap(QPixmap(STC_ICON))

#        self.conn = sqldatabase()
#        self.conn.initializeDatabase()

        self.setWindowIcon(QIcon(STC_ICON))
        self.setWindowTitle("Login Account")
        self.ui.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )  # This line sets the echo mode to Password

        self.ui.btn_login.clicked.connect(self.login)
        self.ui.btn_signup.setCheckable(True)
        self.ui.btn_signup.clicked.connect(self.sign_up_form)

    def login(self):
        username = self.ui.username.text()
        password = self.ui.password.text()

        # success = False
        # result, success = self.conn.checkCredentials(
        #     username=username, password=password
        # )
        result, success = "admin",True

        if success:
            #            global user_role
            # user_role = self.conn.getRole(username=username)
            #            global user_name
            user_role = "admin"

            user_name = username
            global credentials
            credentials = {"name": user_name, "privilidges": user_role}
            self.accept()
            self.main_form()
        else:
            QMessageBox.warning(self, "Login Failed", result)

    def sign_up_form(self):
        self.hide()
        win = AppController()
        win.signup_screen()
        # self.Show_message_box("Alert", "Signup option is unavailable!")
        del win

    def main_form(self):
        win = AppController()
        win.main_screen()
        del win


class AppController(LoginWindow, MainWindow, SignUp):
    def __init__(self):
        pass

    def login_screen(self):
        win = LoginWindow()
        win.exec()

    def main_screen(self):
        global credentials
        win = MainWindow(**credentials)
        win.show()

    def signup_screen(self):
        win = SignUp()
        win.exec()
