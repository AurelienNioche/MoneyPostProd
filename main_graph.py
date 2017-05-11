from PyQt5.QtWidgets import \
    QApplication, QMainWindow, QVBoxLayout, QSizePolicy, \
    QMessageBox, QWidget, QFileDialog, QProgressBar, QLabel, QGridLayout, \
    QPushButton

import json
import os
import sys

from graph.graph import MarketAttendancePlot, ConsumptionPlot, MediumOfExchangePlot, GaussianReward


class GraphWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.label = QLabel(self)

        self.push_button = QPushButton('Run!')
        self.init_UI()
    
    def init_UI(self):

        self.push_button.clicked.connect(self.run)
        self.setWindowTitle("AndroidExperiment: MainGraph")
        # prog = QProgressBar(self)
        # prog.setValue(100)

        # label.setText("Figures are generated!")
        # self.layout.addWidget(prog)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.push_button)
        self.show()

    def run(self):

        save_path = os.path.expanduser("~/Desktop/AndroidXP")
        file_path = os.path.expanduser("~/Desktop/AndroidXP/data.json")

        data = self.import_data(file_path)
        if data:
            self.generate_fig(save_path, data)

        print("Im here")

    @staticmethod
    def show_error(title="Error", text="ERROR"):

        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        close = msgbox.addButton("Close", QMessageBox.ActionRole)

        msgbox.exec_()

        if msgbox.clickedButton() == close:
            sys.exit()

    def select_folder_path(self):

        folder_path = QFileDialog.getExistingDirectory(
            self, 
            'Select where you want to save your data.', 
            os.getenv("HOME")
        )

        if not folder_path:
            self.show_error(text="You must select a path.")

        else:
            return folder_path

    def select_file_path(self):

        file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getenv("HOME"))[0]

        if not file_path:
            self.show_error(text="Selecting a file is required to proceed")
        else:
            return file_path
              
    def import_data(self, file_path):

        data = None

        try:
            with open(file_path) as f:
                data = json.load(f)

        except Exception as e:
            self.show_error(text="You must select json data: " + str(e))

        finally:
            return data

    def generate_fig(self, save_path, data):
        
        mark_plot = MarketAttendancePlot(save_path, data["market_choice"])
        mark_plot.plot()

        # cons_plot = ConsumptionPlot(
        #     save_path,
        #     success=data["hist_success"],
        #     agent_type=data["p"],
        #     choice=data["market_choice"],
        # )
        # cons_plot.plot()
        #
        # mof_plot = MediumOfExchangePlot(
        #         save_path,
        #         agent_type=data["p"],
        #         choice=data["market_choice"]
        #         )
        #
        # mof_plot.plot()
        #
        # ch_plot = ChoicePlot(save_path, choice=data["market_choice"])
        # ch_plot.plot()
        #
        # gauss_plot = GaussianReward(save_path, reward_amount=data["reward_amount"])
        # gauss_plot.plot()

    @staticmethod
    def main():

        app = QApplication(sys.argv)
        win = GraphWindow()
        sys.exit(app.exec_())
 
if __name__ == '__main__':

    GraphWindow.main()

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
    
