import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self, eqns):
        self.ax.clear()
        x = np.linspace(-10, 10, 400)
        for eqn in eqns:
            try:
                y = eval(eqn)
                self.ax.plot(x, y, label=eqn)
            except Exception as e:
                print(f"Error plotting equation '{eqn}': {e}")
        self.ax.legend()
        self.ax.grid(True)
        self.draw()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Desmos")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Enter equations here, one per line.")
        layout.addWidget(self.text_area)

        self.canvas = PlotCanvas(self)
        layout.addWidget(self.canvas)

        plot_button = QPushButton("Plot", self)
        plot_button.clicked.connect(self.plot_equations)
        layout.addWidget(plot_button)

    def plot_equations(self):
        eqns = self.text_area.toPlainText().strip().split("\n")
        self.canvas.plot(eqns)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
