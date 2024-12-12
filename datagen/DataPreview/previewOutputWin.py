from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QTableWidgetItem, QDialog
from forms.df_ui import Ui_Dialog
import pandas as pd

# =================================#


app = QApplication([])


class PreviewOutput(QDialog):  # testing purpose only
    def __init__(
        self,
        dataframe_elect,
        dataframe_graph,
        dataframe_server,
        elect_labels: bool,
        graph_labels: bool,
        server_labels: bool,
    ):
        super().__init__()
        self.ui = Ui_Dialog()

        self.ui.setupUi(self)
        self.installEventFilter(self)

        availabe_screen = app.primaryScreen().availableGeometry()
        self.setFixedSize(availabe_screen.width(), availabe_screen.height())

        self.populate_table_widget(self.ui.elect_tableWidget, dataframe_elect)
        elect_labels_header = list(dataframe_elect.columns)
        if elect_labels:
            self.ui.elect_tableWidget.setHorizontalHeaderLabels(elect_labels_header)

        self.populate_table_widget(self.ui.graph_tableWidget, dataframe_graph)
        graph_labels_header = list(dataframe_graph.columns)
        if graph_labels:
            self.ui.graph_tableWidget.setHorizontalHeaderLabels(graph_labels_header)

        self.populate_table_widget(self.ui.server_tableWidget, dataframe_server)
        server_labels_header = list(dataframe_server.columns)
        if server_labels:
            self.ui.server_tableWidget.setHorizontalHeaderLabels(server_labels_header)

    # def populate_table_widget(self, table_widget, data_frame):
    #     table_widget.setRowCount(data_frame.shape[0])
    #     table_widget.setColumnCount(data_frame.shape[1])
    #     for row in range(data_frame.shape[0]):
    #         for column in range(data_frame.shape[1]):
    #             item = QTableWidgetItem(str(data_frame.iat[row, column]))
    #             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #             table_widget.setItem(row, column, item)
    #     table_widget.resizeColumnsToContents()

    def populate_table_widget(self, table_widget, data_frame):
        table_widget.setRowCount(data_frame.shape[0])
        table_widget.setColumnCount(data_frame.shape[1])

        for row in range(data_frame.shape[0]):
            for column in range(data_frame.shape[1]):
                item = QTableWidgetItem(str(data_frame.iat[row, column]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table_widget.setItem(row, column, item)

            # Set the vertical header (index) to be center-aligned
            v_item = QTableWidgetItem(str(row))
            v_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table_widget.setVerticalHeaderItem(row, v_item)

        table_widget.resizeColumnsToContents()


# app = QtWidgets.QApplication([])
# dialog = MyDialog()
# button = QtWidgets.QPushButton("Click Me")
# button.clicked.connect(dialog.on_button_clicked)

# layout = QtWidgets.QVBoxLayout(dialog)
# layout.addWidget(button)

# dataframe_elect = pd.DataFrame()
# dataframe_laser = pd.DataFrame()

# dataframe_elect = pd.read_csv("Input Files/demo2.csv")
# dataframe_laser = pd.read_csv("Input Files/demo2.csv")
# dataframe_server = pd.read_csv("Input Files/demo2.csv")

# w = PreviewOutput(dataframe_laser,dataframe_elect,dataframe_server,True,False,True)
# w.show()
# app.exec()
