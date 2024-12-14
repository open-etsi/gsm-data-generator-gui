import datetime
import os
import time

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QLineEdit,
    QMessageBox,
    QDialog,
)

from globals.parameters import PARAMETERS, DATA_FRAMES
from gui.screens import PreviewInput, PreviewOutput
from gui.messages import messageBox
from gui.ulits import set_ui_from_json
from gui.table import GuiElect, GuiGraph, GuiExtractor
from gui.ulits import GuiButtons
from gui.ulits import parameter_len
# from datagen.operators.zong.FileWriter import ZongFileWriter
# from datagen.operators.zong.FileParser import ZongFileParser
# from core.json_utils import JsonHandler
# from core.settings import SETTINGS
from globals.settings import SETTINGS
from gui.stylesheet import style_sheet_good, style_sheet_bad, style_sheet_disabled
from gui.forms.main_ui import Ui_MainWindow
from gui.forms.login_ui import Ui_Form as login_form
from gui.forms.signup_ui import Ui_Form as sign_up_form
from core.executor.utils import read_json, list_2_dict
from gui.auth.utils import emailvalidator

from core.parser.utils import json_loader

# from core.executor.script import DataGenerationScript

debug = False
STC_ICON = "resources/stc_logo.ico"


class MainWindow(QMainWindow):
    project_path = os.getcwd()

    def __init__(self, *args, **kwargs):
        global laser_ext_path, headers_data_dict, headers_laser_dict, header_server_dict
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
        self.setAttribute(
            Qt.WidgetAttribute.WA_DeleteOnClose
        )  # to handle timer issues upon exiting app

        self.ui.textEdit.setFontFamily("Cascadia Mono")
        self.ui.textEdit.setFontPointSize(10)
        self.setWindowIcon(QIcon(STC_ICON))
        self.parameters = PARAMETERS.get_instance()
        self.dataframes = DATA_FRAMES.get_instance()
        self.sett = SETTINGS()
        self.elect_gui = GuiElect(self.ui)
        self.graph_gui = GuiGraph(self.ui)
        self.button_gui = GuiButtons(self.ui)
        self.extractor_gui = GuiExtractor(self.ui)
        #        self.sec = messageBox()

        self.user_privileges = user_role
        self.ui.lbl_username.setText(user_name)
        self.ui.lbl_userrole.setText(user_role)
        self.ui.btn_logout.clicked.connect(self.logout_func)

        # this must not be here | remove in revision

        data = read_json("settings.json")
        if data:
            header_server_dict = list_2_dict(data["PARAMETERS"]["server_variables"])
            headers_laser_dict = data["PARAMETERS"]["laser_variables"]
            headers_data_dict = list_2_dict(data["PARAMETERS"]["data_variables"])
            laser_ext_path = data["PATHS"]["OUTPUT_FILES_LASER_EXT"]

        self.parameters.set_LASER_EXT_PATH(laser_ext_path)
        self.parameters.set_ELECT_DICT(headers_data_dict)
        self.parameters.set_GRAPH_DICT(headers_laser_dict)
        self.parameters.set_SERVER_DICT(header_server_dict)

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

        self.ui.add_text.clicked.connect(self.graph_gui.add_text_to_table)
        self.ui.del_text.clicked.connect(self.graph_gui.delete_selected_row)
        self.ui.up_button.clicked.connect(self.graph_gui.move_selected_row_up)
        self.ui.dn_button.clicked.connect(self.graph_gui.move_selected_row_down)
        self.ui.g_default.clicked.connect(self.graph_gui.g_setDefault)
        self.ui.g_save.clicked.connect(self.graph_gui.g_getDefault)

        self.ui.e_add_text.clicked.connect(self.elect_gui.e_add_text_to_table)
        self.ui.e_del_text.clicked.connect(self.elect_gui.e_delete_selected_row)
        self.ui.e_up_button.clicked.connect(self.elect_gui.e_move_selected_row_up)
        self.ui.e_dn_button.clicked.connect(self.elect_gui.e_move_selected_row_down)
        self.ui.e_default.clicked.connect(self.elect_gui.e_setDefault)
        self.ui.e_save.clicked.connect(self.elect_gui.e_getDefault)

        self.ui.browse_button.clicked.connect(self.browse_button_func)
        self.ui.preview_in_file.clicked.connect(self.show_input_files)

        self.ui.graph_data.stateChanged.connect(self.check_state_changed)
        self.ui.elect_data.stateChanged.connect(self.check_state_changed)
        self.ui.server_data.stateChanged.connect(self.check_state_changed)
        self.check_state_changed()

        self.ui.production_data.stateChanged.connect(self.check_state_prod_data)
        self.check_state_prod_data()

        self.ui.op_key_auto.clicked.connect(self.button_gui.auto_op_func)
        self.ui.k4_key_auto.clicked.connect(self.button_gui.auto_k4_func)
        self.ui.op_key_fetch.clicked.connect(self.button_gui.fetch_op_func)
        self.ui.k4_key_fetch.clicked.connect(self.button_gui.fetch_k4_func)
        self.ui.data_size_auto.clicked.connect(self.button_gui.auto_data_size_func)
        self.ui.imsi_auto.clicked.connect(self.button_gui.auto_imsi_func)
        self.ui.iccid_auto.clicked.connect(self.button_gui.auto_iccid_func)

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

        self.ui.pin1_rand_check.stateChanged.connect(self.button_gui.pin1_rand_check)
        self.ui.pin2_rand_check.stateChanged.connect(self.button_gui.pin2_rand_check)
        self.ui.puk1_rand_check.stateChanged.connect(self.button_gui.puk1_rand_check)
        self.ui.puk2_rand_check.stateChanged.connect(self.button_gui.puk2_rand_check)
        self.ui.adm1_rand_check.stateChanged.connect(self.button_gui.adm1_rand_check)
        self.ui.adm6_rand_check.stateChanged.connect(self.button_gui.adm6_rand_check)

        self.ui.pin1_auto.clicked.connect(self.button_gui.auto_pin1_func)
        self.ui.pin2_auto.clicked.connect(self.button_gui.auto_pin2_func)
        self.ui.puk1_auto.clicked.connect(self.button_gui.auto_puk1_func)
        self.ui.puk2_auto.clicked.connect(self.button_gui.auto_puk2_func)
        self.ui.adm1_auto.clicked.connect(self.button_gui.auto_adm1_func)
        self.ui.adm6_auto.clicked.connect(self.button_gui.auto_adm6_func)

        self.ui.save_seting_button.clicked.connect(self.save_settings_func)
        self.ui.load_seting_button.clicked.connect(self.load_settings_func)

        self.ui.de_browse_button.clicked.connect(self.de_browse_button_func)
        self.ui.de_preview_in_file.clicked.connect(self.de_show_input_files)

        self.ui.de_add_text.clicked.connect(self.extractor_gui.de_add_text_to_table)
        self.ui.de_del_text.clicked.connect(self.extractor_gui.de_delete_selected_row)
        self.ui.de_up_button.clicked.connect(self.extractor_gui.de_move_selected_row_up)
        self.ui.de_dn_button.clicked.connect(self.extractor_gui.de_move_selected_row_down)
        self.ui.de_default.clicked.connect(self.extractor_gui.de_setDefault)

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

    def extractor_function(self, dest, src):
        print(self.dataframes._INPUT_DF)


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
            login_screen()
        else:
            exit()


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
            self.button_gui.get_iccid_func()
            self.button_gui.get_imsi_func()
            self.button_gui.get_data_size_func()

        self.button_gui.pin1_rand_check()
        self.button_gui.pin2_rand_check()
        self.button_gui.puk1_rand_check()
        self.button_gui.puk2_rand_check()
        self.button_gui.adm1_rand_check()
        self.button_gui.adm6_rand_check()

        self.button_gui.update_pin1_text()
        self.button_gui.update_pin2_text()
        self.button_gui.update_puk1_text()
        self.button_gui.update_puk2_text()
        self.button_gui.update_adm1_text()
        self.button_gui.update_adm6_text()

        self.button_gui.get_k4_func()
        self.button_gui.get_op_func()

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

        self.parameters.set_GRAPH_DICT(self.graph_gui.get_data_from_table())
        self.parameters.set_ELECT_DICT(self.elect_gui.e_get_data_from_table())
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

            if self.user_privileges == "admin":
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
        var = int(parameter_len(text))
        if (var + 1) > len(key_type):
            widget.setStyleSheet(style_sheet_bad)
        else:
            widget.setStyleSheet(style_sheet_good)


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
        path = os.path.join(path, "Json File")
        filters = ";JSON (*.json);"

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

            # s = DataGenerationScript(config_holder=config_holder)
            # s.SET_ALL_DISP_PARAMS()  # testing
            # (dfs, keys) = s.generate_all_data()
            #
            # # print(s.generate_all_data())
            # print(dfs["ELECT"].to_csv("ELECT.csv"))
            # print(dfs["GRAPH"].to_csv("GRAPH.csv"))
            # print(dfs["SERVER"].to_csv("SERVER.csv"))

    def show_input_files(self):
        set_ui_from_json(self.ui, self.config_holder)
        self.elect_gui.e_setDefault()
        self.graph_gui.g_setDefault()

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



