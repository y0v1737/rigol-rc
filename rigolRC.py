import struct
import pyvisa
from PIL import Image
import io
import matplotlib.pyplot as plt

class Rigol:
    def __init__(self, resource):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource)
        self.upd_current_info()
        
    def idn(self):
        return self.inst.query("*IDN?")

    def expstr2int(self, str):
        n = str.split("E")
        if len(n) == 1:
            return float(n[0])
        elif len(n) == 2:
            return float(n[0]) * (10 ** int(n[1], 10))

    def wave2format(self, wave, wave_size, format_bits):
        if format_bits == "WORD":
            form = "<H"
            step = 2
        elif format_bits == "BYTE":
            form = "<B"
            step = 1
        wave_b = []
        for i in range(0, wave_size, step):
            point = struct.unpack_from(form, wave[i:])[0]
            wave_b.append(point)
        return wave_b, len(wave_b)

    # Show wave. Test function for choose frame for research.
    # w & h -  figure size parametrs
    def show_wave(self, wave, w=15, h=3):
        plt.figure(figsize=(w,h))
        plt.plot(wave)
        plt.show()
        
    # Save screen to internal drive     
    def scrn_int(self, drive="C", name=""):
        self.inst.write(":SAVE:IMAGe " + drive + ":\\" + name + ".png")
        return self.inst.query(":SAVE:STATus?")

    # Download screen to your PC
    def scrn_ext(self, path_dir, name=""):
        disp_data = []
        print(self.inst.write(":DISPlay:DATA?"))
        self.inst.read_bytes(1)
        info_size = int(self.inst.read_bytes(1), 10)
        bmp_size = int(self.inst.read_bytes(info_size),10)
        bmp = self.inst.read_bytes(bmp_size)        
        img = Image.open(io.BytesIO(bmp))
        img.save(path_dir + "\\" + name + ".png", 'png')
        return bmp

    # Save current setup to internal drive
    def ssetup(self, drive="C", name=""):
        self.inst.write(":SAVE:SETup " + drive + ":\\" + name + ".stp")
        return self.inst.query(":SAVE:STATus?")

    # Load setup from internal drive
    def lsetup(self, drive="C", name=""):
        self.inst.write(":LOAD:SETup " + drive + ":\\" + name + ".stp")
        return 0

    # Set grid brightness <1...100>
    def grid(self, level):
        assert level in range(1, 101, 1)
        self.inst.write(":DISPlay:GBRightness ", str(level))
        return 0

    # Get wave only from display. Max 1000 points
    # Return <wave, wave_size>
    # format_bits: BYTE - for 0-8bits osc, WORD - for 9-16bits osc.
    # Example for 12bits oscilloscope: wave, wave_size = osc.get_wave_norm(1, "WORD")
    # Example for 8bits oscilloscope: wave, wave_size = osc.get_wave_norm(1, "BYTE")
    def get_wave_norm(self, ch, format_bits):
        assert (format_bits == "BYTE") or (format_bits == "WORD")
        wave_data = []
        points=1000
        self.inst.write(":WAVeform:SOUR CHAN" + str(ch))
        self.inst.write(":WAV:MODE NORM")
        self.inst.write(":WAVeform:FORMat " + format_bits)
        self.inst.write(":WAVeform:POINts " + str(points))
        self.inst.write(":WAVeform:DATA?")
        self.inst.read_bytes(1)
        info_size = int(self.inst.read_bytes(1), 10)
        wave_size = int(self.inst.read_bytes(info_size),10)
        wave = self.inst.read_bytes(wave_size)
        wave, wave_size = self.wave2format(wave, wave_size, format_bits)
        if points != wave_size:
            print("WARNING: expect " + str(points) + ", given " + str(wave_size))
        return wave, wave_size
        
    # Get RAW wave from internal memory
    # Return <wave, wave_size>
    # format_bits: BYTE - for 0-8bits osc, WORD - for 9-16bits osc.
    # Example for 12bits oscilloscope: wave, wave_size = osc.get_wave_raw(1, 0, 1000, "WORD")
    # Example for 8bits oscilloscope: wave, wave_size = osc.get_wave_raw(1, 0, 1000, "BYTE")
    def get_wave_raw(self, ch, start_position, points, format_bits):
        assert (format_bits == "BYTE") or (format_bits == "WORD")
        wave_data = []
        self.inst.write(":WAVeform:SOUR CHAN" + str(ch))
        self.inst.write(":WAV:MODE RAW")
        self.inst.write(":WAVeform:FORMat " + format_bits)
        self.inst.write(":WAVeform:STARt " + str(start_position))
        self.inst.write(":WAVeform:POINts " + str(points))    
        self.inst.write(":WAVeform:DATA?")
        self.inst.read_bytes(1)
        info_size = int(self.inst.read_bytes(1), 10)
        wave_size = int(self.inst.read_bytes(info_size),10)
        wave = self.inst.read_bytes(wave_size)   
        wave, wave_size = self.wave2format(wave, wave_size, format_bits)
        if points != wave_size:
            print("WARNING: expect " + str(points) + ", given " + str(wave_size))
        return wave, wave_size

    # Trigger mode: single
    def trig_single(self):
        self.inst.write(":SINGle")

    # Update current settings info
    def upd_current_info(self):
        self.main_scale = self.expstr2int(self.inst.query(":TIMebase:MAIN:SCALe?"))
        self.sample_rate = self.expstr2int(self.inst.query(":ACQuire:SRATe?"))
        self.memdepth = self.expstr2int(self.inst.query(":ACQuire:MDEPth?"))
        self.main_offset_time = self.expstr2int(self.inst.query(":TIMebase:MAIN:OFFSet?"))
        self.main_offset_point = self.sample_rate * self.main_offset_time  
        self.main_position_point = self.memdepth/2 + self.main_offset_point
        self.points_in_cell = self.main_scale * self.sample_rate
        self.trig_position_point = self.main_position_point - self.main_offset_point

    # Print info abount current settings 
    def print_current_info(self):
        self.upd_current_info()
        print("main_scale", self.main_scale)
        print("sample_rate", self.sample_rate)
        print("memdepth", self.memdepth)
        print("main_offset_time", self.main_offset_time)
        print("main_offset_point", self.main_offset_point)
        print("main_position_point", self.main_position_point)
        print("points_in_cell", self.points_in_cell)
        print("trig_position_point", self.trig_position_point)

    # Get sample rate
    def get_sample_rate(self):
        self.upd_current_info()
        return self.sample_rate

    # Get memory depth 
    def get_memdepth(self):
        self.upd_current_info()        
        return self.memdepth

    # {AUTO|1k|10k|100k|1M|10M|25M|50M|100M|200M} - discrete
    # Example: set_memdepth("10M")
    def set_memdepth(self, md):
        self.inst.write(":ACQuire:MDEPth " + md)
        self.upd_current_info()        
        return self.memdepth

    # Get main offset.
    # Return: main offset in points
    def get_main_offset(self):
        self.upd_current_info()       
        return self.main_offset_point

    # Set main offset. time_s - time in secconds
    def set_main_offset(self, time_s ):
        self.inst.write(":TIMebase:MAIN:OFFSet " + str(time_s))
        self.upd_current_info()
        return self.main_offset_point

    # Get main position in points. Points offset from start wave in memory to centert of display.
    def get_main_position(self):
        self.upd_current_info()        
        return self.main_position_point

    # Get main scale. time in secconds
    def get_main_scale(self):
        self.upd_current_info() 
        return self.main_scale

    # Set main scale. time_s - time in secconds
    # Set_main_scale(0.003) - set 3ms scale
    def set_main_scale(self, time_s):
        self.inst.write(":TIMebase:MAIN:SCALe " + str(time_s))
        self.upd_current_info() 
        return self.main_scale

    # Return: how many points in one cell
    def get_points_in_cell(self):
        self.upd_current_info() 
        return self.points_in_cell

    # Get trigger position. Points offset from start wave in memory to trigger
    def get_trig_position(self):
        self.upd_current_info()
        return self.trig_position_point
