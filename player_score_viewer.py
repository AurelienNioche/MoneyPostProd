# -*- coding: utf-8 -*-
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QGridLayout, QMessageBox, QLabel
import pickle
from os import path, getenv


class ScoreWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.file_path = None
        self.data = None
        self.sorted_data = None

        self.layout = QGridLayout(self)

        self.init()

        self.init_UI()

    def init(self):

        self.get_file_path()
        if self.file_path:
            self.import_data()
            self.sort_data()

    @staticmethod
    def show_error():

        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle("Error")
        msgbox.setText("Selecting a file is required to proceed.")
        close = msgbox.addButton("Close", QMessageBox.ActionRole)

        msgbox.exec_()

        if msgbox.clickedButton() == close:
            sys.exit()

    def get_file_path(self):

        expected_dir = path.expanduser("~/Desktop/AndroidXP")
        if path.exists(expected_dir):
            directory = expected_dir
        else:
            directory = getenv("HOME")

        print("Directory", directory)
        file_path = QFileDialog.getOpenFileName(
            self, 'Open file', directory,
            "Pickle files (*.p )")[0]

        if file_path:
            self.file_path = file_path

        else:
            self.show_error()

    def import_data(self):

        self.data = pickle.load(open(self.file_path, "rb"))

    def sort_data(self):

        n = len(self.data["p"])
        self.sorted_data = [{"id": None, "p": None, "reward": None} for i in range(n)]
        
        arg = np.argsort(self.data["server_id_in_use"])
            
        for idx in range(n):
            self.sorted_data[idx]["id"] = self.data["server_id_in_use"][arg[idx]]
            self.sorted_data[idx]["p"] = self.data["p"][arg[idx]]
            self.sorted_data[idx]["reward"] = self.data["reward_amount"][arg[idx]]

    def fill_layout(self):

        coord = ((x, y) for y in range(12) for x in range(12))

        for data in self.sorted_data:
            info = QLabel(self)
            info.setText("id: {}  ".format(data["id"])
                         + "type: {}  ".format(data["p"])
                         + "reward: {}  ".format(data["reward"]))

            # generate new coordinates
            my_coord = next(coord)

            self.layout.addWidget(info, my_coord[0], my_coord[1])

    def init_UI(self):
        
        self.fill_layout()

        self.setStyleSheet("border: 1px solid #5D5D5C;")
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("AndroidExperiment: player's stats")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ScoreWindow()
    sys.exit(app.exec_())
