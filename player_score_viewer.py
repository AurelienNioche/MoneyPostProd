# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QFileDialog,
                             QGridLayout, QMessageBox, QLabel)
import pickle
import os


class ScoreWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.data = None

        self.import_data()

        self.nplayer = len(self.data["p"])
        print(self.nplayer)
        self.sorted_data = [{"p": None, "reward": None} for i in range(self.nplayer)]

        self.sort_data()

        self.layout = QGridLayout(self)
        self.fill_layout()

        self.init_UI()

    def import_data(self):

        file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getenv("HOME"))[0]

        if not file_path:

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("Error")
            msgbox.setText("Selecting a file is required to proceed")
            close = msgbox.addButton("Close", QMessageBox.ActionRole)

            msgbox.exec_()
        
            if msgbox.clickedButton() == close:
                sys.exit()
        else:
            self.data = pickle.load(open(file_path, "rb"))

    def sort_data(self):

        for i, idx in enumerate(self.data["server_id_in_use"]):
            self.sorted_data[idx]["p"] = self.data["p"][i]
            self.sorted_data[idx]["reward"] = self.data["reward_amount"][i]

    def fill_layout(self):

        coord = ((x, y) for x in range(7) for y in range(15))

        for idx, data in enumerate(self.sorted_data):
            info = QLabel(self)
            info.setText("id: {}  ".format(idx)
                         + "type: {}  ".format(data["p"])
                         + "reward: {}  ".format(data["reward"]))

            my_coord = next(coord)

            self.layout.addWidget(info, my_coord[1], my_coord[0])

    def init_UI(self):

        self.setStyleSheet("border: 1px solid #5D5D5C;")
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("AndroidExperiment: player's stats")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ScoreWindow()
    sys.exit(app.exec_())
