import  json
from gui.table import GuiElect, GuiGraph, GuiExtractor
from gui.controller.ulits import GuiButtons, GuiCheckBox, TextLengthValidator

from globals.parameters import Parameters
from core.executor.utils import list_2_dict, dict_2_list
class Controller:
    def __init__(self, ui):
        self.ui = ui
        self.parameters = Parameters.get_instance()

        self.elect_gui = GuiElect(self.ui)
        self.graph_gui = GuiGraph(self.ui)
        self.button_gui = GuiButtons(self.ui)
        # self.extractor_gui = GuiExtractor(self.ui)
        self.checkbox_gui = GuiCheckBox(self.ui)
        # self.text_validator = TextLengthValidator(self.ui)
        #

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

        self.ui.graph_data.stateChanged.connect(self.checkbox_gui.check_state_changed)
        self.ui.elect_data.stateChanged.connect(self.checkbox_gui.check_state_changed)
        self.ui.server_data.stateChanged.connect(self.checkbox_gui.check_state_changed)
        #        self.checkbox_gui.check_state_changed() # added in class

        self.ui.production_data.stateChanged.connect(self.checkbox_gui.check_state_prod_data)
        #        self.checkbox_gui.check_state_prod_data() # added in class

        self.ui.op_key_auto.clicked.connect(self.button_gui.auto_op_func)
        self.ui.k4_key_auto.clicked.connect(self.button_gui.auto_k4_func)
        self.ui.op_key_fetch.clicked.connect(self.button_gui.fetch_op_func)
        self.ui.k4_key_fetch.clicked.connect(self.button_gui.fetch_k4_func)
        self.ui.data_size_auto.clicked.connect(self.button_gui.auto_data_size_func)
        self.ui.imsi_auto.clicked.connect(self.button_gui.auto_imsi_func)
        self.ui.iccid_auto.clicked.connect(self.button_gui.auto_iccid_func)

        self.ui.pin1_rand_check.stateChanged.connect(self.checkbox_gui.pin1_rand_check)
        self.ui.pin2_rand_check.stateChanged.connect(self.checkbox_gui.pin2_rand_check)
        self.ui.puk1_rand_check.stateChanged.connect(self.checkbox_gui.puk1_rand_check)
        self.ui.puk2_rand_check.stateChanged.connect(self.checkbox_gui.puk2_rand_check)
        self.ui.adm1_rand_check.stateChanged.connect(self.checkbox_gui.adm1_rand_check)
        self.ui.adm6_rand_check.stateChanged.connect(self.checkbox_gui.adm6_rand_check)

        self.ui.pin1_auto.clicked.connect(self.button_gui.auto_pin1_func)
        self.ui.pin2_auto.clicked.connect(self.button_gui.auto_pin2_func)
        self.ui.puk1_auto.clicked.connect(self.button_gui.auto_puk1_func)
        self.ui.puk2_auto.clicked.connect(self.button_gui.auto_puk2_func)
        self.ui.adm1_auto.clicked.connect(self.button_gui.auto_adm1_func)
        self.ui.adm6_auto.clicked.connect(self.button_gui.auto_adm6_func)

    # def set_ui_from_json(self, config_holder):
    #     self.ui.imsi_text.setText(config_holder.DISP.imsi)
    #     self.ui.iccid_text.setText(config_holder.DISP.iccid)
    #     self.ui.pin1_text.setText(config_holder.DISP.pin1)
    #     self.ui.puk1_text.setText(config_holder.DISP.puk1)
    #     self.ui.pin2_text.setText(config_holder.DISP.pin2)
    #     self.ui.puk2_text.setText(config_holder.DISP.puk2)
    #     self.ui.adm1_text.setText(config_holder.DISP.adm1)
    #     self.ui.adm6_text.setText(config_holder.DISP.adm6)
    #     self.ui.k4_key_text.setText(config_holder.DISP.K4)
    #     self.ui.op_key_text.setText(config_holder.DISP.op)
    #     self.ui.data_size_text.setText(str(config_holder.DISP.size))
    #     self.ui.pin1_rand_check.setChecked(bool(config_holder.DISP.pin1_fix))
    #     self.ui.pin2_rand_check.setChecked(bool(config_holder.DISP.pin2_fix))
    #     self.ui.puk1_rand_check.setChecked(bool(config_holder.DISP.puk1_fix))
    #     self.ui.puk2_rand_check.setChecked(bool(config_holder.DISP.puk2_fix))
    #     self.ui.adm1_rand_check.setChecked(bool(config_holder.DISP.adm1_fix))
    #     self.ui.adm6_rand_check.setChecked(bool(config_holder.DISP.adm6_fix))
    #     self.elect_gui.set_table_from_json(config_holder)
    #     self.graph_gui.set_table_from_json(config_holder)


    def show_tables(self):
        self.elect_gui.e_setDefault()
        self.graph_gui.g_setDefault()

    def update_text(self, field_name: str, param_name: str, expected_len: int):
        text = getattr(self.ui, f"{field_name}_text").text()
        if param_name == "DATA_SIZE" and text.isdigit() and int(text) > 0:
            getattr(self.parameters, f"set_{param_name}")(text)
        elif param_name == "ICCID" and len(text) in [18, 19, 20]:
            getattr(self.parameters, f"set_{param_name}")(text)
        elif len(text) == expected_len:
            getattr(self.parameters, f"set_{param_name}")(text)
        else:
            getattr(self.parameters, f"set_{param_name}")("")
            self.ui.textEdit.append(f"Enter valid {param_name}")

    def update_all_texts(self):
        fields = {
            "pin1": ("PIN1", 4), "pin2": ("PIN2", 4),
            "puk1": ("PUK1", 8), "puk2": ("PUK2", 8),
            "adm1": ("ADM1", 8), "adm6": ("ADM6", 8),
            "op_key": ("OP", 32), "k4_key": ("K4", 64),
            "data_size": ("DATA_SIZE", 1), "imsi": ("IMSI", 15),
            "iccid": ("ICCID", 20)
        }

        for field_name, (param_name, expected_len) in fields.items():
            print(field_name, param_name, expected_len)
            self.update_text(field_name, param_name, expected_len)

    def update_random_checks(self):
        checks = {
            "adm6_rand": "ADM6_RAND",
            "adm1_rand": "ADM1_RAND",
            "pin2_rand": "PIN2_RAND",
            "pin1_rand": "PIN1_RAND",
            "puk1_rand": "PUK1_RAND",
            "puk2_rand": "PUK2_RAND"
        }

        for check_name, param_name in checks.items():
            is_checked = getattr(self.ui, f"{check_name}_check").isChecked()
            getattr(self.parameters, f"set_{param_name}")(is_checked)

    def gui_to_global_params(self):
        self.update_random_checks()
        self.update_all_texts()
        self.parameters.set_ELECT_DICT((self.elect_gui.e_get_data_from_table()))
        self.parameters.set_GRAPH_DICT((self.graph_gui.get_data_from_table()))

        self.parameters.set_ELECT_CHECK()

    def global_params_to_json(self) -> json:
        param_dict:json = {
            "DISP": {
                "elect_data_sep": ".",
                "server_data_sep": ".",
                "graph_data_sep": ".",
                "K4": self.parameters.get_K4(),
                "op": self.parameters.get_OP(),
                "imsi": self.parameters.get_IMSI(),
                "iccid": self.parameters.get_ICCID(),
                "pin1": self.parameters.get_PIN1(),
                "puk1": self.parameters.get_PUK2(),
                "pin2": self.parameters.get_PIN1(),
                "puk2": self.parameters.get_PUK2(),
                "adm1": self.parameters.get_ADM1(),
                "adm6": self.parameters.get_ADM6(),
                "acc": self.parameters.get_ACC(),
                "size": self.parameters.get_DATA_SIZE(),
                "prod_check": self.parameters.get_PRODUCTION_CHECK(),
                "elect_check": self.parameters.get_ELECT_CHECK(),
                "graph_check": self.parameters.get_GRAPH_CHECK(),
                "server_check": self.parameters.get_SERVER_CHECK(),
                "pin1_fix": self.parameters.get_PIN1_RAND(),
                "puk1_fix": self.parameters.get_PUK1_RAND(),
                "pin2_fix": self.parameters.get_PIN2_RAND(),
                "puk2_fix": self.parameters.get_PUK2_RAND(),
                "adm1_fix": self.parameters.get_ADM1_RAND(),
                "adm6_fix": self.parameters.get_ADM6_RAND()
            },
            "PATHS": {
                "TEMPLATE_JSON": "operators/zong/template.json",
                "INPUT_FILE_PATH": "",
                "INPUT_CSV": "operators/zong/input_dataframe.csv",
                "OUTPUT_FILES_DIR": "output_files1",
                "OUTPUT_FILES_LASER_EXT": "laser_extracted"
            },
            "PARAMETERS": {
                "server_variables": dict_2_list(self.parameters.get_ELECT_DICT()),
                "data_variables": dict_2_list(self.parameters.get_ELECT_DICT()),
                "laser_variables": self.parameters.get_GRAPH_DICT()
            }
        }
