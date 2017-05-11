from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QFileDialog
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from pylab import plt, np
from scipy.stats import norm
matplotlib.use("Qt5Agg")
import random
import json
import os
import sys


class MarketAttendancePlot(object):
    legend_font_size = 12
    label_font_size = 12

    def __init__(self, save_path, choice):

        self.X, self.Ys = self.format_data(choice)
        self.fig_name = save_path + "/market_attendance.pdf"

    @staticmethod
    def format_data(choice):

        t_max = len(choice)

        x = np.arange(t_max)

        y0 = []
        y1 = []
        y2 = []
        for t in range(t_max):
            y0.append(choice[t].count([0, 1]) + choice[t].count([1, 0]))
            y1.append(choice[t].count([1, 2]) + choice[t].count([2, 1]))
            y2.append(choice[t].count([2, 0]) + choice[t].count([0, 2]))

        ys = y0, y1, y2

        return x, ys

    def plot(self):

        self.fig = plt.figure(figsize=(25, 12))
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0)

        self.ax = plt.gca()
        self.ax.set_title("Markets attendance \n")

        labels = [
            "Market 0 -> 1 / 1 -> 0",
            "Market 1 -> 2 / 2 -> 1",
            "Market 2 -> 0 / 0 -> 2",
        ]
        line_styles = [
            "-",
            "--",
            ":"
        ]

        for i, y in enumerate(self.Ys):
            self.ax.plot(self.X, y, label=labels[i], linewidth=2, color="black", linestyle=line_styles[i])

        self.ax.legend(bbox_to_anchor=(0.15, 0.1), fontsize=self.legend_font_size, frameon=False)

        self.ax.set_xlabel("t", fontsize=self.label_font_size)
        self.ax.set_ylabel("n", fontsize=self.label_font_size)

        self.ax.spines['right'].set_color('none')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)


class ChoicePlot(object):
    legend_font_size = 12
    label_font_size = 12

    def __init__(self, save_path, choice):

        self.X, self.Ys = self.format_data(choice)
        self.fig_name = save_path + "/choice.pdf"

    @staticmethod
    def format_data(choice):

        t_max = len(choice)

        x = np.arange(t_max)

        y0, y1, y2, y3, y4, y5 = [], [], [], [], [], []

        for t in range(t_max):
            y0.append(choice[t].count([0, 1]))
            y1.append(choice[t].count([1, 0]))
            y2.append(choice[t].count([1, 2]))
            y3.append(choice[t].count([2, 1]))
            y4.append(choice[t].count([2, 0]))
            y5.append(choice[t].count([0, 2]))

        ys = y0, y1, y2, y3, y4, y5

        return x, ys

    def plot(self):

        self.fig = plt.figure(figsize=(25, 12))
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0)

        self.ax = plt.gca()
        self.ax.set_title("Choices \n")

        labels = [
            "Choice 0 -> 1",
            "Choice 1 -> 0",
            "Choice 1 -> 2",
            "Choice 2 -> 1",
            "Choice 2 -> 0",
            "Choice 0 -> 2",
        ]
        line_styles = [
            "-",
            "-",
            "-",
            "-",
            "-",
            "-"
        ]
        markers = [
            4,
            5,
            4,
            5,
            4,
            5
        ]

        colors = [
            "red",
            "red",
            "blue",
            "blue",
            "green",
            "green"
        ]

        for i, y in enumerate(self.Ys):
            self.ax.plot(self.X, y, label=labels[i], linewidth=2, color=colors[i], linestyle=line_styles[i], marker=markers[i])

        self.ax.legend(bbox_to_anchor=(0.9, 0.9), fontsize=self.legend_font_size, frameon=False)

        self.ax.set_xlabel("t", fontsize=self.label_font_size)
        self.ax.set_ylabel("n", fontsize=self.label_font_size)

        self.ax.spines['right'].set_color('none')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)


class ConsumptionPlot(object):
    legend_font_size = 12
    label_font_size = 12

    def __init__(self, save_path, choice, success, agent_type ):

        self.X, self.Y = self.format_data(choice=choice, success=success, agent_type=agent_type)
        self.fig_name = save_path + "/consumption.pdf"

    @staticmethod
    def format_data(choice, success, agent_type):

        t_max = len(choice)

        x = np.arange(t_max)

        y = []

        for t in range(t_max):
            consumption = 0
            for c, s, at, in zip(choice[t], success[t], agent_type):
                if c[1] == (at + 1) % 3 and s:
                    consumption += 1

            y.append(consumption)

        return x, y

    def plot(self):

        self.fig = plt.figure(figsize=(25, 12))
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0)

        self.ax = plt.gca()
        self.ax.set_title("Consumption\n")

        self.ax.plot(self.X, self.Y, linewidth=2, color="black")

        self.ax.set_xlabel("t", fontsize=self.label_font_size)
        self.ax.set_ylabel("n", fontsize=self.label_font_size)

        self.ax.spines['right'].set_color('none')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)


