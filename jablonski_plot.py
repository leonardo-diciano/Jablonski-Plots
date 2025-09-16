import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QVBoxLayout, QFileDialog,QLineEdit,
    QMessageBox, QFormLayout, QHBoxLayout, QMainWindow, QAction, QMenu, QComboBox,
    QActionGroup, QDialog, QLabel, QGroupBox, QPushButton, QSpacerItem, QSizePolicy, QScrollArea)
from PyQt5.QtGui import QFont , QKeyEvent
from PyQt5.QtCore import Qt , QTimer, QPoint
import pyqtgraph as pg


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Jablonski plotter')
		self.setGeometry(100, 100, 800, 600)
	
		""" Initial conditions """
		self.states_dict={}
		self.states_list=[]
		self.proc_list=[]
		
		
		"""Set central widget and main layout"""
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		self.setCentralWidget(central_widget)
		self.create_menu(main_layout)

		self.plot_graph = pg.PlotWidget(background='w')
		main_layout.addWidget(self.plot_graph)
		
		"""Right layout"""
		right_layout = QVBoxLayout()
		
		add_states_group = QGroupBox("Add New State")
		add_states_layout = QVBoxLayout()
		
		self.input_container = QWidget()
		self.input_layout = QVBoxLayout()
		self.states_layout = QGridLayout()
		input_container_layout = QVBoxLayout()
		input_container_layout.addLayout(self.input_layout)
		input_container_layout.addSpacing(10)
		input_container_layout.addLayout(self.states_layout)
		
		self.input_container.setLayout(input_container_layout)
		self.input_container.setVisible(False)
		add_states_layout.addWidget(self.input_container)
		
		
		add_states_group.setLayout(add_states_layout)
		
		
		right_layout.addWidget(add_states_group)
		
		add_process_group = QGroupBox("Add New Process")
		add_process_layout = QVBoxLayout()
		
		self.proc_input_container = QWidget()
		self.proc_input_layout = QVBoxLayout()
		self.process_layout = QGridLayout()
		proc_input_container_layout = QVBoxLayout()
		proc_input_container_layout.addLayout(self.proc_input_layout)
		proc_input_container_layout.addSpacing(10)

		proc_input_container_layout.addLayout(self.process_layout)		
		self.proc_input_container.setLayout(proc_input_container_layout)
		self.proc_input_container.setVisible(False)
		add_process_layout.addWidget(self.proc_input_container)

		add_process_group.setLayout(add_process_layout)

		
		spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
		add_process_layout.addItem(spacer)
		
		right_layout.addWidget(add_process_group)
		main_layout.addLayout(right_layout)

		scroll_lists_layout = QVBoxLayout()

		scroll_group1 = QGroupBox("State Energies List")
		scroll_group1_layout = QVBoxLayout()
		self.states_scroll_content = QWidget()
		self.states_scroll_layout = QVBoxLayout(self.states_scroll_content)
		self.states_scroll_layout.addStretch()

		states_scroll_area = QScrollArea()
		states_scroll_area.setWidgetResizable(True)
		states_scroll_area.setWidget(self.states_scroll_content)
		scroll_group1_layout.addWidget(states_scroll_area)
		scroll_group1.setLayout(scroll_group1_layout)

		scroll_group2 = QGroupBox("Process List")
		scroll_group2_layout = QVBoxLayout()
		self.proc_scroll_content = QWidget()
		self.proc_scroll_layout = QVBoxLayout(self.proc_scroll_content)
		self.proc_scroll_layout.addStretch()

		proc_scroll_area = QScrollArea()
		proc_scroll_area.setWidgetResizable(True)
		proc_scroll_area.setWidget(self.proc_scroll_content)
		scroll_group2_layout.addWidget(proc_scroll_area)
		scroll_group2.setLayout(scroll_group2_layout)
		
		scroll_lists_layout.addWidget(scroll_group1)
		scroll_lists_layout.addWidget(scroll_group2)

		main_layout.addLayout(scroll_lists_layout) 
		
		main_layout.setStretch(0, 2)
		main_layout.setStretch(1, 1)
		main_layout.setStretch(2, 1)
		
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
		
		self.add_state_function()
		self.add_process_function()
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
		save_btn.clicked.connect(self.save_input_states)
		self.input_layout.addWidget(save_btn)
		
		self.input_container.setVisible(True)
	
	def save_input_states(self):
		"""Save input data and create the row for states"""
		input_values = {
		    key: field.text() for key, field in self.input_fields.items()
		}
		container = QWidget()
		state_row = QHBoxLayout(container)
		
		self.states_dict.update({input_values["Name"]:input_values["Energy"]})	
		self.states_list.append(input_values["Name"])
		name_label = QLabel(f"<b>{input_values['Name']}: {input_values['Energy']} eV</b>")
		name_label.setAlignment(Qt.AlignCenter)
		remove_btn = QPushButton("Remove")
		remove_btn.setFixedWidth(remove_btn.sizeHint().width() + 20)
		remove_btn.setStyleSheet("font-size: 15px;")
		state_row.addWidget(name_label)
		state_row.addWidget(remove_btn)
	
		self.states_scroll_layout.insertWidget(self.states_scroll_layout.count() - 1,container)
		self.add_process_function()
				
		def remove_row():
			self.states_scroll_layout.removeWidget(container)
			container.deleteLater()
			self.states_dict.pop(input_values['Name'])
			self.states_list.remove(input_values['Name'])
			print(self.states_dict)
			self.add_process_function()

		remove_btn.clicked.connect(remove_row)


	def add_process_function(self):
		for i in reversed(range(self.proc_input_layout.count())):
			widget = self.proc_input_layout.itemAt(i).widget()
			if widget is not None:
				widget.setParent(None)	
		self.proc_input_fields={}
	
		"""Process Name"""
		new_process_row = QVBoxLayout()
		name_label = QLabel(f"Name")
		name_edit = QComboBox()
		name_edit.addItems(['ABS','FLU','PHO','ISC','RISC','IC'])
		new_process_row.addWidget(name_label)
		new_process_row.addWidget(name_edit)
		name_container = QWidget()
		name_container.setLayout(new_process_row)
		self.proc_input_layout.addWidget(name_container)
		self.proc_input_fields["Name"] = name_edit
		
		"""States involved"""
		state1_label = QLabel("State1")
		state1_edit = QComboBox()
		state1_edit.addItems(self.states_list)
		new_process_row.addWidget(state1_label)
		new_process_row.addWidget(state1_edit)
		state1_container = QWidget()
		state1_container.setLayout(new_process_row)
		self.proc_input_layout.addWidget(state1_container)
		self.proc_input_fields["State1"] = state1_edit

		state2_label = QLabel("State2")
		state2_edit = QComboBox()
		state2_edit.addItems(self.states_list)
		new_process_row.addWidget(state2_label)
		new_process_row.addWidget(state2_edit)
		state2_container = QWidget()
		state2_container.setLayout(new_process_row)
		self.proc_input_layout.addWidget(state2_container)
		self.proc_input_fields["State2"] = state2_edit
		
		"""Rate constant"""
		
		rate_label = QLabel("Rate constant (s<sup>-1</sup>)")
		rate_edit = QLineEdit()
		rate_edit.setText(f"Constant")
		new_process_row.addWidget(rate_label)
		new_process_row.addWidget(rate_edit)
		process_container = QWidget()
		process_container.setLayout(new_process_row)
		self.proc_input_layout.addWidget(process_container)
		self.proc_input_fields["Constant"] = rate_edit

		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_input_process)
		self.proc_input_layout.addWidget(save_btn)
		
		self.proc_input_container.setVisible(True)
	
	def save_input_process(self):
		"""Save input data and create the row for process"""
		proc_input_values = {
		    key: field.currentText() if isinstance(field,QComboBox) else field.text()
			for key, field in self.proc_input_fields.items()
		}
		container = QWidget()
		proc_row = QHBoxLayout(container)
		
		self.proc_list.append((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))	
		name_label = QLabel(f"k<sup>{proc_input_values['Name']}</sup>"
				f"<sub>{proc_input_values['State1']}→{proc_input_values['State2']}</sub>"
    				f" = {proc_input_values['Constant']}")
		name_label.setAlignment(Qt.AlignCenter)
		remove_btn = QPushButton("Remove")
		remove_btn.setFixedWidth(remove_btn.sizeHint().width() + 20)
		remove_btn.setStyleSheet("font-size: 15px;")
		proc_row.addWidget(name_label)
		proc_row.addWidget(remove_btn)
	
		self.proc_scroll_layout.insertWidget(self.proc_scroll_layout.count() - 1,container)
				
		def remove_row():
			self.proc_scroll_layout.removeWidget(container)
			container.deleteLater()
			self.proc_list.remove((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))

		remove_btn.clicked.connect(remove_row)


	def plot_states(self):
		lines=pg.PlotDataItem()
		self.plot_graph.addItem()	

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())
