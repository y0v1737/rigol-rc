# rigol-rc
# Library for RIGOL oscilloscope remote control
## **Disclaimer**

**All information is provided for educational purposes only. Follow these instructions at your own risk. Neither the authors nor their employer are responsible for any direct or consequential damage or loss arising from any person or organization acting or failing to act on the basis of information contained in this page.**

## Introduction

This repository is a library for rigol oscilloscope remote control. Rigol oscilloscope support many **SCPI** commands through USB or LAN. This library is wrapper for SCPI rigol command.

`NOTE:` Library  was tested only for MSO5000, DHO900, DHO800 series.
## Installation 

1) Install python requirements:
```
pip install pyvisa pyvisa-py
pip install Pillow
pip install matplotlib
```
2) Download rigolRC.py
3) Use class `Rigol` in your app

# Usage

1) Get ID of oscilloscope device for next work:
```
>>> import pyvisa
>>> rm = pyvisa.ResourceManager()
>>> rm.list_resources()
('USB0::0x1AB1::0x0515::MS5A250901328::INSTR', 'ASRL18::INSTR') # for USB device
('TCPIP::192.168.136.138::INSTR',) # for LAN(LXI) device
```
2) Include library & use:
```
from rigolRC import Rigol

# USE ID FROM PREVIOUS STEP
# osc = Rigol('USB0::0x1AB1::0x0515::MS5A250901328::INSTR') # for USB device
osc = Rigol('TCPIP::192.168.136.138::INSTR') # for LAN(LXI) device
idn = osc.idn()
print(idn)
```
![Screenshot_1](https://github.com/y0v1737/rigol-rc/assets/128224033/08dfac8b-614a-427f-a3f1-6c7625ad80df)

# Examples

```
from rigolRC import Rigol

osc = Rigol('USB0::0x1AB1::0x0515::MS5A250901328::INSTR') # for USB device
osc = Rigol('TCPIP::192.168.136.138::INSTR') # for LAN(LXI) device

# print identificator
print(osc.idn())

# save screnshoot to your PC
osc.scrn_ext("C:\\img_osc", name="test_img")

# save screnshoot to internal memory
osc.scrn_int(name="test_img")

# save & load setup
osc.ssetup("set-for_glitch")
osc.lsetup("set-for_glitch")

# set grid brightness
osc.grid(100)

# get wave RAW
wave, wave_size = osc.get_wave_raw(ch=1, start_position=0, points=100000, "WORD") # for 9-16 bits oscilloscope
wave, wave_size = osc.get_wave_raw(1, 0, 1000, "BYTE") # for 0-8  bits oscilloscope

# get wave only from display
wave, wave_size = osc.get_wave_norm(ch=1, "WORD") # for 9-16 bits oscilloscope
wave, wave_size = osc.get_wave_norm(ch=1, "BYTE") # for 0-8  bits oscilloscope

# set trigger mode: single
osc.trig_single()

# Show waveform in figure
osc.show_wave(wave)

# get trigger position
osc.get_trig_position()

# Get wave from trigger with 2 cell len
osc.trig_single()
...do something 
NUM_CELL = 2
wave, wave_size = osc.get_wave_raw(1, osc.trig_position_point, osc.points_in_cell * NUM_CELL, "WORD")
osc.show_wave(wave)
```
