from PyQt5.QtWidgets import \
    QApplication, QMessageBox, QWidget, QFileDialog, QProgressBar, QLabel, QGridLayout
from os import path, getenv, mkdir
import sys
from subprocess import Popen


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.label = QLabel(self)
        self.prog = QProgressBar(self)

        self.file_path = None
        self.save_path = None

        self.init()
        self.init_UI()

    def init(self):

        self.get_file_path()

        if self.file_path:

            self.get_save_path()
            self.generate_fig()

    def init_UI(self):

        self.setWindowTitle("AndroidExperiment: MainGraph")
        self.prog.setValue(100)

        self.label.setText("Figures are generated!")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.prog)

        self.show()

    @staticmethod
    def show_error(msg):

        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle("Error")
        msgbox.setText(msg)
        close = msgbox.addButton("Close", QMessageBox.ActionRole)

        msgbox.exec_()

        if msgbox.clickedButton() == close:
            sys.exit()

    def get_save_path(self):

        split_path = self.file_path.split("/")

        root_folder = "/" + path.join(*split_path[:-1])
        file_name = split_path[-1].split(".")[0]

        save_path = root_folder + "/Fig_" + file_name

        if not path.exists(save_path):
            mkdir(save_path)
        self.save_path = save_path

    def get_file_path(self):

        expected_dir = path.expanduser("~/Desktop/AndroidXP")
        if path.exists(expected_dir):
            directory = expected_dir
        else:
            directory = getenv("HOME")

        file_path = QFileDialog.getOpenFileName(
            self, 'Open file', directory,
            "Json files (*.json )")[0]

        if file_path:
            self.file_path = file_path

        else:
            self.show_error("Selecting a file is required to proceed.")

    def generate_fig(self):

        Popen(["python", "main_graph.py", self.file_path, self.save_path])


def main():

    app = QApplication(sys.argv)
    win = GraphWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

