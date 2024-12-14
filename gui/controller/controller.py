
from gui.table import GuiElect, GuiGraph, GuiExtractor
from gui.controller.ulits import GuiButtons, GuiCheckBox, TextLengthValidator

class Controller:
    def __init__(self, ui):
        self.ui = ui

        self.elect_gui = GuiElect(self.ui)
        self.graph_gui = GuiGraph(self.ui)
        self.button_gui = GuiButtons(self.ui)
        self.extractor_gui = GuiExtractor(self.ui)
        self.checkbox_gui = GuiCheckBox(self.ui)
        self.text_validator = TextLengthValidator(self.ui)

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

        self.ui.de_add_text.clicked.connect(self.extractor_gui.de_add_text_to_table)
        self.ui.de_del_text.clicked.connect(self.extractor_gui.de_delete_selected_row)
        self.ui.de_up_button.clicked.connect(self.extractor_gui.de_move_selected_row_up)
        self.ui.de_dn_button.clicked.connect(self.extractor_gui.de_move_selected_row_down)
        self.ui.de_default.clicked.connect(self.extractor_gui.de_setDefault)

