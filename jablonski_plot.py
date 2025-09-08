import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFileDialog,QLineEdit,
    QMessageBox, QFormLayout, QHBoxLayout, QMainWindow, QAction, QMenu, QComboBox,
    QActionGroup, QDialog, QLabel, QGroupBox, QPushButton, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont , QKeyEvent
from PyQt5.QtCore import Qt , QTimer, QPoint
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Jablonski plotter')
        self.setGeometry(100, 100, 800, 600)

        """Set central widget and main layout"""
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.plot_graph = pg.PlotWidget(background='w')
        main_layout.addWidget(self.plot_graph)

        """Right layout (add box menu)"""
        right_layout = QVBoxLayout()

        add_states_group = QGroupBox("Add New State")
        add_states_layout = QVBoxLayout()

        self.input_container = QWidget()
        self.input_layout = QVBoxLayout()
        self.states_layout = QVBoxLayout()
        input_container_layout = QVBoxLayout()
        input_container_layout.addLayout(self.input_layout)
        input_container_layout.addSpacing(10)
        input_container_layout.addLayout(self.states_layout)

        self.input_container.setLayout(input_container_layout)
        self.input_container.setVisible(False)
        add_states_layout.addWidget(self.input_container)
        
        spacer = QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding)
        add_states_layout.addItem(spacer)

        add_states_group.setLayout(add_states_layout)

        spacer = QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding)
        add_states_layout.addItem(spacer)

        right_layout.addWidget(add_states_group)

        add_process_group = QGroupBox("Add New Process")
        add_process_layout = QVBoxLayout()

        spacer = QSpacerItem(2, 4, QSizePolicy.Minimum, QSizePolicy.Expanding)
        add_process_layout.addItem(spacer)

        right_layout.addWidget(add_process_group)

        main_layout.addLayout(right_layout)

        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 2)

        self.setStyleSheet("""
            QMenuBar { font-family: Arial; font-size: 15pt; }
            QMenu { font-family: Arial; font-size: 13pt; }
            QAction { font-family: Arial; font-size: 13pt; }
            QGroupBox { font-family: Arial; font-size: 16pt; }
            QLabel { font-family: Arial; font-size: 14pt; }
            QPushButton { font-family: Arial; font-size: 14pt; }
            QDialog { font-family: Arial; font-size: 14pt; }
            QLineEdit { font-family: Arial; font-size: 14pt; }
            QComboBox { font-family: Arial; font-size: 14pt; }
            QTextEdit { font-family: Arial; font-size: 14pt; }
            QProgressBar { font-family: Arial; font-size: 14pt; }
            QSlider { font-family: Arial; font-size: 14pt; }
            QSpinBox { font-family: Arial; font-size: 14pt; }
            QDoubleSpinBox { font-family: Arial; font-size: 14pt; }
            QCheckBox { font-family: Arial; font-size: 14pt; }
            QRadioButton { font-family: Arial; font-size: 14pt; }
            QGroupBox::title { subcontrol-position: top left; }
            QTabBar::tab { font-family: Arial; font-size: 14pt; }
         """)

        self.timer = QTimer(self)
        self.timer.start(16)
        self.add_state_function()
        self.showMaximized()

    def create_menu(self, layout):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        upload_action = QAction("Clear All", self)
        upload_action.triggered.connect(self.upload_file)
        file_menu.addAction(upload_action)

        download_menu = QMenu("Export image", self)
        file_menu.addMenu(download_menu)


    # --- Placeholder methods ---
    def upload_file(self): print("Upload File clicked")

    def add_state_function(self):
        for i in reversed(range(self.input_layout.count())):
            widget = self.input_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.input_fields={}

        """State Name"""
        new_state_row = QHBoxLayout()
        name_label = QLabel(f"State Name")
        name_edit = QLineEdit()
        name_edit.setText(f"Name")
        new_state_row.addWidget(name_label)
        new_state_row.addWidget(name_edit)
        name_container = QWidget()
        name_container.setLayout(new_state_row)
        self.input_layout.addWidget(name_container)
        self.input_fields["Name"] = name_edit

        """Energy"""
        energy_label = QLabel("Energy (eV)")
        energy_edit = QLineEdit()
        energy_edit.setText(f"Energy")
        new_state_row.addWidget(energy_label)
        new_state_row.addWidget(energy_edit)
        energy_container = QWidget()
        energy_container.setLayout(new_state_row)
        self.input_layout.addWidget(energy_container)
        self.input_fields["Energy"] = energy_edit

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_inputs)
        self.input_layout.addWidget(save_btn)

        self.input_container.setVisible(True)

    def save_inputs(self):
        """Save input data and create the box"""
        state_values = {
            key: field.text() for key, field in self.input_fields.items()
        }
        row = QVBoxLayout()
        container = QWidget()

        name_label = QLabel(f"<b>{state_values}</b>")
        name_label.setAlignment(Qt.AlignCenter)
        state_row = QHBoxLayout()
        remove_btn = QPushButton("Remove")
        remove_btn.setFixedWidth(remove_btn.sizeHint().width() + 20)
        remove_btn.setStyleSheet("font-size: 15px;")
        state_row.addWidget(name_label)
        state_row.addWidget(remove_btn)

        row.addWidget(name_label)
        row.addLayout(state_row)

        container.setLayout(row)
        insert_index = self.states_layout.count() - 2
        self.states_layout.insertWidget(insert_index, container)

        def remove_row():
            self.states_layout.removeWidget(container)
            container.deleteLater()

        remove_btn.clicked.connect(remove_row)
        self.add_remove_all_button()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
