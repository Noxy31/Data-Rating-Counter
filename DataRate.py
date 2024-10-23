# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from decimal import Decimal
import datetime
import os
import subprocess

class Ui_DataRating(object):
    def setupUi(self, DataRating):
        DataRating.setObjectName("DataRating")
        DataRating.setMinimumSize(280, 225)

        self.centralWidget = QtWidgets.QWidget(DataRating)
        DataRating.setCentralWidget(self.centralWidget)

        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)

        self.FreeValue = QtWidgets.QTextEdit(self.centralWidget)
        self.FreeValue.setMaximumHeight(30)
        self.gridLayout.addWidget(self.FreeValue, 1, 0, 1, 2)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setMinimumHeight(40)
        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 2)

        self.TotalFrame = QtWidgets.QFrame(self.centralWidget)
        self.TotalFrame.setObjectName("TotalFrame")

        self.gridLayout.addWidget(self.TotalFrame, 3, 0, 1, 2)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.TotalFrame)

        self.Btotal = QtWidgets.QPushButton(self.TotalFrame)
        self.Btotal.setObjectName("Btotal")
        self.horizontalLayout.addWidget(self.Btotal)

        self.label_34 = QtWidgets.QLabel(self.TotalFrame)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout.addWidget(self.label_34)

        self.result = QtWidgets.QLabel(self.TotalFrame)
        self.result.setObjectName("result")
        self.horizontalLayout.addWidget(self.result)

        self.SaveButton = QtWidgets.QPushButton(self.centralWidget)
        self.SaveButton.setObjectName("SaveButton")
        self.gridLayout.addWidget(self.SaveButton, 4, 0, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)

        self.timer_label = QtWidgets.QLabel(self.centralWidget)
        self.timer_label.setObjectName("timer_label")

        timer_layout = QtWidgets.QHBoxLayout()
        timer_layout.addWidget(self.timer_label, alignment=QtCore.Qt.AlignCenter)
        self.gridLayout.addLayout(timer_layout, 5, 0, 1, 2)
        self.label_18 = QtWidgets.QLabel(self.centralWidget)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 6, 1, 1, 1, QtCore.Qt.AlignRight)

        self.retranslateUi(DataRating)
        QtCore.QMetaObject.connectSlotsByName(DataRating)

        self.total = Decimal(0)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_label.setText("00:00:00")
        self.timer.start(1000)


    def add_value(self, value):
        if value != "Total":
            self.total += Decimal(value)
            self.result.setText(str(self.total))
            print("Total:", self.total)
            self.timer_label.setText("00:00:00")

    def add_free_value(self):
        value = self.FreeValue.toPlainText()
        if value:
            self.add_value(value)

    def update_timer(self):
        time = self.timer_label.text()
        h, m, s = map(int, time.split(":"))
        elapsed_time = datetime.timedelta(hours=h, minutes=m, seconds=s) + datetime.timedelta(seconds=1)
        self.timer_label.setText(str(elapsed_time))

    def reset_total(self):
        self.total = Decimal(0)
        self.result.setText(str(self.total))

    def save_total(self):
        total_minutes = int(self.total)
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

        formatted_total = "Total: {} minutes ({} hours {} minutes)".format(total_minutes, total_hours,
                                                                           remaining_minutes)
        log_entry = "{} - {}\n".format(timestamp, formatted_total)

        desktop_path = os.path.expanduser("C:/Users/Nox/Desktop")
        log_folder = "Data Rating"
        folder_path = os.path.join(desktop_path, log_folder)
        filename = f"DataRate log.txt"
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "a") as file:
            file.write(log_entry)

        subprocess.Popen(["pythonw", ""], creationflags=subprocess.DETACHED_PROCESS,
                         close_fds=True)

    def convert_to_hours(self):
        if isinstance(self.total, Decimal):
            hours = int(self.total // 60)
            minutes = int(self.total % 60)
            self.result.setText("{:02d}:{:02d}".format(hours, minutes))

    def retranslateUi(self, DataRating):
        self.Btotal.clicked.connect(self.convert_to_hours)
        _translate = QtCore.QCoreApplication.translate
        DataRating.setWindowTitle(_translate("DataRating", "DataRater - Nox - 2023"))

        self.Btotal.setText(_translate("DataRating", "Total"))
        self.label_34.setText(_translate("DataRating", "="))
        self.SaveButton.setText(_translate("DataRating", "Save"))
        self.pushButton.setText(_translate("DataRating", "Clean")) 
        self.pushButton_2.setText(_translate("DataRating", "Add Value")) 
        self.timer_label.setText(_translate("DataRating", "00:00:00"))
        self.label_18.setText(_translate("DataRating", "Nox - 2023"))
        self.pushButton_2.clicked.connect(self.add_free_value)
        self.pushButton.clicked.connect(self.reset_total)
        self.SaveButton.clicked.connect(self.save_total)
        buttons = [attr for attr in dir(self) if attr.startswith("B")]
        for button_name in buttons:
            button = getattr(self, button_name)
            if isinstance(button, QtWidgets.QPushButton):
                button.clicked.connect(lambda checked, value=button.text().replace("B", ""): self.add_value(value))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DataRating = QtWidgets.QDialog()
    DataRating = QtWidgets.QMainWindow()
    ui = Ui_DataRating()
    ui.setupUi(DataRating)
    DataRating.show()
    sys.exit(app.exec_())