# class SignUp(QDialog, messageBox, sqldatabase):
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
        login_screen()

    #        win.signup_2_login()

    def createAccount(self):
        username = self.ui.username.text()
        password = self.ui.password.text()
        re_password = self.ui.re_password.text()
        email = self.ui.email.text()

        #        SignUp.Emailvalidator(email=email)

        if emailvalidator(email=email) is False:
            self.Show_message_box("Message", "Enter Valid Email")
            return

            # if password == re_password:
            #     result, success = self.conn.insertData(
            #         user_name=username,
            #         user_pass=password,
            #         user_email=email,
            #         user_role="user",
            #     )

            # if success is True:
            #     self.Show_message_box("Message", "Login Created Successfully")
            #
            # else:
            #     self.Show_message_box("Message", result)

        else:
            self.Show_message_box("Message", "Password do not match!")

    def close(self):
        self.hide()


def main_form():
    win = AppController()
    main_screen()
    del win


class LoginWindow(QDialog, messageBox):
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
        self.ui.btn_signup.clicked.connect(self.sign_up_form)

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
            global credentials
            credentials = {"name": user_name, "privilidges": user_role}
            self.accept()
            main_form()
        else:
            QMessageBox.warning(self, "Login Failed", result)

    def sign_up_form(self):
        self.hide()
        win = AppController()
        signup_screen()
        # self.Show_message_box("Alert", "Signup option is unavailable!")
        del win


def login_screen():
    win = LoginWindow()
    win.exec()


def main_screen():
    global credentials
    win = MainWindow(**credentials)
    win.show()


def signup_screen():
    win = SignUp()
    win.exec()


class AppController(LoginWindow, MainWindow, SignUp):
    def __init__(self):
        pass
