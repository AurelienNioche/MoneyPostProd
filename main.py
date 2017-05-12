# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton
from subprocess import Popen


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.layout = QHBoxLayout(self)

        graph = QPushButton("Compute figures")
        score = QPushButton("Print scores")
        json = QPushButton("JSON Converter")
        video = QPushButton("Assemble video")

        graph.clicked.connect(self.compute_figures)
        score.clicked.connect(self.view_players_scores)
        json.clicked.connect(self.convert_to_json)
        video.clicked.connect(self.convert_video)

        self.buttons = [json, graph, video, score]

        self.init_UI()

    @staticmethod
    def convert_video():

        Popen(["python", "video_converter_gui.py"])

    @staticmethod
    def compute_figures():

        Popen(["python",  "graph_gui.py"])

    @staticmethod
    def view_players_scores():

        Popen(["python",  "player_score_viewer.py"])

    @staticmethod
    def convert_to_json():

        Popen(["python",  "json_converter_gui.py"])

    def fill_layout(self):
        
        for btn in self.buttons:
            self.layout.addWidget(btn)

    def init_UI(self):

        self.fill_layout()
        self.setWindowTitle("AndroidExperiment: Main post prod")
        self.show()


def main():

    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_()) 

if __name__ == '__main__':

   main() 
