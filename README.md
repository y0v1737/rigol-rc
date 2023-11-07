# rigol-rc
# Library for RIGOL oscilloscope remote control
## **Disclaimer**

**All information is provided for educational purposes only. Follow these instructions at your own risk. Neither the authors nor their employer are responsible for any direct or consequential damage or loss arising from any person or organization acting or failing to act on the basis of information contained in this page.**

## Introduction

This repository is a library for rigol oscilloscope remote control. Rigol oscilloscope support many **SCPI** commands through USB. This library is wrapper for SCPI rilol command.

`NOTE:` Library  was tested only for MSO5000 series.
## Installation 

1) Install python requirements:
```
pip install pyvisa
pip install Pillow
```
2) Download rigolRC.py
3) Use class `Rigol` in your app

# Usage

1) Get ID of oscilloscope device for next work:
```
>>> import pyvisa
>>> rm = pyvisa.ResourceManager()
>>> rm.list_resources()
('USB0::0x1AB1::0x0515::MS5A250901328::INSTR', 'ASRL18::INSTR')
```
2) Include library & use:
```
from rigolRC import Rigol

# USE ID FROM PREVIOUS STEP
osc = Rigol('USB0::0x1AB1::0x0515::MS5A250901328::INSTR') 
idn = osc.idn()
print(idn)
```
# Examples

```
from rigolRC import Rigol

osc = Rigol('USB0::0x1AB1::0x0515::MS5A250901328::INSTR') 

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
wave, wave_size = osc.get_wave_raw(ch=1, start_position=0, points=100000)

# get wave only from display
wave, wave_size = osc.get_wave_norm(ch=1)

# set trigger mode: single
osc.trig_single()

# get trigger position
osc.get_trig_position()
```
