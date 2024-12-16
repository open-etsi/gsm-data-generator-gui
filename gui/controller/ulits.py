import os
from typing import Annotated
from globals.parameters import Parameters
from gui.stylesheet import style_sheet_disabled, style_sheet_good, style_sheet_bad


class TextLengthValidator:
    def __init__(self, ui):
        self.ui = ui
        self.connect_signals()

    def connect_signals(self):
        text_widgets = {
            "K4": self.ui.k4_key_text,
            "OP": self.ui.op_key_text,
            "SIZE": self.ui.data_size_text,
            "IMSI": self.ui.imsi_text,
            "ICCID_MIN": self.ui.iccid_text,
            "PIN1": self.ui.pin1_text,
            "PIN2": self.ui.pin2_text,
            "PUK1": self.ui.puk1_text,
            "PUK2": self.ui.puk2_text,
            "ADM1": self.ui.adm1_text,
            "ADM6": self.ui.adm6_text,
        }

        for key_type, widget in text_widgets.items():
            widget.textChanged.connect(lambda text, k=key_type, w=widget: len_check(k, text, w))


class GuiCheckBox:
    def __init__(self, ui):
        self.global_elect_check = None
        self.global_graph_check = None
        self.global_prod_check = None
        self.parameters = Parameters.get_instance()
        self.ui = ui
        self.ui.production_data.setChecked(self.parameters.get_PRODUCTION_CHECK())
        self.ui.elect_data.setChecked(self.parameters.get_ELECT_CHECK())
        self.ui.graph_data.setChecked(self.parameters.get_GRAPH_CHECK())
        self.ui.server_data.setChecked(self.parameters.get_SERVER_CHECK())
        self.check_state_changed()
        self.check_state_prod_data()

    def get_elect_check(self) -> bool:
        return self.ui.elect_data.isChecked()

    def get_graph_check(self) -> bool:
        return self.ui.graph_data.isChecked()

    def get_server_check(self) -> bool:
        return self.ui.server_data.isChecked()

    def adm6_rand_check(self):
        if self.ui.adm6_rand_check.isChecked():
            self.parameters.set_ADM6_RAND(True)
        else:
            self.parameters.set_ADM6_RAND(False)

    def adm1_rand_check(self):
        if self.ui.adm1_rand_check.isChecked():
            self.parameters.set_ADM1_RAND(True)
        else:
            self.parameters.set_ADM1_RAND(False)

    def pin2_rand_check(self):
        if self.ui.pin2_rand_check.isChecked():
            self.parameters.set_PIN2_RAND(True)
        else:
            self.parameters.set_PIN2_RAND(False)

    def pin1_rand_check(self):
        if self.ui.pin1_rand_check.isChecked():
            self.parameters.set_PIN1_RAND(True)
        else:
            self.parameters.set_PIN1_RAND(False)

    def puk1_rand_check(self):
        if self.ui.puk1_rand_check.isChecked():
            self.parameters.set_PUK1_RAND(True)
        else:
            self.parameters.set_PUK1_RAND(False)

    def puk2_rand_check(self):
        if self.ui.puk2_rand_check.isChecked():
            self.parameters.set_PUK2_RAND(True)
        else:
            self.parameters.set_PUK2_RAND(False)

    def check_state_prod_data(self):
        # if self.ui.production_data.isChecked() is False:
        self.global_prod_check = True
        self.parameters.set_PRODUCTION_CHECK(False)
        self.ui.browse_button.setDisabled(False)
        self.ui.preview_in_file.setDisabled(False)
        self.ui.imsi_text.setDisabled(False)
        self.ui.iccid_text.setDisabled(False)
        self.ui.data_size_text.setDisabled(False)
        self.ui.imsi_auto.setDisabled(False)
        self.ui.iccid_auto.setDisabled(False)
        self.ui.data_size_auto.setDisabled(False)

    # else:
    #     self.global_prod_check = False
    #     self.parameters.set_PRODUCTION_CHECK(True)
    #     self.ui.browse_button.setDisabled(False)
    #
    #     self.ui.filename.clear()
    #
    #     self.ui.imsi_text.setDisabled(True)
    #     self.ui.imsi_text.clear()
    #     self.ui.imsi_text.setStyleSheet(style_sheet_disabled)
    #
    #     self.ui.iccid_text.setDisabled(True)
    #     self.ui.iccid_text.clear()
    #     self.ui.iccid_text.setStyleSheet(style_sheet_disabled)
    #
    #     self.ui.preview_in_file.setDisabled(False)
    #
    #     self.ui.data_size_text.setDisabled(True)
    #     self.ui.data_size_text.clear()
    #     self.ui.data_size_text.setStyleSheet(style_sheet_disabled)
    #
    #     self.ui.imsi_auto.setDisabled(True)
    #     self.ui.iccid_auto.setDisabled(True)
    #     self.ui.data_size_auto.setDisabled(True)

    def check_state_changed(self):
        print("check_state_changed()")
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