class MediumOfExchangePlot(object):


    legend_font_size = 12
    label_font_size = 12

    def __init__(self, save_path, choice, agent_type):
        
        self.fig_name = save_path + "/medium_of_exchange.pdf"
        self.X, self.Ys = self.format_data(choice, agent_type)

    @staticmethod
    def format_data(choice, agent_type):

        t_max = len(choice)

        x = np.arange(t_max)

        ys = [], [], []

        for t in range(t_max):

            # Will register the number of times each good has been used as a medium of exchange
            y = [0, 0, 0]

            for i, ch, at in zip(range(len(agent_type)), choice[t], agent_type):

                p = at
                c = (at + 1) % 3
                m = (at + 2) % 3
                if (ch[0] == p and ch[1] == m) or (ch[0] == m and ch[1] == c):
                    y[m] += 1

            for i in range(3):
                ys[i].append(y[i])

        return x, ys

    def plot(self):

        self.fig = plt.figure(figsize=(25, 12))
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0)

        self.ax = plt.gca()
        self.ax.set_title("Medium of exchange \n")

        labels = [
            "Good 0",
            "Good 1",
            "Good 2",
        ]
        line_styles = [
            ":",
            "--",
            "-"
        ]

        for i, y in enumerate(self.Ys):
            self.ax.plot(self.X, y, label=labels[i], linewidth=2, color="black", linestyle=line_styles[i])

        self.ax.legend(bbox_to_anchor=(0.15, 0.1), fontsize=self.legend_font_size, frameon=False)

        self.ax.set_xlabel("t", fontsize=self.label_font_size)
        self.ax.set_ylabel("n", fontsize=self.label_font_size)

        self.ax.spines['right'].set_color('none')
        self.ax.yaxis.set_ticks_position('left')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['top'].set_color('none')

        plt.savefig(self.fig_name)


class GaussianReward(object):
    legend_font_size = 12
    label_font_size = 12

    def __init__(self, save_path, reward_amount):

        self.X, self.Y = self.format_data(reward_amount)
        self.fig_name = save_path + "/gaussian_reward.pdf"

    @staticmethod
    def format_data(reward_amount):

        y = reward_amount

        x = np.arange(len(y))

        return x, y

    def plot(self):

        self.fig = plt.figure(figsize=(25, 12))
        self.fig.patch.set_facecolor('white')
        self.fig.patch.set_alpha(0)

        self.ax = plt.gca()
        self.ax.set_title("Gaussian rewards \n")
        
        sd = np.std(self.Y)
        mn = np.mean(self.Y)

        self.ax.plot(self.X, norm.pdf(self.Y, mn, sd))

        plt.savefig(self.fig_name)

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, figure, parent=None, width=5, height=4, dpi=100):

        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class GraphWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AndroidExperiment : MainGraph")

        self.layout = QVBoxLayout(self)
        
        self.get_save_path()
        self.import_data()
        self.generate_fig()
        self.import_fig()

        # self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.show()
    
    def get_save_path(self):

        self.save_path = QFileDialog.getExistingDirectory(
            self, 
            'Select where you want to save your data.', 
            os.getenv("HOME")
            )

        if not self.save_path:

            msgbox = QMessageBox()
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setWindowTitle("Error")
            msgbox.setText("Selecting a file is required to proceed")
            close = msgbox.addButton("Close", QMessageBox.ActionRole)

            msgbox.exec_()

            if msgbox.clickedButton() == close:
                sys.exit()
  

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
            with open(file_path, "rb") as f:
                self.data = json.load(f)

    def import_fig(self):
        
        for figure in self.figure_list:
            fig = MyMplCanvas(figure,
                    self.main_widget,
                    width=5,
                    height=4,
                    dpi=100
                    )
            self.layout.addWidget(fig)
        
    def generate_fig(self):
        
        mark_plot = MarketAttendancePlot(self.save_path, self.data["market_choice"])
        mark_plot.plot()

        cons_plot = ConsumptionPlot(
            self.save_path,
            success=self.data["hist_success"],
            agent_type=self.data["p"],
            choice=self.data["market_choice"],
        )
        cons_plot.plot()

        mof_plot = MediumOfExchangePlot(
                self.save_path,
                agent_type=self.data["p"], 
                choice=self.data["market_choice"]
                )
        
        mof_plot.plot()

        ch_plot = ChoicePlot(self.save_path, choice=self.data["market_choice"])
        ch_plot.plot()

        gauss_plot = GaussianReward(self.save_path, self.data["reward_amount"])
        gauss_plot.plot()

        self.figure_list = [mark_plot.fig, mof_plot.fig, ch_plot.fig, gauss_plot.fig]

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
    
    @staticmethod
    def main():
        app = QApplication(sys.argv)
        win = GraphWindow()
        sys.exit(app.exec_())
 
