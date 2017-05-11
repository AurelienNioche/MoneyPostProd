from PyQt5.QtWidgets import \
    QApplication, QMessageBox, QWidget, QFileDialog, QProgressBar, QLabel, QGridLayout
from PyQt5.QtCore import pyqtSignal, QObject
from os import path, getenv, chdir, rename
import sys
from threading import Thread
from multiprocessing import cpu_count
from subprocess import call


class Communicate(QObject):
    signal = pyqtSignal()


class ConverterTread(Thread):

    def __init__(self, folder, communicant):
        super().__init__()
        self.communicant = communicant
        self.folder = folder

    def run(self):

        chdir(self.folder)
        old_file = self.folder + "/final.avi"
        if path.exists(self.folder + "/final.avi"):
            rename(old_file, self.folder + "/_old_final.avi")

        call("avconv -threads {} -f image2 -i %04dshot.png -r 60 -s 1024x768 -qscale 1 final.avi"
             .format(cpu_count()).split(" "))

        self.communicant.signal.emit()


class VideoConverterWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.label = QLabel(self)
        self.prog = QProgressBar(self)

        self.folder_path = None

        self.communicant = Communicate()
        self.communicant.signal.connect(self.done)

        self.init()
        self.init_UI()

    def init(self):

        self.get_folder_path()

        if self.folder_path:
            self.generate_video()

    def init_UI(self):

        self.setWindowTitle("AndroidExperiment: VideoConverter")
        self.prog.setValue(0)

        self.label.setText("Converting...")
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

    def get_folder_path(self):

        expected_dir = path.expanduser("~/Desktop/AndroidXP/Capture")
        if path.exists(expected_dir):
            directory = expected_dir
        else:
            directory = getenv("HOME")

        folder_path = QFileDialog.getExistingDirectory(
            self, 'Open file', directory)

        if folder_path:
            self.folder_path = folder_path

        else:
            self.show_error("Selecting a folder is required to proceed.")

    def generate_video(self):

        th = ConverterTread(folder=self.folder_path, communicant=self.communicant)
        th.start()

    def done(self):
        self.prog.setValue(100)
        self.label.setText("Done!")


def main():

    app = QApplication(sys.argv)
    win = VideoConverterWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

