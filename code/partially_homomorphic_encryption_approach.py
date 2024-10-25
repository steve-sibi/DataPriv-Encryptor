import sys
import threading

import pandas as pd
import tenseal as ts
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)


class HomomorphicEncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Partially Homomorphic Encryption with TenSEAL")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        load_button = QPushButton('Load Data')
        load_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(load_button)

        encrypt_button = QPushButton('Encrypt Data')
        encrypt_button.clicked.connect(self.async_encrypt_data)
        layout.addWidget(encrypt_button)

        modify_button = QPushButton('Modify Encrypted Data')
        modify_button.clicked.connect(self.modify_encrypted_data)
        layout.addWidget(modify_button)

        decrypt_button = QPushButton('Decrypt Data')
        decrypt_button.clicked.connect(self.decrypt_data)
        layout.addWidget(decrypt_button)

        self.setup_context()

    def setup_context(self):
        self.context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=4096,
            coeff_mod_bit_sizes=[30, 30, 30]
        )
        self.context.global_scale = 2**30
        self.context.generate_galois_keys()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.load_data(fileName)

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        self.display_data(self.data)

    def display_data(self, data):
        self.table.setRowCount(data.shape[0])
        self.table.setColumnCount(data.shape[1])
        self.table.setHorizontalHeaderLabels(data.columns)

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))

    def async_encrypt_data(self):
        threading.Thread(target=self.encrypt_data).start()

    def encrypt_data(self):
        temperatures = self.data['Temperature'].tolist()
        self.encrypted_vector = ts.ckks_vector(self.context, temperatures)
        self.data['Temperature'] = ['Encrypted value' for _ in temperatures]  # Placeholder text for encrypted data
        self.display_data(self.data)
        self.show_status("Data encrypted!")

    def modify_encrypted_data(self):
        if self.encrypted_vector:
            self.encrypted_vector += 5  # Adding 5 to the encrypted vector
            self.data['Temperature'] = ['Modified encrypted value' for _ in self.data['Temperature']]  # Placeholder text for modified data
            self.display_data(self.data)
            self.show_status("Encrypted data modified!")
        else:
            self.show_status("Encrypt data first!")

    def decrypt_data(self):
        if self.encrypted_vector:
            decrypted_temperatures = self.encrypted_vector.decrypt()
            self.data['Temperature'] = decrypted_temperatures
            self.display_data(self.data)
            self.show_status("Data decrypted!")
        else:
            self.show_status("Encrypt and modify data first!")

    def show_status(self, message):
        print(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = HomomorphicEncryptionApp()
    mainWin.show()
    sys.exit(app.exec_())
