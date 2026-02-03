# Addition to the original project
Option to add gcode at the beginning and end of the file
Setting are saved between sessions
Added Italian and Spanish translations

# Lightburn_Gcode_z_plotter_conversion
Script that converts gcodes for laser engraver to pen up - down
LightBurn G-Code Pen Converter

A desktop tool that converts standard LightBurn G-code (laser output) into G-code suitable for pen plotters or laser engravers with z axis by automatically inserting pen up and pen down moves based on travel/cutting transitions.

This tool removes laser power commands, replaces them with Z-axis pen control, and includes adjustable settings for pen height and delay.
A simple GUI is provided, and the script can be compiled into a standalone .exe using PyInstaller.

Features
✅ Automatic G-code Conversion

The script:

Removes all laser power commands (Sxxx)

Removes laser ON/OFF commands (M3, M4, M5)

Inserts pen up (Z-raise) when transitioning from cutting (G1) to travel (G0)

Inserts pen down (Z-lower) when transitioning from travel (G0) to cutting (G1)

Supports LightBurn G-code where Sxxx is attached, e.g. X120.5Y50.2S700F9000

Optionally removes ending commands (M9, G1 S0, M2)

Optionally includes the original G-code line as a comment above the modified line

✅ Customizable Pen Settings (GUI)

The GUI allows modifying:

Pen up Z height

Pen down Z height

Pause duration (G4 Pxxx) between movements

Toggle cleanup of ending commands

Toggle keeping original code as comments

✅ SHX, LightBurn, CNC, Plotter Compatibility

This script is designed for:

X/Y/Z pen plotters

Modified laser machines with servo pen-lift

CNC machines running GRBL/Marlin

LightBurn-generated G-code

Any G-code using G0 for travel and G1 for drawing

How It Works
Pen Up Sequence

Inserted when script detects transition:
G1 → G0

G0 Z<pen_up_height>    ; pen up
G4 P<pause>            ; wait

Pen Down Sequence

Inserted when script detects transition:
G0 → G1

G0 Z<pen_down_height>  ; pen down
G4 P<pause>            ; wait

Laser Commands Removed

Examples:

M3 S1000  →  removed
M5        →  removed
G1 X50 S800 F12000  →  G1 X50 F12000

Installation
1. Install Python

Download Python 3.x from:
https://www.python.org/downloads/

During installation, check:

Add Python to PATH

2. Install PyInstaller (optional, for building .exe)
python -m pip install pyinstaller

Running the Script
Run directly with Python
python gcode_pen_gui.py


A GUI window will appear.

Building a Standalone .exe (Windows)

Run:

python -m PyInstaller --onefile --windowed gcode_pen_gui.py


After building, the executable will be located in:

dist/gcode_pen_gui.exe


You can now run it on any Windows machine without Python installed.

Usage Instructions

Launch the GUI.

Click Open G-code and select a LightBurn-generated .gcode/.nc file.

Adjust:

Pen Up Z

Pen Down Z

Pause (seconds)

Optional checkboxes:

Remove ending commands (M9, G1 S0, M2)

Keep original G-code as comments

Click Apply pen conversion.

Review output in the text window.

Click Save As... to export the converted G-code.

Example Output

Input:

G1 X50Y100S800F12000
G0 X120 Y140
G1 X190 Y200 S500


Output:

G1 X50 Y100 F12000    ; cutting move
G0 Z-35    ; pen up
G4 P0.5    ; wait 0.5 s
G0 X120 Y140    ; travel move
G0 Z-38    ; pen down
G4 P0.5    ; wait 0.5 s
G1 X190 Y200 F12000    ; cutting move

System Requirements

Windows 10/11

Python 3.8+ (only needed if running script directly)

GRBL/Marlin or any firmware that supports:

G0, G1

G4 pause

Z-axis lifting for pen control

License

Free for personal and commercial use.
No attribution required (but appreciated 😊).
