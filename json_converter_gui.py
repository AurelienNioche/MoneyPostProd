import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QLabel, QGridLayout, QMessageBox, QProgressBar
from PyQt5.QtCore import Qt
import os
import json
import pickle
import numpy as np
from os import path


class JsonConverterWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.save_path = None
        self.data = None

        self.layout = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.label)

        self.init()
        self.init_UI()

    def init(self):

        self.get_file_path()
        if self.file_path:
            self.get_save_path()
            self.import_data()
            self.add_market_choice()
            self.convert_data()

    def init_UI(self):

        prog = QProgressBar(self)
        prog.setValue(100)
        self.layout.addWidget(prog)
        self.label.setText("Conversion is done!" + self.label.text())

        self.label.setText(
            "\n Used file is '{file_path:}'"
            "\n Json file is saved to '{save_path:}'".format(file_path=self.file_path,
                                                             save_path=self.save_path)
        )

        self.setWindowTitle("JSON converter")
        self.show()

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

    def get_save_path(self):

        split_path = self.file_path.split("/")
        root_folder = "/" + path.join(*split_path[:-1])
        file_name = split_path[-1].split(".")[0]
        save_path = root_folder + "/" + file_name + ".json"
        self.save_path = save_path

    def get_file_path(self):

        expected_dir = path.expanduser("~/Desktop/AndroidXP")
        if path.exists(expected_dir):
            directory = expected_dir
        else:
            directory = os.getenv("HOME")

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

    def convert_data(self):
        
        # to_json implicitly call convert_array_to_list
        JsonConverter.to_json(self.data, output=self.save_path)
        
    def add_market_choice(self):

        t_max = len(self.data["hist_choice"])
        n = len(self.data["hist_choice"][0])

        market_choice = np.ones((t_max, n, 2), dtype=int) * - 1

        for t in range(t_max):

            for i in range(n):

                if t == 0:
                    in_hand = self.data["p"][i]

                else:
                    in_hand = self.data["hist_h"][t - 1][i]

                market_choice[t, i, 0] = in_hand
                market_choice[t, i, 1] = self.get_desired_good(
                    i=i, choice=self.data["hist_choice"][t][i],
                    in_hand=in_hand
                )
        
        self.data["market_choice"] = market_choice

    def get_desired_good(self, i, choice, in_hand):

        if choice == 1:
            return self.data["c"][i]

        else:
            if in_hand == self.data["p"][i]:
                return (self.data["p"][i] + 2) % 3

            else:
                return self.data["p"][i]


class JsonConverter(object):

    @staticmethod
    def to_json(data, output="data.json"):

        json_data = dict()

        for key, value in data.items():

            if type(value) == np.int64:
                json_data[key] = int(value)

            elif type(value) == np.float64:
                json_data[key] = float(value)

            elif type(value) == np.ndarray:
                json_data[key] = JsonConverter.convert_array_into_list(value)

            elif type(value) == list:

                if value and type(value[0]) == np.ndarray:
                    json_data[key] = JsonConverter.convert_array_into_list(value)

                else:
                    json_data[key] = value

            else:
                json_data[key] = value

        with open(output, "w") as file:
            json.dump(json_data, file)

    @classmethod
    def convert_array_into_list(cls, value):

        if type(value[0]) == np.int64:
            return [int(i) for i in value]

        elif type(value[0]) == np.float64:
            return [float(i) for i in value]

        elif type(value[0]) == np.ndarray:
            return [cls.convert_array_into_list(i) for i in value]

        else:
            raise Exception("Type not expected: {}.".format(type(value[0])))


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    win = JsonConverterWindow()
    sys.exit(app.exec_()) 