class GuiButtons:
    def __init__(self, ui):
        self.default_init_imsi = 410000000000000
        self.default_init_iccid = 899000000000000000
        self.default_data_size = 5
        self.parameters = Parameters.get_instance()
        self.ui = ui

    def fetch_op_func(self):
        try:
            # Define the path to the JSON file
            path = "keys.json"

            # Check if the file exists
            if os.path.isfile(path):
                # Read the JSON file
                #                keys = read_json(path)
                keys = {"op": "55555555555555555555555555555555",
                        "k4": "6666666666666666666666666666666666666666666666666666666666666666"}
                # Check if the JSON is not empty
                if keys:
                    op_key = keys.get("op")
                    if len(op_key) == 32:
                        # Set the op_key_text field in the UI
                        self.ui.op_key_text.setText(str(op_key))
                        # self.statusBar().showMessage(
                        #     "Loaded OP sucessfully :{} Length : {}".format(
                        #         op_key, len(op_key)
                        #     ),
                        #     2000,
                        # )
                    else:
                        self.ui.textEdit.append("length of OP is invalid!")
                        # self.statusBar().showMessage(
                        #     "Loaded OP Error ! :{} Length : {}".format(
                        #         op_key, len(op_key)
                        #     ),
                        #     2000,
                        # )

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
                keys = {"op": "55555555555555555555555555555555",
                        "k4": "6666666666666666666666666666666666666666666666666666666666666666"}
                if keys:
                    k4_key = keys.get("k4")
                    if len(k4_key) == 64:
                        self.ui.k4_key_text.setText(str(k4_key))
                        # self.statusBar().showMessage(
                        #     "Loaded K4 successfully ! : {} Length : {}".format(
                        #         k4_key, len(k4_key)
                        #     ),
                        #     2000,
                        # )
                    else:
                        self.ui.textEdit.append("length of K4 is invalid!")
                        # self.statusBar().showMessage(
                        #     "Loaded K4 Error ! : {} Length : {}".format(
                        #         k4_key, len(k4_key)
                        #     ),
                        #     2000,
                        # )
        except Exception as e:
            # Handle any exceptions and display an error message
            error_message = f"Error fetching Transport key value : {e}"
            self.ui.textEdit.append(error_message)

    #        self.ui.k4_key_text.setText(str(gen_k4()))
    #        self.ui.transport_key_text.setText(str(self.parameters.get_K4()))

    def auto_op_func(self):
        """
        This function is to generate new Operator key
        This is added for development purpose only
        To be removed in production environment.
        """

        # temp_key = gen_ki()
        temp_key = "55555555555555555555555555555555"

        self.ui.op_key_text.setText(str(temp_key))
        # self.statusBar().showMessage(
        #     "Auto OP generated sucessfully :{} Lenght : {}".format(
        #         temp_key, len(temp_key)
        #     ),
        #     2000,
        # )

    def auto_k4_func(self):
        """
        This function is to generate new Transport key
        This is added for development purpose only
        To be removed in production environment.
        """

        # temp_key = gen_k4()
        temp_key = "55555555555555555555555555555555"

        self.ui.k4_key_text.setText(str(temp_key))
        # self.statusBar().showMessage(
        #     "Auto K4 generated successfully :{} Length : {}".format(
        #         temp_key, len(temp_key)
        #     ),
        #     2000,
        # )

    def auto_data_size_func(self):
        self.ui.data_size_text.setText(str(self.default_data_size))
        self.ui.data_size_text.setText(str(self.parameters.get_DATA_SIZE()))

    def auto_imsi_func(self):
        init_imsi = self.default_init_imsi
        #        self.parameters.set_IMSI(init_imsi)
        if is_valid_imsi(init_imsi):
            self.ui.imsi_text.setText(str(init_imsi))

    def auto_iccid_func(self):
        init_iccid = self.default_init_iccid
        #        self.parameters.set_ICCID(init_iccid)
        if is_valid_iccid(init_iccid):
            self.ui.iccid_text.setText(str(init_iccid))

    # def update_pin1_text(self):
    #     var = self.ui.pin1_text.text()
    #     if len(var) == 4:
    #         self.parameters.set_PIN1(var)
    #     else:
    #         self.parameters.set_PIN1("")
    #         self.ui.textEdit.append("Enter valid PIN1")
    #
    # def update_pin2_text(self):
    #     var = self.ui.pin2_text.text()
    #     if len(var) == 4:
    #         self.parameters.set_PIN2(var)
    #     else:
    #         self.parameters.set_PIN2("")
    #         self.ui.textEdit.append("Enter valid PIN2")
    #
    # def update_puk1_text(self):
    #     var = self.ui.puk1_text.text()
    #     if len(var) == 8:
    #         self.parameters.set_PUK1(var)
    #     else:
    #         self.parameters.set_PUK1("")
    #         self.ui.textEdit.append("Enter valid PUK1")
    #
    # def update_puk2_text(self):
    #     var = self.ui.puk2_text.text()
    #     if len(var) == 8:
    #         self.parameters.set_PUK2(var)
    #     else:
    #         self.parameters.set_PUK2("")
    #         self.ui.textEdit.append("Enter valid PUK2")
    #
    # def update_adm1_text(self):
    #     var = self.ui.adm1_text.text()
    #     if len(var) == 8:
    #         self.parameters.set_ADM1(var)
    #     else:
    #         self.parameters.set_ADM1("")
    #         self.ui.textEdit.append("Enter valid ADM1")
    #
    # def update_adm6_text(self):
    #     var = self.ui.adm6_text.text()
    #     if len(var) == 8:
    #         self.parameters.set_ADM6(var)
    #     else:
    #         self.parameters.set_ADM6("")
    #         self.ui.textEdit.append("Enter valid ADM6")

    def auto_pin1_func(self):
        # string = generate_4_Digit()
        string = "0000"
        self.ui.pin1_text.setText(string)

    def auto_pin2_func(self):
        #        string = generate_4_Digit()
        string = "0000"
        self.ui.pin2_text.setText(string)

    def auto_puk1_func(self):
        #        string = generate_8_Digit()
        string = "00000000"
        self.ui.puk1_text.setText(string)

    def auto_puk2_func(self):
        #        string = generate_8_Digit()
        string = "00000000"
        self.ui.puk2_text.setText(string)

    def auto_adm1_func(self):
        #        string = generate_8_Digit()
        string = "00000000"
        self.ui.adm1_text.setText(string)

    def auto_adm6_func(self):
        #        string = generate_8_Digit()
        string = "00000000"
        self.ui.adm6_text.setText(string)


def parameter_len(param) -> str:
    """Function printing python version."""
    length = 0
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


def is_valid_iccid(iccid: Annotated[int, "ICCID length validation"]) -> bool:
    iccid_length = len(str(iccid))
    return iccid_length in [18, 19, 20]


def is_valid_imsi(imsi: [int, "IMSI Length Validation"]) -> bool:
    return len(str(imsi)) == 15


def len_check(text, key_type, widget):
    var = int(parameter_len(text))
    if (var + 1) > len(key_type):
        widget.setStyleSheet(style_sheet_bad)
    else:
        widget.setStyleSheet(style_sheet_good)