# class MyMplCanvas(FigureCanvas):
    # """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    # def __init__(self, figure, parent=None, width=5, height=4, dpi=100):

        # FigureCanvas.__init__(self, figure)
        # self.setParent(parent)

        # FigureCanvas.setSizePolicy(self,
                # QSizePolicy.Expanding,
                # QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)


# class GraphWindow(QMainWindow):
    # """Main window containing canvas (figures)"""

    # def __init__(self):

        # QMainWindow.__init__(self)
        # self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.setWindowTitle("AndroidExperiment : MainGraph")

        # self.file_menu = QMenu('&File', self)
        # self.file_menu.addAction('&Quit', self.fileQuit,
                # QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        # self.menuBar().addMenu(self.file_menu)

        # self.help_menu = QMenu('&Help', self)
        # self.menuBar().addSeparator()
        # self.menuBar().addMenu(self.help_menu)

        # self.main_widget = QWidget(self)
        
        # self.layout = QVBoxLayout(self.main_widget)
        # self.layout.setSpacing(30)
        
        # self.get_save_path()
        # self.import_data()
        # self.generate_fig()
        # self.import_fig()

        # # self.main_widget.setFocus()
        # self.setCentralWidget(self.main_widget)
        # self.show()
    
    # def get_save_path(self):

        # self.save_path = QFileDialog.getExistingDirectory(
            # self, 
            # 'Select where you want to save your data.', 
            # os.getenv("HOME")
            # )

        # if not self.save_path:

            # msgbox = QMessageBox()
            # msgbox.setIcon(QMessageBox.Critical)
            # msgbox.setWindowTitle("Error")
            # msgbox.setText("Selecting a file is required to proceed")
            # close = msgbox.addButton("Close", QMessageBox.ActionRole)

            # msgbox.exec_()

            # if msgbox.clickedButton() == close:
                # sys.exit()
  

    # def import_data(self):
        
        # file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getenv("HOME"))[0]

        # if not file_path:

            # msgbox = QMessageBox()
            # msgbox.setIcon(QMessageBox.Critical)
            # msgbox.setWindowTitle("Error")
            # msgbox.setText("Selecting a file is required to proceed")
            # close = msgbox.addButton("Close", QMessageBox.ActionRole)

            # msgbox.exec_()
        
            # if msgbox.clickedButton() == close:
                # sys.exit()
        # else:
            # with open(file_path, "rb") as f:
                # self.data = json.load(f)

    # def import_fig(self):
        
        # for figure in self.figure_list:
            # fig = MyMplCanvas(figure,
                    # self.main_widget,
                    # width=5,
                    # height=4,
                    # dpi=100
                    # )
            # self.layout.addWidget(fig)
        
    # def generate_fig(self):
        
        # mark_plot = MarketAttendancePlot(self.save_path, self.data["market_choice"])
        # mark_plot.plot()

        # cons_plot = ConsumptionPlot(
            # self.save_path,
            # success=self.data["hist_success"],
            # agent_type=self.data["p"],
            # choice=self.data["market_choice"],
        # )
        # cons_plot.plot()

        # mof_plot = MediumOfExchangePlot(
                # self.save_path,
                # agent_type=self.data["p"], 
                # choice=self.data["market_choice"]
                # )
        
        # mof_plot.plot()

        # ch_plot = ChoicePlot(self.save_path, choice=self.data["market_choice"])
        # ch_plot.plot()

        # gauss_plot = GaussianReward(self.save_path, self.data["reward_amount"])
        # gauss_plot.plot()

        # self.figure_list = [mark_plot.fig, mof_plot.fig, ch_plot.fig, gauss_plot.fig]

    # def fileQuit(self):
        # self.close()

    # def closeEvent(self, ce):
        # self.fileQuit()
    
    # @staticmethod
    # def main():
        # app = QApplication(sys.argv)
        # win = GraphWindow()
        # sys.exit(app.exec_())
    
