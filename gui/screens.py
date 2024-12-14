#from gui.forms import Ui_Dialog as input_ui
from gui.forms.df_ui import Ui_Dialog as input_ui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QTableWidgetItem, QDialog
from gui.forms.df_ui import Ui_Dialog


# =================================#

app = QApplication([])


class PreviewInput(QDialog):  # testing purpose only
    def __init__(self, dataframe):
        super().__init__()
        self.ui = input_ui()
        self.ui.setupUi(self)
        availabe_screen = app.primaryScreen().availableGeometry()
        self.setFixedSize(availabe_screen.width(), availabe_screen.height())
        self.showMaximized()

        self.populate_table_widget(self.ui.inputWidget, dataframe)
        header_labels = list(dataframe.columns)
        self.ui.inputWidget.setHorizontalHeaderLabels(header_labels)


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

    # def get_var_df(self, contents):
    #     pattern = r"(\w+)\s*:\s*(.+)"
    #     flags = re.UNICODE
    #     matches = re.findall(pattern, contents, flags=flags)
    #     dict1 = {}
    #     for match in matches:
    #         variable = match[0]
    #         value = match[1]
    #         dict1[variable] = value

    #     # Extract DataFrame content
    #     df_start = contents.find("var_out:")
    #     df_content = contents[df_start + len("var_out:") :]

    #     # Create DataFrame from the content
    #     data = [line.split() for line in df_content.split("\n") if line.strip()]
    #     column_names = data[0]
    #     df_data = data[1:]
    #     df = pd.DataFrame(df_data, columns=column_names)
    #     return df, dict1


# df_input = pd.read_csv("Input Files/input1.csv")
# w = PreviewInput(df_input)
# w.show()
# app.exec()


# =================================#


# app = QApplication([])


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
