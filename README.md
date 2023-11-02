# rigol-rc
# Library for RIGOL oscilloscope remote control library
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