#        print(param_dict)
#        j = json.dumps(param_dict)

        return param_dict



    def global_params_to_gui(self, params):
        self.ui.imsi_text.setText(params.get_IMSI())
        self.ui.iccid_text.setText(params.get_ICCID())
        self.ui.pin1_text.setText(params.get_PIN1())
        self.ui.puk1_text.setText(params.get_PUK1())
        self.ui.pin2_text.setText(params.get_PIN2())
        self.ui.puk2_text.setText(params.get_PUK2())
        self.ui.adm1_text.setText(params.get_ADM1())
        self.ui.adm6_text.setText(params.get_ADM6())
        self.ui.k4_key_text.setText(params.get_K4())
        self.ui.op_key_text.setText(params.get_OP())
        self.ui.data_size_text.setText(params.get_DATA_SIZE())
        self.ui.pin1_rand_check.setChecked(bool(params.get_PIN1_RAND()))
        self.ui.pin2_rand_check.setChecked(bool(params.get_PIN2_RAND()))
        self.ui.puk1_rand_check.setChecked(bool(params.get_PUK1_RAND()))
        self.ui.puk2_rand_check.setChecked(bool(params.get_PUK2_RAND()))
        self.ui.adm1_rand_check.setChecked(bool(params.get_ADM1_RAND()))
        self.ui.adm6_rand_check.setChecked(bool(params.get_ADM6_RAND()))
        self.graph_gui.g_setDefault()
        self.elect_gui.e_setDefault()

    @staticmethod
    def json_to_global_params(config_holder, params):
        params.set_SERVER_SEP(config_holder.DISP.server_data_sep)
        params.set_ELECT_SEP(config_holder.DISP.elect_data_sep)
        params.set_GRAPH_SEP(config_holder.DISP.graph_data_sep)
        params.set_K4(config_holder.DISP.K4)
        params.set_OP(config_holder.DISP.op)
        params.set_IMSI(config_holder.DISP.imsi)
        params.set_ICCID(config_holder.DISP.iccid)
        params.set_PIN1(config_holder.DISP.pin1)
        params.set_PUK1(config_holder.DISP.puk1)
        params.set_PIN2(config_holder.DISP.pin2)
        params.set_PUK2(config_holder.DISP.puk2)
        params.set_ADM1(config_holder.DISP.adm1)
        params.set_ADM6(config_holder.DISP.adm6)
        params.set_DATA_SIZE(config_holder.DISP.size)

        params.set_PRODUCTION_CHECK(False)
        params.set_ELECT_CHECK(config_holder.DISP.elect_check)
        params.set_GRAPH_CHECK(config_holder.DISP.graph_check)
        params.set_SERVER_CHECK(config_holder.DISP.server_check)

        params.set_SERVER_DICT(list_2_dict(config_holder.PARAMETERS.server_variables))
        params.set_ELECT_DICT(list_2_dict(config_holder.PARAMETERS.data_variables))
        params.set_GRAPH_DICT(config_holder.PARAMETERS.laser_variables)
            #  params.set_INPUT_PATH("C:/Users/hamza.qureshi/Desktop/STC_APP/improvements/dataGen-v17/input.csv")
        params.set_INPUT_PATH(config_holder.PATHS.INPUT_FILE_PATH)

            # ========================================#
            # ========================================#
            # ========================================#

        params.set_PIN1_RAND(config_holder.DISP.pin1_fix)
        params.set_PUK1_RAND(config_holder.DISP.puk1_fix)
        params.set_PIN2_RAND(config_holder.DISP.pin2_fix)
        params.set_PUK2_RAND(config_holder.DISP.puk2_fix)
        params.set_ADM1_RAND(config_holder.DISP.adm1_fix)
        params.set_ADM6_RAND(config_holder.DISP.adm6_fix)
    #        params.set_ACC_RAND(config_holder.DISP.pin1_rand)
