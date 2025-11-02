# <img src="https://raw.githubusercontent.com/leonardo-diciano/Jablonski-Plots/main/screenshots/icon.png" alt="icon" width="50" />    Jablonski Plots
### An easy way to plot publication-ready Jablonski diagrams 
[![DOI](https://zenodo.org/badge/1052758037.svg)](https://doi.org/10.5281/zenodo.17508675)

![Screenshot of Jablonski Plots app](https://raw.githubusercontent.com/leonardo-diciano/Jablonski-Plots/main/screenshots/screen2.png)

### Installation
Jablonski Plots can be easily installed from pip.
```
 pip install jablonski-plots
```
Alternatively, it is possible to clone this repository
```
 git clone git@github.com:leonardo-diciano/Jablonski-Plots.git
```
and the program can be run directly or through a python interpreter, no installation is needed. 
```
./jablonski-plots.py
```
```
python jablonski-plots.py
```
The cloned Jablonski Plots directory may be added to the system PATH, for a quicker start.
```
export $PATH:"your_file_path/Jablonski-Plots/:$PATH"
#Then, to execute it, just type the program name from anywhere in your computer
jablonski-plots.py
```
The required libraries are:
  * PyQt6;
  * numpy;
  * pyqtgraph.

### Usage and Features
After Jablonski Plots app can be easily launched from the command line and the GUI is very intuitive. It is composed by three main parts:
  * On the left there is the Jablonski plot, which readily updates each them new information are added or removed.
  * On the center there is the main menu, composed by:
      * An _Add New State_ section, where the state label (ie. S_1 or T_1), its energy and its color in the plot may be chosen for each state inserted. The procedure is completed with the corresponding Save button. At the moment, only singlet states with labels starting by "S" and triplet states with labels starting by "T" works.
      * An _Add New Process_ section, where the process type may be selected between fluorescence (FLU), internal conversion (IC), intersystem crossing (ISC), reverse intersystem crossing (RISC), phosphoresence (PHO) and absorbance(ABS). Then, the initial and final state for the process can be selected between the added states and the corresponding rate constant may be written in the last entry. The information are stored with the "Save" button and the plot is updated accordingly. For the absorbance feature, the rate constant field is subsituted with an absorption coefficient coefficient, a plain text or just nothing.
      * A _Rescale Energy Axis_ section, which allows to indicate the minimum and maximum Y value for the energy axis and apply it to the plot with the Apply button.
      * A _Save as Image_ button, that allows to export the Jablonski plot as .PNG, .JPEG and .SVG files in the desired location.
      * A _Plot Again_ button, which shuffles the label positions and allows to easily fix any visualization problem.
  * On the right, two list will keep track of every state (_State Energies List_) and process (_Process List_) added in the system, alongside with a button to remove each one of them.

### Processes representations
In Jablonski Plots, each process is represented with a specific type of arrow:
  * Fluorescence (FLU) and Phosphorescence (PHO) processes are depicted with solid vertical arrows;
  * Internal conversion (IC) is represented by a vertical wiggly arrow;
  * Intersystem crossing (ISC) and reverse intersystem crossing (RISC) are represented by curved wiggly arrows;
  * Absorption (ABS) is represented by a dashed vertical arrow.
The arrows and their label are of the same color as their intial state, with exception of absorption where the arrow color depends on the final state.

### Examples
<p align="center">
  <img src="https://raw.githubusercontent.com/leonardo-diciano/Jablonski-Plots/main/screenshots/example1.png" alt="Image 1" width="43.7%"/>
  <img src="https://raw.githubusercontent.com/leonardo-diciano/Jablonski-Plots/main/screenshots/example2.png" alt="Image 2" width="45%"/>
</p>

![Screenshot of Jablonski Plots app](https://raw.githubusercontent.com/leonardo-diciano/Jablonski-Plots/main/screenshots/screen1.png)
