# from globals.parameters import Parameters
from globals import Parameters
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QTableWidgetItem,
)

from .utils import parameter_len
# from core.executor.utils import list_2_dict


class GuiElect:
    tableWidgetHeader = ["Variables", "Clip", "length"]

    def __init__(self, ui):
        self.default_elect = None
        self.ui = ui
        self.parameters = Parameters.get_instance()

        self.ui.e_tableWidget.setHorizontalHeaderLabels(GuiElect.tableWidgetHeader)

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

            e_combo_box = QComboBox()
            e_combo_box.addItems(drop_down_menu)
            e_combo_box.setDisabled(True)
            self.ui.e_tableWidget.setCellWidget(row_count, 1, e_combo_box)

            col3 = QTableWidgetItem("0-" + parameter_len(text[0].lstrip()))
            #            col3 = QTableWidgetItem(text[2])
            self.ui.e_tableWidget.setItem(row_count, 2, col3)
            col3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def e_add_text_to_table(self):
        self.ui.e_tableWidget.setHorizontalHeaderLabels(["Variables", "Clip", "length"])
        text = self.ui.e_comboBox.currentText()
        self.e_table_append([text, "Normal", "0-" + parameter_len(text).lstrip()])

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

    # ===================================================================================#
    # ===================================================================================#
    # =========================GRAPHICAL DATA FUNCTIONS==================================#
    # ===================================================================================#
    # ===================================================================================#


class GuiGraph:
    tableWidgetHeader = ["Variables", "Clip", "length"]

    def __init__(self, ui):
        self.default_graph = None
        self.combo_box = None
        self.ui = ui
        self.parameters = Parameters.get_instance()
        self.ui.tableWidget.setHorizontalHeaderLabels(GuiGraph.tableWidgetHeader)

    def g_setDefault(self):
        d = self.parameters.get_GRAPH_DICT()
        for items in d:
            self.g_table_append(d[items][0], d[items][2])

    def g_getDefault(self):
        self.default_graph = self.get_data_from_table()

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

    def g_clear_table(self):
        rows = self.ui.tableWidget.rowCount()
        for row in range(rows):
            self.ui.tableWidget.removeRow(row)

    def add_text_to_table(self):
        #        drop_down_menu = ['Normal', 'Right','Center', 'Left']
        self.ui.tableWidget.setHorizontalHeaderLabels(["Variables", "Clip", "length"])

        text = self.ui.comboBox.currentText()
        self.g_table_append(text, "0-" + parameter_len(text.lstrip()))

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

    # ===================================================================================#
    # ===================================================================================#
    # ========================EXTRACTOR DATA FUNCTIONS==================================#
    # ===================================================================================#
    # ===================================================================================#


class GuiExtractor:
    extractor_columns = []

    def __init__(self, ui):
        self.combo_box = None
        self.ui = ui
        self.parameters = Parameters.get_instance()

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

            col3 = QTableWidgetItem("0-" + parameter_len(text.lstrip()))
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


__all__ = ["GuiElect", "GuiGraph", "GuiExtractor"]
