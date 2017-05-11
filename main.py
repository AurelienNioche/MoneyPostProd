# -*- coding: utf-8 -*-
import sys
import numpy as np
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QFileDialog, QHBoxLayout, QMessageBox, QLabel, QPushButton
from json_converter_gui import JsonConverterWindow
from main_graph import MainGraph
from player_score_viewer import ScoreWindow
import pickle
import os


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        self.layout = QHBoxLayout(self)

        self.graph = QPushButton("Compute figures")
        self.score = QPushButton("Print scores")
        self.json = QPushButton("JSON Converter")
       
        self.buttons = [self.graph, self.score, self.json]

        self.graph.clicked.connect(self.compute_figures)
        self.score.clicked.connect(self.view_players_scores)
        self.json.clicked.connect(self.convert_to_json)

        self.init_UI()
    
    def compute_figures(self):

        mywin = GraphWindow()

    def view_players_scores(self):

        mywin = ScoreWindow()
        
    def convert_to_json(self):

        mywin = JsonConverterWindow()

    def fill_layout(self):
        
        for btn in self.buttons:
            self.layout.addWidget(btn)

    def init_UI(self):

        self.fill_layout()
        self.setWindowTitle("AndroidExperiment: Main post prod")
        self.setGeometry(200, 200, 500, 100)
        self.show()

    @staticmethod
    def main():

        app = QApplication(sys.argv)
        win = MainWindow()
        sys.exit(app.exec_()) 

if __name__ == '__main__':

    MainWindow.main() 
