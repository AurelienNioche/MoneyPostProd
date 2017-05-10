import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QLabel, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt

import os
import json
import pickle
import numpy as np


class JsonConverterWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.save_path = None
        self.save_file_name = "/last_data.json"

        self.layout = QGridLayout(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.label)
        self.data = None
        self.init()
        self.init_UI()

    def init(self):

        self.get_save_path()
        self.import_data()
        self.add_market_choice()
        self.convert_data()

    def init_UI(self):

        self.setWindowTitle("JSON converter")
        self.show()

    def get_save_path(self):

        self.save_path = QFileDialog.getExistingDirectory(self, 'Select where you want to save your data.', os.getenv("HOME"))

        if not self.save_path:

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("Error")
            msgbox.setText("Selecting a file is required to proceed")
            close = msgbox.addButton("Close", QMessageBox.ActionRole)

            msgbox.exec_()

            if msgbox.clickedButton() == close:
                sys.exit()
        else:

            self.save_path += self.save_file_name

    def import_data(self):
        
        file_path = QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        
        if file_path:
            self.data = pickle.load(open(file_path, "rb"))
            self.label.setText(
                "Done converting..."
                "\n Used file is '{file_path:}'"
                "\n Json file is saved to '{save_path:}'".format(file_path=file_path,
                                                                 save_path=self.save_path)
            )

        else:
            self.label.setText("Selecting a file is required!")

    def convert_data(self):
        
        # to_json implicitly call convert_array_to_list
        JsonConverter.to_json(self.data, output=self.save_path)
        
    def add_market_choice(self):
        
        market_choice = []
        
        # create t list containing n agent choice
        for array in self.data["hist_choice"]:
            market_choice.append(self.get_real_good(array))
        
        for t in range(len(self.data["hist_h"])):
            for idx in range(len(market_choice[0])):
                if idx != 0:
                    market_choice[t][idx][1] = int(self.data["hist_h"][t - 1][idx])
                else:
                    market_choice[t][idx][1] = int(self.data["p"][idx])
        
        self.data["market_choice"] = market_choice

    def get_real_good(self, array):
        return [[int(self.get_desired_good(i, value)), -1] for i, value in enumerate(array)]

    def get_desired_good(self, i, value):

        if value == 1:
            return self.data["c"][i]

        else:
            if value == self.data["p"][i]:
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

        print("Done converting...")

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

