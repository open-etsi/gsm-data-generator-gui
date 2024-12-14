import os
from globals.parameters import PARAMETERS


class GuiButtons:
    def __init__(self, ui):
        self.parameters = PARAMETERS.get_instance()
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
                        #     "Loaded K4 sucessfully ! : {} Length : {}".format(
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
        This fucntion is to generate new Operator key
        This is added for development purpose only
        To be removed in production enviroment.
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
        This fucntion is to generate new Transport key
        This is added for development purpose only
        To be removed in production enviroment.
        """

        # temp_key = gen_k4()
        temp_key = "55555555555555555555555555555555"

        self.ui.k4_key_text.setText(str(temp_key))
        # self.statusBar().showMessage(
        #     "Auto K4 generated sucessfully :{} Lenght : {}".format(
        #         temp_key, len(temp_key)
        #     ),
        #     2000,
        # )

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


def set_ui_from_json(ui, config_holder):
    ui.imsi_text.setText(config_holder.DISP.imsi)
    ui.imsi_text.setText(config_holder.DISP.imsi)
    ui.iccid_text.setText(config_holder.DISP.iccid)
    ui.pin1_text.setText(config_holder.DISP.pin1)
    ui.puk1_text.setText(config_holder.DISP.puk1)
    ui.pin2_text.setText(config_holder.DISP.pin2)
    ui.puk2_text.setText(config_holder.DISP.puk2)
    ui.adm1_text.setText(config_holder.DISP.adm1)
    ui.adm6_text.setText(config_holder.DISP.adm6)
    ui.k4_key_text.setText(config_holder.DISP.K4)
    ui.op_key_text.setText(config_holder.DISP.op)
    ui.data_size_text.setText(str(config_holder.DISP.size))
    ui.pin1_rand_check.setChecked(bool(config_holder.DISP.pin1_fix))
    ui.pin2_rand_check.setChecked(bool(config_holder.DISP.pin2_fix))
    ui.puk1_rand_check.setChecked(bool(config_holder.DISP.puk1_fix))
    ui.puk2_rand_check.setChecked(bool(config_holder.DISP.puk2_fix))
    ui.adm1_rand_check.setChecked(bool(config_holder.DISP.adm1_fix))
    ui.adm6_rand_check.setChecked(bool(config_holder.DISP.adm6_fix))



class GuiContoller:
    def __init__(self):
        pass


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


def is_valid_iccid(iccid):
    iccid_length = len(str(iccid))
    return iccid_length in [18, 19, 20]


def is_valid_imsi(imsi):
    return len(str(imsi)) == 15
