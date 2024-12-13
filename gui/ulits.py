from globals.parameters import PARAMETERS


class GuiButtons:
    def __init__(self, ui):
        self.parameters = PARAMETERS.get_instance()
        self.ui = ui

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
