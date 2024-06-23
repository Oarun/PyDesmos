import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import re

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
                eqn = eqn.lower().replace('y=', '').replace('^', '**')
                eqn = re.sub(r'(\d)x', r'\1*x', eqn) 
                 # Add support for trigonometric functions
                eqn = eqn.replace('sin', 'np.sin')
                eqn = eqn.replace('cos', 'np.cos')
                eqn = eqn.replace('tan', 'np.tan')
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
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        input_area = QWidget(self)
        input_layout = QVBoxLayout(input_area)
        main_layout.addWidget(input_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scroll)
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollLayout)
        self.scroll.setWidget(self.scrollContent)
        input_layout.addWidget(self.scroll)

        self.add_eqn_button = QPushButton("Add Equation", self)
        self.add_eqn_button.clicked.connect(self.add_equation_input)
        input_layout.addWidget(self.add_eqn_button)

        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.plot_equations)
        input_layout.addWidget(self.plot_button)

        self.canvas = PlotCanvas(self)
        main_layout.addWidget(self.canvas)

        self.equation_inputs = []
        self.add_equation_input() 

    def add_equation_input(self):
        eqn_input = QLineEdit(self)
        eqn_input.setPlaceholderText("Enter an equation (e.g., y=3x or x^2)")
        self.scrollLayout.addWidget(eqn_input)
        self.equation_inputs.append(eqn_input)

    def plot_equations(self):
        eqns = [input.text().strip() for input in self.equation_inputs if input.text().strip()]
        self.canvas.plot(eqns)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
