import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QLineEdit, QRadioButton, QButtonGroup, \
    QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

from sound import play, record


def play_music(self):
    play(self.file_path)


def record_sound(self):
    record(self.frequency, self.bit_depth,15)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analogue-Digital Operator")

        self.frequency = 40000
        self.bit_depth = 16
        self.file_path = ""

        # Górna część okna
        upper_widget = QWidget()
        upper_layout = QVBoxLayout()

        # Suwak i pole tekstowe do ustawienia częstotliwości
        freq_layout = QHBoxLayout()
        self.freq_label = QLabel('Frequency:')
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setMinimum(20000)
        self.freq_slider.setMaximum(60000)
        self.freq_slider.setValue(self.frequency)
        self.freq_slider.valueChanged.connect(self.update_freq_text)
        self.freq_text = QLineEdit(str(self.freq_slider.value()))
        self.freq_text.setFixedWidth(100)
        self.freq_text.editingFinished.connect(self.update_freq_slider)

        freq_layout.addWidget(self.freq_label)
        freq_layout.addWidget(self.freq_slider)
        freq_layout.addWidget(self.freq_text)

        upper_layout.addLayout(freq_layout)

        # Wybór opcji dla kwantyzacji
        self.bit_8 = QRadioButton('8-bit')
        self.bit_16 = QRadioButton('16-bit')
        self.bit_16.setChecked(True)

        bit_layout = QHBoxLayout()
        bit_layout.addWidget(self.bit_8)
        bit_layout.addWidget(self.bit_16)

        self.bit_group = QButtonGroup()
        self.bit_group.addButton(self.bit_8)
        self.bit_group.addButton(self.bit_16)

        upper_layout.addLayout(bit_layout)

        # Przycisk otwierający eksplorator plików
        self.choose_file_button = QPushButton('Choose File')
        self.choose_file_button.clicked.connect(self.open_file_dialog)

        self.file_display = QLineEdit()
        self.file_display.setReadOnly(True)

        upper_layout.addWidget(self.file_display)
        upper_layout.addWidget(self.choose_file_button)

        upper_widget.setLayout(upper_layout)

        # ------------------------------------------

        lower_widget = QWidget()
        lower_layout = QHBoxLayout()

        self.record_button = QPushButton('Record')
        self.record_button.clicked.connect(lambda: record_sound(self))

        self.play_button = QPushButton('Play')
        self.record_button.clicked.connect(lambda: play_music(self))

        lower_layout.addWidget(self.record_button)
        lower_layout.addWidget(self.play_button)

        lower_widget.setLayout(lower_layout)

        # --------------------------------------------

        main_layout = QVBoxLayout()
        main_layout.addWidget(upper_widget)
        main_layout.addWidget(lower_widget)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def update_freq_text(self):
        self.frequency = self.freq_slider.value()
        self.freq_text.setText(str(self.freq_slider.value()))

    def update_freq_slider(self):
        self.freq_slider.setValue(int(self.freq_text.text()))

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.file_display.setText(file_path)
            print(f"File chosen: {file_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
