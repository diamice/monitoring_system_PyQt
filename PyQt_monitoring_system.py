import sys
import mysql.connector

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTableWidget, \
    QPushButton, QRadioButton, QDateEdit, QFrame, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QHeaderView

from config import connection_config
from temp_funcs import engine_avg_temp, engine_temperature
from axis_funcs import axis_status_finder
from log_messages import log_list


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Система мониторинга")
        layout = QHBoxLayout()

        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("static/images/logo.png"))
        left_layout.addWidget(logo_label)

        machine_type_combo = QComboBox()
        machine_name_combo = QComboBox()

        machine_types = self.type_of_machine()
        machine_names = self.name_of_machine()

        machine_type_combo.addItems(machine_types)
        machine_name_combo.addItems(machine_names)

        label_type = QLabel("Тип станка:")
        label_name = QLabel("Наименование станка:")

        left_layout.addSpacing(50)
        left_layout.addWidget(label_type)
        left_layout.addSpacing(0)
        left_layout.addWidget(machine_type_combo)
        left_layout.addSpacing(50)
        left_layout.addWidget(label_name)
        left_layout.addSpacing(0)
        left_layout.addWidget(machine_name_combo)
        left_layout.addSpacing(30)

        machine_image_pixmap = QPixmap("static/images/stanok.jpg")
        machine_image_pixmap = machine_image_pixmap.scaled(machine_image_pixmap.width() // 2,
                                                           machine_image_pixmap.height() // 2)
        machine_image_label = QLabel()
        machine_image_label.setPixmap(machine_image_pixmap)
        machine_image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(machine_image_label)

        label_machine = QLabel("Mazak MultiTasker X7-2000")
        label_machine.setAlignment(Qt.AlignCenter)
        label_machine.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(label_machine)

        button_layout = QHBoxLayout()

        for item in ['X', 'Y', 'Z', 'A', 'C']:
            button = QPushButton(item)
            button.setMinimumSize(30, 30)
            button_layout.addWidget(button)

        left_layout.addLayout(button_layout)

        mode_button = QPushButton("Mode: Auto")
        mode_button.clicked.connect(self.toggle_mode)
        button_layout.addWidget(mode_button)

        central_layout = QVBoxLayout()

        temperature_table = QTableWidget(self)
        central_layout.addWidget(temperature_table)
        temperature_table.setFixedSize(900, 174)
        self.populate_temperature_table(temperature_table)

        axis_table = QTableWidget(self)
        axis_table.setFixedSize(301, 211)
        axis_layout = QVBoxLayout()
        axis_layout.addWidget(axis_table)

        image_label = QLabel(self)
        image_path = "static/images/temperature_plot.png"
        image_label.setPixmap(QPixmap(image_path))
        image_label.setScaledContents(True)
        image_label.setFixedSize(600, 250)

        axis_widget = QWidget()
        axis_widget.setLayout(axis_layout)

        table_and_image_layout = QHBoxLayout()

        table_and_image_layout.addWidget(axis_widget)

        table_and_image_layout.addWidget(image_label)

        central_layout.addLayout(table_and_image_layout)

        self.make_axis_table(axis_table)

        filter_group = QFrame()
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.addWidget(QRadioButton("Важные"))
        filter_layout.addWidget(QDateEdit())
        filter_layout.addWidget(QRadioButton("Ошибка выполнения"))
        filter_layout.addWidget(QRadioButton("Все сообщения"))

        central_layout.addWidget(filter_group)

        message_table = QTableWidget(self)
        message_table.setFixedSize(900, 160)
        central_layout.addWidget(message_table)
        self.make_message_table(message_table)

        layout.addWidget(left_frame, stretch=1)
        layout.addLayout(central_layout, stretch=4)

        left_frame.setMinimumWidth(350)
        self.setLayout(layout)
        self.setFixedSize(1300, 700)

    def populate_temperature_table(self, table):
        engine_data = sorted(engine_temperature(connection_config))
        avg_data = sorted(engine_avg_temp(connection_config))

        table.setColumnCount(len(engine_data))
        table.setRowCount(4)

        horizontal_headers = [data_row[0] for data_row in engine_data]
        table.setHorizontalHeaderLabels(horizontal_headers)

        table.setSpan(0, 0, 1, len(engine_data))
        item = QTableWidgetItem("Температура Двигателей")
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(0, 0, item)

        for col_num, data_row in enumerate(engine_data):
            item = QTableWidgetItem(str(data_row[1]))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(1, col_num, item)

        table.setSpan(2, 0, 1, len(engine_data))
        avg_item = QTableWidgetItem("Средняя температура")
        avg_item.setTextAlignment(Qt.AlignCenter)
        table.setItem(2, 0, avg_item)

        for col_num, avg_row in enumerate(avg_data):
            item = QTableWidgetItem(str(avg_row[1]))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(3, col_num, item)


        table.verticalHeader().setVisible(False)

        # Set resizing mode for columns
        header = table.horizontalHeader()
        for col_num in range(table.columnCount()):
            header.setSectionResizeMode(col_num, QHeaderView.Stretch)

        header_font = QFont("Arial", 6, QFont.Bold)
        header.setFont(header_font)
        table.setStyleSheet("QTableWidget { gridline-color: #000000; border: 1px solid #000000; }"
                            "QHeaderView::section { border: 1px solid #000000; }")
        table.setAlternatingRowColors(True)

    def make_axis_table(self, table):
        axis_list = sorted(axis_status_finder(connection_config), key=lambda x: x[3], reverse=True)
        table.setColumnCount(3)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(["Ось", "Статус готовности", "Дата и время"])
        table.verticalHeader().setVisible(False)

        for row_num, row_data in enumerate(axis_list):
            for col_num, value in enumerate(row_data[1:]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_num, col_num, item)

                if col_num == 2:
                    formatted_datetime = value.strftime("%b. %d, %Y, %I:%M %p")
                    item.setText(formatted_datetime)

        header = table.horizontalHeader()
        for col_num in range(table.columnCount()):
            header.setSectionResizeMode(col_num, QHeaderView.ResizeToContents)

        header_font = QFont("Arial", 6, QFont.Bold)
        header.setFont(header_font)
        table.setStyleSheet("QTableWidget { gridline-color: #000000; border: 1px solid #000000; }"
                            "QHeaderView::section { border: 1px solid #000000; }")
        table.setAlternatingRowColors(True)

    def make_message_table(self, table):
        messages = sorted(log_list(connection_config), key=lambda x: x[4], reverse=True)
        table.setColumnCount(5)
        table.setRowCount(3)
        table.setHorizontalHeaderLabels(["Тип сообщения", "Приоритет", "Код", "Описание", "Дата и время"])
        for row_num, message_data in enumerate(messages):
            for col_num, value in enumerate(message_data[1:]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_num, col_num, item)

            formatted_datetime = message_data[5].strftime("%b. %d, %Y, %I:%M %p")
            item = QTableWidgetItem(formatted_datetime)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_num, 4, item)
        table.verticalHeader().setVisible(False)
        header = table.horizontalHeader()
        for col_num in range(table.columnCount()):
            header.setSectionResizeMode(col_num, QHeaderView.ResizeToContents)

        header_font = QFont("Arial", 6, QFont.Bold)
        header.setFont(header_font)
        table.setStyleSheet("QTableWidget { gridline-color: #000000; border: 1px solid #000000; }"
                            "QHeaderView::section { border: 1px solid #000000; }")
        table.setAlternatingRowColors(True)

    def toggle_mode(self):
        current_mode = self.sender().text()
        new_mode = "Mode: Auto" if current_mode == "Mode: MDI" else "Mode: MDI"
        self.sender().setText(new_mode)

    def type_of_machine(self):
        with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
            query = """
             SELECT
             type
             FROM
             data_for_monitoring_system.machine_type
             """
            cursor.execute(query)
            machine_types = [row[0] for row in cursor.fetchall()]
        return machine_types

    def name_of_machine(self):
        with mysql.connector.connect(**connection_config) as connection, connection.cursor() as cursor:
            query = """
             SELECT
             model_name
             FROM
             data_for_monitoring_system.machine_name
             """
            cursor.execute(query)
            machine_names = [row[0] for row in cursor.fetchall()]
        return machine_names


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
