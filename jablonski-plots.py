#!/usr/bin/env python

import sys
from PyQt6.QtWidgets import (
    QApplication, QLayout, QWidget, QGridLayout, QVBoxLayout, QFileDialog,QLineEdit,
    QMessageBox, QFormLayout, QHBoxLayout, QMainWindow, QMenu, QComboBox,
    QDialog, QLabel, QGroupBox, QPushButton, QSpacerItem, QSizePolicy, QScrollArea, QColorDialog)
from PyQt6.QtGui import QFont , QKeyEvent, QIcon
from PyQt6.QtCore import Qt , QTimer, QPoint
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Jablonski Plots')
		self.setGeometry(100, 100, 800, 600)
	
		""" Initial conditions """
		self.states_dict={}
		self.states_list=[]
		self.proc_list=[]
		self.proc_ISC_list=[]
		self.sing_proc=[]
		self.label_list=[]
		self.x_val={'S':[0.2,1.2],'T':[2.2,2.8]}	
		self.states_color={}
		
		"""Set central widget and main layout"""
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		self.setCentralWidget(central_widget)

		self.plot_graph = pg.PlotWidget(background='w')
		main_layout.addWidget(self.plot_graph)
		self.plot_graph.setXRange(0,3.1)
		self.plot_graph.setYRange(-0.001,1.5)
		self.plot_graph.getPlotItem().hideAxis('bottom')
		self.plot_graph.setLabel("left",'<span style="color: black; font-size: 24px"> Energy (eV) </span>')
		self.plot_graph.getAxis("left").setPen(pg.mkPen(color='black',width=5))
		self.plot_graph.getAxis("left").setTickFont(QFont().setPointSize(14))
		self.plot_graph.getAxis("left").setTextPen(pg.mkPen(color='black'))
		self.plot_graph.getAxis("left").setTickSpacing(major=0.2,minor=0.2)
		self.plot_graph.getPlotItem().setMouseEnabled(x=False,y=False)		
		self.plot_graph.getPlotItem()	
		
		"""Right layout"""
		right_layout = QVBoxLayout()
		
		add_states_group = QGroupBox("Add New State")
		add_states_group.setFlat(True) 
		add_states_layout = QVBoxLayout()
		
		self.input_container = QWidget()
		self.input_layout = QVBoxLayout()
		#self.states_layout = QGridLayout()
		input_container_layout = QVBoxLayout()
		input_container_layout.addLayout(self.input_layout)
		#input_container_layout.addLayout(self.states_layout)
		input_container_layout.addSpacing(10)
		
		self.input_container.setLayout(input_container_layout)
		self.input_container.setVisible(False)
		add_states_layout.addWidget(self.input_container)
		add_states_group.setLayout(add_states_layout)
		
		right_layout.addWidget(add_states_group)
		
		add_process_group = QGroupBox("Add New Process")
		add_process_group.setFlat(True) 
		add_process_layout = QVBoxLayout()
		
		self.proc_input_container = QWidget()
		self.proc_input_layout = QVBoxLayout()
		proc_input_container_layout = QVBoxLayout()
		proc_input_container_layout.addLayout(self.proc_input_layout)
		proc_input_container_layout.addSpacing(10)
		self.proc_input_container.setLayout(proc_input_container_layout)
		self.proc_input_container.setVisible(False)
		add_process_layout.addWidget(self.proc_input_container)

		add_process_group.setLayout(add_process_layout)

		right_layout.addWidget(add_process_group)
		
		axis_rescale_group = QGroupBox("Rescale Energy Axis")
		axis_rescale_group.setFlat(True) 
		axis_rescale_layout = QVBoxLayout()
			
		self.rescale_axis_container = QWidget()
		self.rescale_axis_layout = QHBoxLayout()
		rescale_axis_container_layout = QHBoxLayout()
		rescale_axis_container_layout.addLayout(self.rescale_axis_layout)
		self.rescale_axis_container.setLayout(rescale_axis_container_layout)
		self.rescale_axis_container.setVisible(False)
		axis_rescale_layout.addWidget(self.rescale_axis_container)
		axis_rescale_group.setLayout(axis_rescale_layout)	
		right_layout.addWidget(axis_rescale_group)

		buttons_group = QGroupBox()
		buttons_group.setFlat(True) 
		buttons_layout=QVBoxLayout()
	
		self.save_button = QPushButton("Save as Image")
		self.save_button.clicked.connect(self.save_figure)
		buttons_layout.addWidget(self.save_button)
	
		self.reload_button = QPushButton("Plot Again")
		self.reload_button.clicked.connect(self.plot_again)	
		buttons_layout.addWidget(self.reload_button)

		buttons_group.setLayout(buttons_layout)	
		right_layout.addWidget(buttons_group)
		right_layout.addStretch(1)
		right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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
		    QGroupBox { font-family: Arial; font-size: 16pt;}
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
		self.rescale_axis_input()
		self.showMaximized()
	
	
	def add_state_function(self):
		for i in reversed(range(self.input_layout.count())):
			widget = self.input_layout.itemAt(i).widget()
			if widget is not None:
				widget.setParent(None)	
		self.input_fields={}
	
		"""State Name"""
		new_state_row = QHBoxLayout()
		name_label = QLabel(f"Name")
		name_edit = QLineEdit()
		name_edit.setText(f"S0")
		name_edit.setFixedSize(30, 25)
		new_state_row.addWidget(name_label)
		new_state_row.addWidget(name_edit)
		name_container = QWidget()
		name_container.setLayout(new_state_row)
		self.input_layout.addWidget(name_container)
		self.input_fields["Name"] = name_edit
		
		"""Energy"""
		energy_label = QLabel("Energy (eV)")
		energy_edit = QLineEdit()
		energy_edit.setText(f"0")
		energy_edit.setFixedSize(50, 25)
		new_state_row.addWidget(energy_label)
		new_state_row.addWidget(energy_edit)
		energy_container = QWidget()
		energy_container.setLayout(new_state_row)
		self.input_layout.addWidget(energy_container)
		self.input_fields["Energy"] = energy_edit

		"""Color"""
		color_label = QLabel(f"Color")
		self.color_button = QPushButton()
		self.color_button.setStyleSheet("background-color: black;")
		self.color_button.color_value = "#000000"
		self.color_button.setFixedSize(30, 30) 
		self.color_button.clicked.connect(self.choose_color)
		new_state_row.addWidget(color_label)
		new_state_row.addWidget(self.color_button)
		color_container= QWidget()
		color_container.setLayout(new_state_row)
		self.input_layout.addWidget(color_container)
		self.input_fields["Color"] = self.color_button 
		
		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_input_states)
		self.input_layout.addWidget(save_btn)
		
		self.input_container.setVisible(True)
	
	def save_input_states(self):
		"""Save input data and create the row for states"""
		input_values = {}
		for  key,field in self.input_fields.items(): 
			if isinstance(field,QLineEdit):
				input_values[key] = field.text() 
			elif isinstance(field, QPushButton) and hasattr(field, "color_value"):
				input_values[key] = field.color_value
			else:
				 input_values[key] = None
		container = QWidget()
		state_row = QHBoxLayout(container)
		
		self.states_dict.update({input_values["Name"]:float(input_values["Energy"])})	
		self.states_list.append(input_values["Name"])
		name_label = QLabel(f"<b>{input_values['Name']}: {input_values['Energy']} eV</b>")
		name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		remove_btn = QPushButton("Remove")
		remove_btn.setFixedWidth(remove_btn.sizeHint().width() + 20)
		remove_btn.setStyleSheet("font-size: 15px;")
		state_row.addWidget(name_label)
		state_row.addWidget(remove_btn)
		self.states_color.update({input_values["Name"]:input_values["Color"]})
			
		self.states_scroll_layout.insertWidget(self.states_scroll_layout.count() - 1,container)
		self.add_process_function()
		self.plot_states()			
		self.plot_process()		

		def remove_row():
			self.states_scroll_layout.removeWidget(container)
			container.deleteLater()
			self.states_dict.pop(input_values['Name'])
			self.states_list.remove(input_values['Name'])
			self.states_color.pop(input_values['Name'])
			self.add_process_function()
			self.plot_states()
			self.plot_process()		

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
		name_edit.addItems(['FLU','IC','PHO','ISC','RISC'])
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
		rate_edit.setFixedSize(300, 25)
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
		name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		remove_btn = QPushButton("Remove")
		remove_btn.setFixedWidth(remove_btn.sizeHint().width() + 20)
		remove_btn.setStyleSheet("font-size: 15px;")
		proc_row.addWidget(name_label)
		proc_row.addWidget(remove_btn)
		
		if proc_input_values["Name"] == 'ISC' or proc_input_values["Name"] == 'RISC':
			 self.proc_ISC_list.append((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))
		else:
			 self.sing_proc.append((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))
	
		self.proc_scroll_layout.insertWidget(self.proc_scroll_layout.count() - 1,container)
		self.plot_states()
		self.plot_process()		

		def remove_row():
			self.proc_scroll_layout.removeWidget(container)
			container.deleteLater()
			self.proc_list.remove((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))
			if proc_input_values["Name"] == 'ISC' or proc_input_values["Name"] == 'RISC': 
				self.proc_ISC_list.remove((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))
			else:
				self.sing_proc.remove((proc_input_values["Name"],proc_input_values["State1"],proc_input_values["State2"],proc_input_values["Constant"]))
			self.plot_states()
			self.plot_process()

		remove_btn.clicked.connect(remove_row)

	def choose_color(self):
		color = QColorDialog.getColor()
		if color.isValid():
			self.color_button.setStyleSheet(f"background-color: {color.name()};")
			self.color_button.color_value = color.name()

	def rescale_axis_input(self):
		for i in reversed(range(self.rescale_axis_layout.count())):
			widget = self.rescale_axis_layout.itemAt(i).widget()
			if widget is not None:
				widget.setParent(None)	
		self.axis_input_fields={}
	
		"""Minimum Y"""
		y_min_row = QHBoxLayout()
		y_min_label = QLabel(f"Y min")
		y_min_edit = QLineEdit()
		y_min_edit.setText(f"-0.001")
		y_min_edit.setFixedSize(40, 25)
		y_min_row.addWidget(y_min_label)
		y_min_row.addWidget(y_min_edit)
		y_min_container = QWidget()
		y_min_container.setLayout(y_min_row)
		self.rescale_axis_layout.addWidget(y_min_container)
		self.axis_input_fields["Ymin"] = y_min_edit
		
		"""Maximum Y"""
		y_max_row = QHBoxLayout()
		y_max_label = QLabel(f"Y max")
		y_max_edit = QLineEdit()
		y_max_edit.setText(f"1.5")
		y_max_edit.setFixedSize(40, 25)
		y_max_row.addWidget(y_max_label)
		y_max_row.addWidget(y_max_edit)
		y_max_container = QWidget()
		y_max_container.setLayout(y_max_row)
		self.rescale_axis_layout.addWidget(y_max_container)
		self.axis_input_fields["Ymax"] = y_max_edit

		apply_btn = QPushButton("Apply")
		apply_btn.clicked.connect(self.rescale_axis)
		self.rescale_axis_layout.addWidget(apply_btn)
		
		self.rescale_axis_container.setVisible(True)
	
	def rescale_axis(self):
		axis_rescale_input_values = {
		    key: field.text()
			for key, field in self.axis_input_fields.items()
		}
		self.plot_graph.setYRange(float(axis_rescale_input_values['Ymin']),float(axis_rescale_input_values['Ymax']))			
		

	def plot_states(self):
		self.plot_graph.clear()
		self.plot_graph.setXRange(0,3.5)

		if self.states_dict and all(v is not None for v in self.states_dict.values()):		
			self.plot_graph.setYRange(-0.001,max(1.5,max(self.states_dict.values())+0.25))
		else:
			self.plot_graph.setYRange(-0.001,1.5)
		for i in self.states_list:
			if i.startswith("T"):
				line=self.x_val["T"]
			else:
				line=self.x_val["S"]
			pen = pg.mkPen(color=self.states_color[i], width=5, style=Qt.PenStyle.SolidLine)
			energy=[float(self.states_dict[i]),float(self.states_dict[i])]
			self.plot_graph.plot(line,energy,pen=pen)
			text=pg.TextItem(html=f"<span style='font-size:24pt;'>{i[0]}<sub>{i[1]}</sub></span>",anchor=(0.5, 0.5))
			text.setColor(self.states_color[i])
			self.plot_graph.addItem(text)
			if i.startswith("T"):
				text.setPos(line[1]+0.12,energy[0])
			else:
				text.setPos(line[0]-0.12,energy[0])
		
	def plot_process(self):
		self.label_list=[]
		all_lbl=[]
		points=np.linspace(self.x_val["S"][0],self.x_val["S"][1]-0.4,len(self.sing_proc))
		sing_ISC_points=np.linspace(self.x_val["S"][0]+0.4,self.x_val["S"][1],len(self.proc_ISC_list))
		trip_ISC_points=np.linspace(self.x_val["T"][0],self.x_val["T"][1]-0.15,len(self.proc_ISC_list))

		for j,i in enumerate(self.sing_proc):
			if i[0] == 'FLU': 
				self.draw_straight_arrow(points[j],self.states_dict[i[1]],self.states_dict[i[2]],self.states_color[i[1]])	
				all_lbl.append((points[j],i))
			elif i[0] == 'IC': 
				self.draw_wiggly(points[j],self.states_dict[i[1]],self.states_dict[i[2]],self.states_color[i[1]])
				all_lbl.append((points[j],i))
			else:
				pass

		for j,i in enumerate(self.proc_ISC_list):
			if i[0] == 'ISC': 
				self.draw_wiggly_curved(sing_ISC_points[j],self.states_dict[i[1]],trip_ISC_points[j],self.states_dict[i[2]],self.states_color[i[1]])
				dx=trip_ISC_points[j] - sing_ISC_points[j] 
				all_lbl.append((sing_ISC_points[j] + dx/2,i))
			elif i[0] == 'RISC': 
				self.draw_wiggly_curved(trip_ISC_points[j],self.states_dict[i[1]],sing_ISC_points[j],self.states_dict[i[2]],self.states_color[i[1]])
				dx=trip_ISC_points[j] - sing_ISC_points[j] 
				all_lbl.append((sing_ISC_points[j] + dx/2,i))
			elif i[0] == 'PHO': 
				self.draw_straight_arrow(trip_ISC_points[j],self.states_dict[i[1]],self.states_dict[i[2]],self.states_color[i[1]])
				all_lbl.append((points[j],i))
			else:
				pass
		self.plot_label(all_lbl)
	

	def draw_wiggly_curved(self,x_start,y_start,x_end,y_end,color):
		dy=y_end - y_start
		dx=x_end - x_start
		t=np.linspace(0,1,300)
		length=np.hypot(dx,dy)
		nx=-dy/length
		ny=dx/length
		if dy < 0 and dx < 0:
			wiggle=0.015*np.sin(2*np.pi*10*t)+(0.5*t**2)*(1-t)
		elif dy > 0 and dx > 0:
			wiggle=0.015*np.sin(2*np.pi*10*t)+(0.5*t**2)*(1-t)
		elif dy < 0 and dx > 0:
			wiggle=0.015*np.sin(2*np.pi*10*t)-(0.5*t**2)*(1-t)
		elif dy > 0 and dx < 0:
			wiggle=0.015*np.sin(2*np.pi*10*t)-(0.5*t**2)*(1-t)
		angle = np.arctan2(dy, dx)
		cos_a = np.cos(angle)
		sin_a = np.sin(angle)
		x_rot = cos_a * length * t - sin_a * wiggle
		y_rot = sin_a * length * t + cos_a * wiggle
		x_wiggle = x_start + x_rot
		y_wiggle = y_start + y_rot   
		pen = pg.mkPen(color=color, width=5, style=Qt.PenStyle.SolidLine)
		self.plot_graph.plot(x_wiggle,y_wiggle,pen=pen)
		if dy < 0 and dx < 0:
			self.plot_graph.plot([x_end-0.02,x_end,x_end+0.02],[y_end-0.02,y_end,y_end-0.02],pen=pen)
		elif dy > 0 and dx > 0:
			self.plot_graph.plot([x_end-0.02,x_end,x_end+0.02],[y_end+0.02,y_end,y_end-+0.02],pen=pen)
		elif dy < 0 and dx > 0:
			self.plot_graph.plot([x_end-0.02,x_end,x_end+0.02],[y_end-0.02,y_end,y_end-0.02],pen=pen)
		elif dy > 0 and dx < 0:
			self.plot_graph.plot([x_end-0.02,x_end,x_end+0.02],[y_end+0.02,y_end,y_end+0.02],pen=pen)
		return

	def draw_wiggly(self,x,y_start,y_end,color):
		pen = pg.mkPen(color=color, width=5, style=Qt.PenStyle.SolidLine)
		dy=y_end - y_start
		y=np.linspace(y_start,y_end+0.02,200)
		x_wiggle=x+0.03*np.sin(2*np.pi*10*(y-y_start)/dy)
		self.plot_graph.plot(x_wiggle,y,pen=pen)
		if y_end-y_start > 0 :
			self.plot_graph.plot([x-0.02,x,x+0.02],[y_end-0.02,y_end,y_end-0.02],pen=pen)
		else:
			self.plot_graph.plot([x-0.02,x,x+0.02],[y_end+0.02,y_end,y_end+0.02],pen=pen)
		return

	def draw_straight_arrow(self,x,y_start,y_end,color):
		pen = pg.mkPen(color=color, width=5, style=Qt.PenStyle.SolidLine)
		self.plot_graph.plot([x,x],[y_start,y_end],pen=pen)
		if y_end-y_start > 0 :
			self.plot_graph.plot([x-0.02,x,x+0.02],[y_end-0.02,y_end,y_end-0.02],pen=pen)
		else:
			self.plot_graph.plot([x-0.02,x,x+0.02],[y_end+0.02,y_end,y_end+0.02],pen=pen)
		return

	def draw_dashed_arrow(self,x,y_start,y_end,color):
		pen = pg.mkPen(color=color, width=5, style=Qt.PenStyle.DashLine)
		self.plot_graph.plot([x,x],[y_start,y_end],pen=pen)
		if y_end-y_start > 0 :
			self.plot_graph.plot([x-0.02,x,x+0.02],[y_end-0.02,y_end,y_end-0.02],pen=pen)
		else:
			self.plot_graph.plot([x-0.02,x,x+0.02],[y_end+0.02,y_end,y_end+0.02],pen=pen)
		return

	def plot_label(self,all_lbl):
		font = QFont()
		font.setPointSize(24)
		for i in all_lbl:
			text=pg.TextItem(html=f"<span style='font-size:16pt; background-color:white; padding:2px'>k<sup>{i[1][0]}</sup>"
                                f"<sub>{i[1][1]}→{i[1][2]}</sub>"
                                f" = {i[1][3]}",anchor=(0.4, 0.5))
			text.setColor(self.states_color[i[1][1]])
			self.plot_graph.addItem(text)
			if i[1][0] == 'ISC' or i[1][0] == 'RISC':
				text.setPos(i[0],(self.states_dict[i[1][1]]+self.states_dict[i[1][2]])/2+np.random.rand()*(self.states_dict[i[1][2]]-self.states_dict[i[1][1]]))
			else:
				text.setPos(i[0],self.gen_label_y(self.states_dict[i[1][1]],self.states_dict[i[1][2]]))
			text.setFont(font)
		return

	def gen_label_y(self,y_start,y_end):
		check=True
		while check :
			sample_y=y_end + 0.05 + np.random.rand()*(y_start-y_end-0.1)
			error_flag=any(abs(elem - sample_y) <= 0.08 for elem in self.label_list)
			if not error_flag:
				check = False

		self.label_list.append(sample_y)
		return sample_y
	
	def plot_again(self):
		self.plot_states()
		self.plot_process()
	
	def save_figure(self):
		filename, _ = QFileDialog.getSaveFileName( self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;SVG Files(*.svg);;All Files (*)")
		if filename:
			if filename.lower().endswith(".svg"):
				exporter = pg.exporters.SVGExporter(self.plot_graph.plotItem)
				exporter.export(filename)
			else:
				exporter = pg.exporters.ImageExporter(self.plot_graph.plotItem)
				exporter.parameters()['width'] = self.plot_graph.width() * 3
				exporter.export(filename)

def main():
        app = QApplication(sys.argv) 
        window = MainWindow()
        window.setWindowIcon(QIcon("icon.png"))
        sys.exit(app.exec())

if __name__ == "__main__":
	main()
