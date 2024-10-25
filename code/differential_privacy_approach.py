import sys

import numpy as np
import pandas as pd
import seaborn as sns
from diffprivlib.mechanisms import Gaussian, Laplace
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
                             QDoubleSpinBox, QFileDialog, QHBoxLayout, QLabel,
                             QMainWindow, QMessageBox, QPushButton,
                             QScrollArea, QTableWidget, QTableWidgetItem,
                             QTabWidget, QTextEdit, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_data = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Differential Privacy Application')
        self.setGeometry(100, 100, 1400, 1000)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Tabs for data and plots
        self.tab_widget = QTabWidget()
        self.data_tab = QWidget()
        self.plot_tab = QWidget()
        self.tab_widget.addTab(self.data_tab, "Data")
        self.tab_widget.addTab(self.plot_tab, "Plots")
        self.layout.addWidget(self.tab_widget)

        # Data tab layout
        self.data_layout = QVBoxLayout(self.data_tab)
        self.table_widget = QTableWidget()
        self.data_layout.addWidget(self.table_widget)

        # Control buttons layout
        self.buttons_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Data')
        self.load_button.clicked.connect(self.load_data)
        self.buttons_layout.addWidget(self.load_button)

        self.revert_button = QPushButton('Revert to Original')
        self.revert_button.clicked.connect(self.revert_to_original)
        self.buttons_layout.addWidget(self.revert_button)

        self.apply_dp_button = QPushButton('Apply Differential Privacy')
        self.apply_dp_button.clicked.connect(self.apply_dp)
        self.buttons_layout.addWidget(self.apply_dp_button)

        self.save_button = QPushButton('Save Data')
        self.save_button.clicked.connect(self.save_data)
        self.buttons_layout.addWidget(self.save_button)

        self.plot_button = QPushButton('Plot Data Comparison')
        self.plot_button.clicked.connect(self.plot_data_comparison)
        self.buttons_layout.addWidget(self.plot_button)

        self.layout.addLayout(self.buttons_layout)

        # Plot tab layout
        self.plot_layout = QVBoxLayout(self.plot_tab)
        self.scroll_area = QScrollArea(self.plot_tab)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.plot_layout.addWidget(self.scroll_area)

        self.dp_controls = []

    def load_data(self):
        try:
            fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV files (*.csv)")
            if fname:
                self.data = pd.read_csv(fname)
                self.original_data = self.data.copy()  # Store original data
                self.display_data(self.data)
                self.prepare_dp_controls()
                QMessageBox.information(self, 'Info', 'Data loaded successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Failed to load data: ' + str(e))

    def revert_to_original(self):
        try:
            if self.original_data is not None:
                self.data = self.original_data.copy()
                self.display_data(self.data)
                QMessageBox.information(self, 'Info', 'Dataset reverted to original state.')
            else:
                QMessageBox.warning(self, 'Error', 'No data to revert to. Load data first.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Failed to revert data: ' + str(e))

    def display_data(self, data):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data.columns))
        self.table_widget.setHorizontalHeaderLabels(data.columns)
        for row_index, row in data.iterrows():
            for col_index, value in enumerate(row):
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def prepare_dp_controls(self):
        try:
            # Add labels for clarity
            label_layout = QHBoxLayout()
            label_layout.addWidget(QLabel('Column'))
            label_layout.addWidget(QLabel('Mechanism'))
            label_layout.addWidget(QLabel('Epsilon'))
            label_layout.addWidget(QLabel('Sensitivity'))
            self.layout.addLayout(label_layout)

            for widget in self.dp_controls:
                widget.deleteLater()
            self.dp_controls.clear()

            for i, column in enumerate(self.data.columns):
                hbox = QHBoxLayout()
                checkbox = QCheckBox(f"{column}")
                hbox.addWidget(checkbox)

                combo_box = QComboBox()
                combo_box.addItems(["Laplace", "Gaussian"])
                hbox.addWidget(combo_box)

                epsilon_spinbox = QDoubleSpinBox()
                epsilon_spinbox.setRange(0.01, 10.0)
                epsilon_spinbox.setSingleStep(0.1)
                epsilon_spinbox.setValue(0.5)
                hbox.addWidget(epsilon_spinbox)

                sensitivity_spinbox = QDoubleSpinBox()
                sensitivity_spinbox.setRange(0.1, 10.0)
                sensitivity_spinbox.setSingleStep(0.1)
                sensitivity_spinbox.setValue(1.0)
                hbox.addWidget(sensitivity_spinbox)

                self.layout.addLayout(hbox)
                self.dp_controls.append((checkbox, combo_box, epsilon_spinbox, sensitivity_spinbox))
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Failed to prepare differential privacy controls: ' + str(e))

    def apply_dp(self):
        try:
            self.anonymized_data = self.data.copy()
            for i, controls in enumerate(self.dp_controls):
                if controls[0].isChecked():
                    epsilon = controls[2].value()
                    sensitivity = controls[3].value()
                    mechanism_type = controls[1].currentText()
                    column = self.data.columns[i]

                    if mechanism_type == "Laplace":
                        mechanism = Laplace(epsilon=epsilon, sensitivity=sensitivity)
                    elif mechanism_type == "Gaussian":
                        mechanism = Gaussian(epsilon=epsilon, sensitivity=sensitivity, delta=1e-5)

                    self.anonymized_data[column] = [mechanism.randomise(val) for val in self.data[column]]

            self.display_data(self.anonymized_data)
            QMessageBox.information(self, 'Info', 'Differential privacy applied successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Failed to apply differential privacy: ' + str(e))

    def save_data(self):
        try:
            fname, _ = QFileDialog.getSaveFileName(self, 'Save file', '', "CSV files (*.csv)")
            if fname:
                self.anonymized_data.to_csv(fname, index=False)
                QMessageBox.information(self, 'Info', 'Data saved successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Failed to save data: ' + str(e))

    def plot_data_comparison(self):
        try:
            if not hasattr(self, 'anonymized_data'):
                QMessageBox.warning(self, 'Error', 'Apply differential privacy before plotting.')
                return

            # Clear existing plots to avoid overlay of graphs on re-plotting
            for i in reversed(range(self.scroll_layout.count())): 
                widgetToRemove = self.scroll_layout.itemAt(i).widget()
                if widgetToRemove is not None:
                    widgetToRemove.setParent(None)
                    widgetToRemove.deleteLater()

            # Plot new data comparisons
            for i, column in enumerate(self.data.columns):
                controls = self.dp_controls[i]
                checkbox = controls[0]
                if checkbox.isChecked():
                    fig = Figure(figsize=(10, 8))
                    canvas = FigureCanvas(fig)
                    axs = fig.subplots(2, 2)

                    # Histogram with title including column name
                    axs[0, 0].hist(self.data[column], bins=20, alpha=0.5, label='Original')
                    axs[0, 0].hist(self.anonymized_data[column], bins=20, alpha=0.5, label='Anonymized')
                    axs[0, 0].set_title(f'Histogram of {column}')
                    axs[0, 0].legend()

                    # Box Plot with title including column name
                    axs[0, 1].boxplot([self.data[column], self.anonymized_data[column]], labels=['Original', 'Anonymized'])
                    axs[0, 1].set_title(f'Box Plot of {column}')

                    # Density Plot with title including column name
                    sns.kdeplot(self.data[column], ax=axs[1, 0], fill=True, label='Original', alpha=0.5)
                    sns.kdeplot(self.anonymized_data[column], ax=axs[1, 0], fill=True, label='Anonymized', alpha=0.5)
                    axs[1, 0].set_title(f'Density Plot of {column}')
                    axs[1, 0].legend()

                    # Line Plot with title including column name
                    axs[1, 1].plot(self.data[column], label='Original')
                    axs[1, 1].plot(self.anonymized_data[column], label='Anonymized')
                    axs[1, 1].set_title(f'Line Plot of {column}')
                    axs[1, 1].legend()

                    self.scroll_layout.addWidget(canvas)

                    # Add metrics text area
                    metrics_text = QTextEdit()
                    metrics_text.setPlainText(
                        f"Original Mean: {np.mean(self.data[column]):.2f}, Anonymized Mean: {np.mean(self.anonymized_data[column]):.2f}\n"
                        f"Original Std Dev: {np.std(self.data[column]):.2f}, Anonymized Std Dev: {np.std(self.anonymized_data[column]):.2f}"
                    )
                    metrics_text.setReadOnly(True)
                    self.scroll_layout.addWidget(metrics_text)
        except Exception as e:
            QMessageBox.critical(self, 'Error', 'Failed to generate plots: ' + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
