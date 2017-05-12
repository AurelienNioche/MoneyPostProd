# -*- coding: utf-8 -*-
import sys
import numpy as np
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QFileDialog, QHBoxLayout, QMessageBox, QLabel, QPushButton
from subprocess import Popen
import pickle
import os


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

        self.buttons = [graph, score, json, video]

        self.init_UI()
    
    def convert_video(self):

        Popen(["python", "video_converter_gui.py"])

    def compute_figures(self):

        Popen(["python",  "graph_gui.py"])

    def view_players_scores(self):

        Popen(["python",  "player_score_viewer.py"])

    def convert_to_json(self):

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
