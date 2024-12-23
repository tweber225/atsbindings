from enum import Enum, IntEnum
from ctypes import Structure, c_uint64, c_uint32, c_uint16, c_uint8, c_uint, c_bool


class ClockSources(Enum):
    INTERNAL_CLOCK = 1
    FAST_EXTERNAL_CLOCK = 2
    MEDIUM_EXTERNAL_CLOCK = 3
    SLOW_EXTERNAL_CLOCK = 4
    EXTERNAL_CLOCK_AC = 5
    EXTERNAL_CLOCK_DC = 6
    EXTERNAL_CLOCK_10MHz_REF = 7
    INTERNAL_CLOCK_10MHz_REF = 8
    EXTERNAL_CLOCK_10MHz_PXI = 10
    INTERNAL_CLOCK_DIV_4 = 15
    INTERNAL_CLOCK_DIV_5 = 16
    MASTER_CLOCK = 17
    INTERNAL_CLOCK_SET_VCO = 18

    def __str__(self):
        """ Provides a readable version """      
        words = self.name.split('_')
        for i in range(len(words)):
            if words[i].upper() in ["DC", "AC"]:  # Check if the word is an abbreviation (all uppercase)
                continue  # Don't change it
            words[i] = words[i].capitalize()  # Capitalize normal words
        
        return ' '.join(words)

    @classmethod
    def from_str(cls, source_str:str):
        """ Returns the enumeration matching the readable string """
        normalized_str = source_str.replace(' ', '_').upper()
        try:
            return cls[normalized_str]
        except KeyError:
            raise ValueError(f"'{source_str}' is not a valid ClockSources enum string")


class SampleRates(Enum):
    """
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetCaptureClock.html#c.ALAZAR_SAMPLE_RATES
    """
    SAMPLE_RATE_1KSPS = 0x00000001
    SAMPLE_RATE_2KSPS = 0x00000002
    SAMPLE_RATE_5KSPS = 0x00000004
    SAMPLE_RATE_10KSPS = 0x00000008
    SAMPLE_RATE_20KSPS = 0x0000000A
    SAMPLE_RATE_50KSPS = 0x0000000C
    SAMPLE_RATE_100KSPS = 0x0000000E
    SAMPLE_RATE_200KSPS = 0x00000010
    SAMPLE_RATE_500KSPS = 0x00000012
    SAMPLE_RATE_1MSPS = 0x00000014
    SAMPLE_RATE_2MSPS = 0x00000018
    SAMPLE_RATE_5MSPS = 0x0000001A
    SAMPLE_RATE_10MSPS = 0x0000001C
    SAMPLE_RATE_20MSPS = 0x0000001E
    SAMPLE_RATE_25MSPS = 0x00000021
    SAMPLE_RATE_50MSPS = 0x00000022
    SAMPLE_RATE_100MSPS = 0x00000024
    SAMPLE_RATE_125MSPS = 0x00000025
    SAMPLE_RATE_160MSPS = 0x00000026
    SAMPLE_RATE_180MSPS = 0x00000027
    SAMPLE_RATE_200MSPS = 0x00000028
    SAMPLE_RATE_250MSPS = 0x0000002B
    SAMPLE_RATE_400MSPS = 0x0000002D
    SAMPLE_RATE_500MSPS = 0x00000030
    SAMPLE_RATE_800MSPS = 0x00000032
    SAMPLE_RATE_1000MSPS = 0x00000035
    SAMPLE_RATE_1200MSPS = 0x00000037
    SAMPLE_RATE_1500MSPS = 0x0000003A
    SAMPLE_RATE_1600MSPS = 0x0000003B
    SAMPLE_RATE_1800MSPS = 0x0000003D
    SAMPLE_RATE_2000MSPS = 0x0000003F
    SAMPLE_RATE_2400MSPS = 0x0000006A
    SAMPLE_RATE_3000MSPS = 0x00000075
    SAMPLE_RATE_3600MSPS = 0x0000007B
    SAMPLE_RATE_4000MSPS = 0x00000080
    SAMPLE_RATE_300MSPS = 0x00000090
    SAMPLE_RATE_350MSPS = 0x00000094
    SAMPLE_RATE_370MSPS = 0x00000096
    SAMPLE_RATE_5000MSPS = 0x000000A0
    SAMPLE_RATE_10000MSPS = 0x000000B0
    SAMPLE_RATE_1333MSPS_RECUR_DECIMAL = 0x000000C0
    SAMPLE_RATE_2666MSPS_RECUR_DECIMAL = 0x000000C1
    SAMPLE_RATE_USER_DEF = 0x00000040

    # Class method to find the enum by Hz value
    @classmethod
    def from_hertz(cls, hz):
        """
        Return the SampleRate enum based on the desired sample rate in Hz.
        """
        # Mapping from sample rate in Hz to Enum members
        _rate_map = {
            1000: cls.SAMPLE_RATE_1KSPS,
            2000: cls.SAMPLE_RATE_2KSPS,
            5000: cls.SAMPLE_RATE_5KSPS,
            10000: cls.SAMPLE_RATE_10KSPS,
            20000: cls.SAMPLE_RATE_20KSPS,
            50000: cls.SAMPLE_RATE_50KSPS,
            100000: cls.SAMPLE_RATE_100KSPS,
            200000: cls.SAMPLE_RATE_200KSPS,
            500000: cls.SAMPLE_RATE_500KSPS,
            1000000: cls.SAMPLE_RATE_1MSPS,
            2000000: cls.SAMPLE_RATE_2MSPS,
            5000000: cls.SAMPLE_RATE_5MSPS,
            10000000: cls.SAMPLE_RATE_10MSPS,
            20000000: cls.SAMPLE_RATE_20MSPS,
            25000000: cls.SAMPLE_RATE_25MSPS,
            50000000: cls.SAMPLE_RATE_50MSPS,
            100000000: cls.SAMPLE_RATE_100MSPS,
            125000000: cls.SAMPLE_RATE_125MSPS,
            160000000: cls.SAMPLE_RATE_160MSPS,
            180000000: cls.SAMPLE_RATE_180MSPS,
            200000000: cls.SAMPLE_RATE_200MSPS,
            250000000: cls.SAMPLE_RATE_250MSPS,
            400000000: cls.SAMPLE_RATE_400MSPS,
            500000000: cls.SAMPLE_RATE_500MSPS,
            800000000: cls.SAMPLE_RATE_800MSPS,
            1000000000: cls.SAMPLE_RATE_1000MSPS,
            1200000000: cls.SAMPLE_RATE_1200MSPS,
            1500000000: cls.SAMPLE_RATE_1500MSPS,
            1600000000: cls.SAMPLE_RATE_1600MSPS,
            1800000000: cls.SAMPLE_RATE_1800MSPS,
            2000000000: cls.SAMPLE_RATE_2000MSPS,
            2400000000: cls.SAMPLE_RATE_2400MSPS,
            3000000000: cls.SAMPLE_RATE_3000MSPS,
            3600000000: cls.SAMPLE_RATE_3600MSPS,
            4000000000: cls.SAMPLE_RATE_4000MSPS
        }
        if hz in _rate_map.keys():
            return _rate_map[hz]
        raise ValueError(f"No matching sample rate found for {hz} Hz")
    
    @classmethod
    def from_str(cls, rate_str:str):
        v, u = rate_str.split()
        if u == "kS/s":
            return cls[f"SAMPLE_RATE_{v}KSPS"]
        elif u == "MS/s":
            return cls[f"SAMPLE_RATE_{v}MSPS"]
        elif u == "GS/s":
            return cls[f"SAMPLE_RATE_{int(v*1000)}MSPS"]
        else:
            raise ValueError("Invalid rate string unit: {u}")
    
        

    @property
    def to_hertz(self):
        rate = self.name[12:]
        if rate[-4:] == "KSPS":
            return int(float(rate[:-4])*1e3)
        elif rate[-4:] == "MSPS":
            return int(float(rate[:-4])*1e6)
        
    def __str__(self) -> str:
        h = self.to_hertz
        if h < 1e6:
            return f"{int(h/1000)} kS/s"
        elif h < 1e9:
            return f"{int(h/1000000)} MS/s"
        else:
            return f"{h/1000000000:.1f} GS/s"
        

class ClockEdges(Enum):
    CLOCK_EDGE_RISING = 0
    CLOCK_EDGE_FALLING = 1

    def __str__(self):
        """ Provides a readable version """
        if self.value == 0:
            return "Rising"
        else:
            return "Falling"
        
    @classmethod
    def from_str(cls, edge_str:str):
        if edge_str.lower() == "rising":
            return cls.CLOCK_EDGE_RISING
        elif edge_str.lower() == "falling":
            return cls.CLOCK_EDGE_FALLING
        else:
             raise ValueError(f"'{edge_str}' is not a valid ClockEdges enum string")


class Channels(IntEnum):
    CHANNEL_ALL = 0 # Untested
    CHANNEL_A = 1
    CHANNEL_B = 2
    CHANNEL_C = 4
    CHANNEL_D = 8
    CHANNEL_E = 16
    CHANNEL_F = 32
    CHANNEL_G = 64
    CHANNEL_H = 128
    CHANNEL_I = 256
    CHANNEL_J = 512
    CHANNEL_K = 1024
    CHANNEL_L = 2048
    CHANNEL_M = 4096
    CHANNEL_N = 8192
    CHANNEL_O = 16384
    CHANNEL_P = 32768

    @classmethod
    def from_int(cls, i):
        c = chr(i + ord('A'))
        return getattr(cls, "CHANNEL_"+c)


class ADMAModes(IntEnum):
    ADMA_TRADITIONAL_MODE = 0
    ADMA_CONTINUOUS_MODE = 0x100
    ADMA_NPT = 0x200
    ADMA_TRIGGERED_STREAMING = 0x400

    def __str__(self):
        if self.value == 0:
            return "Traditional"
        elif self.value == 0x100:
            return "Continuous"
        elif self.value == 0x200:
            return "NPT"
        else:
            return "Triggered streaming"
        
    @classmethod
    def from_str(cls, mode:str):
        mode_lower = mode.lower()
        if mode_lower == "traditional":
            return cls.ADMA_TRADITIONAL_MODE
        elif mode_lower == "continuous":
            return cls.ADMA_CONTINUOUS_MODE
        elif mode_lower in ["npt", "no pretrigger", "no pre-trigger"]:
            return cls.ADMA_NPT
        elif mode_lower == "triggered streaming":
            return cls.ADMA_TRIGGERED_STREAMING
        else:
            raise ValueError(f"Invalid ADMA mode: {mode}")
        

class ADMAFlags(IntEnum):
    ADMA_EXTERNAL_STARTCAPTURE = 0x1
    ADMA_ENABLE_RECORD_HEADERS = 0x8
    ADMA_ALLOC_BUFFERS = 0x20
    ADMA_FIFO_ONLY_STREAMING = 0x800
    ADMA_INTERLEAVE_SAMPLES = 0x1000
    ADMA_GET_PROCESSED_DATA = 0x2000
    ADMA_DSP = 0x4000
    ADMA_ENABLE_RECORD_FOOTERS = 0x10000
    ADMA_PARALLEL_DMA = 0x20000


class AuxInputLevels(Enum):
    AUX_INPUT_LOW = 0
    AUX_INPUT_HIGH = 1


class BoardKind(Enum):
    ATS850 = 1
    ATS310 = 2
    ATS330 = 3
    ATS855 = 4
    ATS315 = 5
    ATS335 = 6
    ATS460 = 7
    ATS860 = 8
    ATS660 = 9
    ATS665 = 10
    ATS9462 = 11
    ATS9870 = 13
    ATS9350 = 14
    ATS9325 = 15
    ATS9440 = 16
    ATS9351 = 18
    ATS9850 = 21
    ATS9625 = 22
    ATS9626 = 24
    ATS9360 = 25
    AXI9870 = 26
    ATS9370 = 27
    ATS9373 = 29
    ATS9416 = 30
    ATS9637 = 31
    ATS9120 = 32
    ATS9371 = 33
    ATS9130 = 34
    ATS9352 = 35
    ATS9453 = 36
    ATS9146 = 37
    ATS9437 = 40
    ATS9618 = 41
    ATS9358 = 42
    ATS9353 = 44
    ATS9872 = 45
    ATS9628 = 47


class BoardOptionsLow(Enum):
    OPTION_STREAMING_DMA = (1 << 0)
    OPTION_EXTERNAL_CLOCK = (1 << 1)
    OPTION_DUAL_PORT_MEMORY = (1 << 2)
    OPTION_180MHZ_OSCILLATOR = (1 << 3)
    OPTION_LVTTL_EXT_CLOCK = (1 << 4)
    OPTION_SW_SPI = (1 << 5)
    OPTION_ALT_INPUT_RANGES = (1 << 6)
    OPTION_VARIABLE_RATE_10MHZ_PLL = (1 << 7)
    OPTION_MULTI_FREQ_VCO = (1 << 7)
    OPTION_2GHZ_ADC = (1 << 8)
    OPTION_DUAL_EDGE_SAMPLING = (1 << 9)
    OPTION_DCLK_PHASE = (1 << 10)
    OPTION_WIDEBAND = (1 << 11)


class BoardOptionsHigh(Enum):
    OPTION_OEM_FPGA = (1 << 15)


class InputRanges(Enum):
    INPUT_RANGE_PM_20_MV = 0x1
    INPUT_RANGE_PM_40_MV = 0x2
    INPUT_RANGE_PM_50_MV = 0x3
    INPUT_RANGE_PM_80_MV = 0x4
    INPUT_RANGE_PM_100_MV = 0x5
    INPUT_RANGE_PM_200_MV = 0x6
    INPUT_RANGE_PM_400_MV = 0x7
    INPUT_RANGE_PM_500_MV = 0x8
    INPUT_RANGE_PM_800_MV = 0x9
    INPUT_RANGE_PM_1_V = 0xA
    INPUT_RANGE_PM_2_V = 0xB
    INPUT_RANGE_PM_4_V = 0xC
    INPUT_RANGE_PM_5_V = 0xD
    INPUT_RANGE_PM_8_V = 0xE
    INPUT_RANGE_PM_10_V = 0xF
    INPUT_RANGE_PM_20_V = 0x10
    INPUT_RANGE_PM_40_V = 0x11
    INPUT_RANGE_PM_16_V = 0x12
    INPUT_RANGE_PM_1_V_25 = 0x21
    INPUT_RANGE_PM_2_V_5 = 0x25
    INPUT_RANGE_PM_125_MV = 0x28
    INPUT_RANGE_PM_250_MV = 0x30

    # Class method to find the enum by V value
    @classmethod
    def from_v(cls, v):
        """
        Return the InputRanges enum based on the desired range in volts (V).
        """
        whole_num = int(v)
        decimal = v - whole_num
        millivolts = int(1000*decimal)
        if whole_num > 0:
            if millivolts == 250:
                volts_string = f"{whole_num}_V_25"
            elif millivolts == 500:
                volts_string = f"{whole_num}_V_5"
            else:
                volts_string = f"{whole_num}_V"
        else:
            volts_string = f"{millivolts}_MV"
        
        volts_string = "INPUT_RANGE_PM_" + volts_string
            
        if hasattr(cls, volts_string):
            return getattr(cls, volts_string)
        raise ValueError(f"No matching input range found for {v} V")
    
    @classmethod
    def from_str(cls, range_str:str):
        strsplit = range_str.split()
        v = float(strsplit[0].replace("±",""))
        u = strsplit[1].lower()
        if u == "mv":
            return cls.from_v(v/1000)
        elif u == "v":
            return cls.from_v(v)
        raise ValueError(f"No matching input range for string, {range_str}")
        
    @property
    def to_volts(self):
        if self.name == "INPUT_RANGE_PM_20_MV": 
            return 0.02
        elif self.name == "INPUT_RANGE_PM_40_MV": 
            return 0.04
        elif self.name == "INPUT_RANGE_PM_50_MV": 
            return 0.05
        elif self.name == "INPUT_RANGE_PM_80_MV": 
            return 0.08
        elif self.name == "INPUT_RANGE_PM_100_MV": 
            return 0.1
        elif self.name == "INPUT_RANGE_PM_125_MV": 
            return 0.125
        elif self.name == "INPUT_RANGE_PM_200_MV": 
            return 0.2
        elif self.name == "INPUT_RANGE_PM_250_MV": 
            return 0.25
        elif self.name == "INPUT_RANGE_PM_400_MV": 
            return 0.4
        elif self.name == "INPUT_RANGE_PM_500_MV": 
            return 0.5
        elif self.name == "INPUT_RANGE_PM_800_MV": 
            return 0.8
        elif self.name == "INPUT_RANGE_PM_1_V": 
            return 1.0
        elif self.name == "INPUT_RANGE_PM_1_V_25": 
            return 1.25
        elif self.name == "INPUT_RANGE_PM_2_V": 
            return 2.0
        elif self.name == "INPUT_RANGE_PM_2_V_5": 
            return 2.5
        elif self.name == "INPUT_RANGE_PM_4_V": 
            return 4.0
        elif self.name == "INPUT_RANGE_PM_5_V": 
            return 5.0
        elif self.name == "INPUT_RANGE_PM_8_V": 
            return 8.0
        elif self.name == "INPUT_RANGE_PM_10_V": 
            return 10.0
        elif self.name == "INPUT_RANGE_PM_20_V": 
            return 20.0
        elif self.name == "INPUT_RANGE_PM_40_V": 
            return 40.0
        elif self.name == "INPUT_RANGE_PM_16_V": 
            return 16.0
        
    def __str__(self) -> str:
        r = self.to_volts
        if r < 1:
            return f"±{int(r*1000)} mV"
        else:
            return f"±{r} V"


class Capabilities(Enum):
    GET_SERIAL_NUMBER = 0x10000024
    GET_FIRST_CAL_DATE = 0x10000025
    GET_LATEST_CAL_DATE = 0x10000026
    GET_LATEST_TEST_DATE = 0x10000027
    GET_LATEST_CAL_DATE_MONTH = 0x1000002D
    GET_LATEST_CAL_DATE_DAY = 0x1000002E
    GET_LATEST_CAL_DATE_YEAR = 0x1000002F
    GET_BOARD_OPTIONS_LOW = 0x10000037
    GET_BOARD_OPTIONS_HIGH = 0x10000038
    MEMORY_SIZE = 0x1000002A
    ASOPC_TYPE = 0x1000002C
    BOARD_TYPE = 0x1000002B
    GET_PCIE_LINK_SPEED = 0x10000030
    GET_PCIE_LINK_WIDTH = 0x10000031
    GET_MAX_PRETRIGGER_SAMPLES = 0x10000046
    GET_CPF_DEVICE = 0x10000071
    HAS_RECORD_FOOTERS_SUPPORT = 0x10000073
    CAP_SUPPORTS_TRADITIONAL_AUTODMA = 0x10000074
    CAP_SUPPORTS_NPT_AUTODMA = 0x10000075
    CAP_MAX_NPT_PRETRIGGER_SAMPLES = 0x10000076
    CAP_IS_VFIFO_BOARD = 0x10000077
    CAP_SUPPORTS_NATIVE_SINGLE_PORT = 0x10000078
    CAP_SUPPORT_8_BIT_PACKING = 0x10000079
    CAP_SUPPORT_12_BIT_PACKING = 0x10000080


class Couplings(Enum):
    AC_COUPLING = 1
    DC_COUPLING = 2
    GND_COUPLING = 4

    def __str__(self):
        if self.value == 1:
            return "AC"
        elif self.value == 2:
            return "DC"
        else:
            return "Ground"

    @classmethod
    def from_str(cls, coupling_str:str):
        coupling = coupling_str.lower()
        if coupling == "ac":
            return cls.AC_COUPLING
        elif coupling == "dc":
            return cls.DC_COUPLING
        elif coupling == "ground":
            return cls.GND_COUPLING
        else:
            raise ValueError(f"'{coupling_str}' is not a valid Couplings enum string")


class TriggerEngines(Enum):
    TRIG_ENGINE_J = 0
    TRIG_ENGINE_K = 1


class TriggerOperations(Enum):
    TRIG_ENGINE_OP_J = 0
    TRIG_ENGINE_OP_K = 1
    TRIG_ENGINE_OP_J_OR_K = 2
    TRIG_ENGINE_OP_J_AND_K = 3
    TRIG_ENGINE_OP_J_XOR_K = 4
    TRIG_ENGINE_OP_J_AND_NOT_K = 5
    TRIG_ENGINE_OP_NOT_J_AND_K = 6


class TriggerSources(Enum):
    TRIG_CHAN_A = 0x0
    TRIG_CHAN_B = 0x1
    TRIG_EXTERNAL = 0x2
    TRIG_DISABLE = 0x3
    TRIG_CHAN_C = 0x4
    TRIG_CHAN_D = 0x5
    TRIG_CHAN_E = 0x6
    TRIG_CHAN_F = 0x7
    TRIG_CHAN_G = 0x8
    TRIG_CHAN_H = 0x9
    TRIG_CHAN_I = 0xA
    TRIG_CHAN_J = 0xB
    TRIG_CHAN_K = 0xC
    TRIG_CHAN_L = 0xD
    TRIG_CHAN_M = 0xE
    TRIG_CHAN_N = 0xF
    TRIG_CHAN_O = 0x10
    TRIG_CHAN_P = 0x11

    @property
    def channel_index(self):
        if self not in [TriggerSources.TRIG_EXTERNAL, TriggerSources.TRIG_DISABLE]:
            index = self.value
            if index > 3: index -= 2
            return index
        else:
            raise RuntimeError("Trigger source is not an input channel")

    def __str__(self):
        """ Provides a readable version """
        if self.name[5:9] == "CHAN":
            return f"Channel {self.name[-1]}"
        elif self.name[5:] == "EXTERNAL":
            return "External"
        else:
            return "Disable"

    @classmethod
    def from_str(cls, trigger:str):
        trigger_str = trigger.lower()
        if trigger_str[:7] == "channel":
            return cls[f"TRIG_CHAN_{trigger_str[-1].upper()}"]
        elif trigger_str == "external":
            return cls.TRIG_EXTERNAL
        elif trigger_str == "disable":
            return cls.TRIG_DISABLE
        else:
            raise ValueError(f"'{trigger}' is not a valid TriggerSources enum string")


class TriggerSlopes(Enum):
    TRIGGER_SLOPE_POSITIVE = 1
    TRIGGER_SLOPE_NEGATIVE = 2

    def __str__(self):
        if self.value == 1:
            return "Positive"
        else:
            return "Negative"
        
    @classmethod
    def from_str(cls, slope:str):
        slope_str = slope.lower()
        if slope_str == "positive":
            return cls.TRIGGER_SLOPE_POSITIVE
        elif slope_str == "negative":
            return cls.TRIGGER_SLOPE_NEGATIVE
        else:
            raise ValueError(f"'{slope}' is not a valid TriggerSlopes enum string")


class Impedances(Enum):
    IMPEDANCE_1M_OHM = 1
    IMPEDANCE_50_OHM = 2
    IMPEDANCE_75_OHM = 4
    IMPEDANCE_300_OHM = 8

    @classmethod
    def from_ohms(cls, ohms):
        if ohms == 1e6:
            return cls.IMPEDANCE_1M_OHM
        elif ohms == 50:
            return cls.IMPEDANCE_50_OHM
        elif ohms == 75:
            return cls.IMPEDANCE_75_OHM
        elif ohms == 300:
            return cls.IMPEDANCE_300_OHM
        raise ValueError(f"No matching input impedance found for {ohms} ohms")
    
    @classmethod
    def from_str(cls, ohms_str:str):
        ohms = ohms_str.lower()
        if ohms in ["50 ohm", "50 Ω".lower()]:
            return cls.IMPEDANCE_50_OHM
        elif ohms in ["1 mohm", "1 MΩ".lower()]:
            return cls.IMPEDANCE_1M_OHM
        elif ohms in ["75 ohm", "75 Ω".lower()]:
            return cls.IMPEDANCE_75_OHM
        elif ohms == ["300 ohm", "300 Ω".lower()]:
            return cls.IMPEDANCE_300_OHM
        raise ValueError(f"No matching input impedance found for {ohms_str}")
    
    @property
    def in_ohms(self):
        if self.value == 1:
            return int(1e6)
        elif self.value == 2:
            return 50
        if self.value == 4:
            return 75
        if self.value == 8:
            return 300
        
    def __str__(self):
        r = self.in_ohms
        if r == 1e6:
            return f"1 MΩ"
        else:
            return f"{int(r)} Ω"


class ExternalTriggerRanges(Enum):
    ETR_5V = 0
    ETR_1V = 1
    ETR_TTL = 2
    ETR_2V5 = 3

    @property
    def to_volts(self):
        if self.name == "ETR_5V": 
            return 5.0
        elif self.name == "ETR_1V": 
            return 1.0
        elif self.name == "ETR_2V5": 
            return 2.5
        elif self.name == "ETR_TTL": 
            return 5.0 # Not +/-5V in this case, 0V to 5V
        
    def __str__(self):
        if self.name == "ETR_5V": 
            return "±5 V"
        elif self.name == "ETR_1V": 
            return "±1 V"
        elif self.name == "ETR_2V5": 
            return "±2.5 V"
        elif self.name == "ETR_TTL": 
            return "TTL"
        
    @classmethod
    def from_str(cls, external_trigger_range_str:str):
        if external_trigger_range_str == "±5 V": 
            return cls.ETR_5V
        elif external_trigger_range_str == "±1 V": 
            return cls.ETR_1V
        elif external_trigger_range_str == "±2.5 V": 
            return cls.ETR_2V5
        elif external_trigger_range_str == "TTL": 
            return cls.ETR_TTL


class LED(Enum):
    LED_OFF = 0
    LED_ON = 1


class AuxIOModes(Enum):
    AUX_OUT_TRIGGER = 0
    AUX_IN_TRIGGER_ENABLE = 1
    AUX_OUT_PACER = 2
    AUX_IN_AUXILIARY = 13
    AUX_OUT_SERIAL_DATA = 14


class Parameters(Enum):
    DATA_WIDTH = 0x10000009
    SETGET_ASYNC_BUFFSIZE_BYTES = 0x10000039
    SETGET_ASYNC_BUFFCOUNT = 0x10000040
    GET_ASYNC_BUFFERS_PENDING = 0x10000050
    GET_ASYNC_BUFFERS_PENDING_FULL = 0x10000051
    GET_ASYNC_BUFFERS_PENDING_EMPTY = 0x10000052
    SET_DATA_FORMAT = 0x10000041
    GET_DATA_FORMAT = 0x10000042
    GET_SAMPLES_PER_TIMESTAMP_CLOCK = 0x10000044
    GET_RECORDS_CAPTURED = 0x10000045
    ECC_MODE = 0x10000048
    GET_AUX_INPUT_LEVEL = 0x10000049
    GET_CHANNELS_PER_BOARD = 0x10000070
    GET_FPGA_TEMPERATURE = 0x10000080
    PACK_MODE = 0x10000072
    SET_SINGLE_CHANNEL_MODE = 0x10000043
    API_FLAGS = 0x10000090
    SET_SOFTWARE_CAL_MECHANISM = 0x10000100
    API_LOG_CLEAR = 0x10000102
    SETGET_TRIGGER_SKIPPING = 0x10000103
    GET_ADC_TEMPERATURE = 0x10000104
    GET_ONBOARD_MEMORY_USED = 0x10000105


class ECCModes(Enum):
    ECC_DISABLE = 0
    ECC_ENABLE = 1


class AuxInputLevels(Enum):
    AUX_INPUT_LOW = 0
    AUX_INPUT_HIGH = 1


class PackModes(Enum):
    PACK_DEFAULT = 0
    PACK_8_BITS_PER_SAMPLE = 1
    PACK_12_BITS_PER_SAMPLE = 2

    def __str__(self):
        if self.value == 0:
            return "None"
        elif self.value == 1:
            return "8-bit"
        else:
            return "12-bit"
    
    @classmethod
    def from_str(cls, pack:str):
        pack_lower = pack.lower()
        if pack_lower == "none":
            return cls.PACK_DEFAULT
        elif pack_lower == "8-bit":
            return cls.PACK_8_BITS_PER_SAMPLE
        elif pack_lower == "12-bit":
            return cls.PACK_12_BITS_PER_SAMPLE
        else:
            raise ValueError(f"'{pack}' is not a valid PackModes enum string")


class APITraceStates(Enum):
    API_DISABLE_TRACE = 0
    API_ENABLE_TRACE = 0



class HEADER0(Structure):
    # Note: many of these return zero
    _fields_ = [
        ("SerialNumber", c_uint, 18),       # bits 17..0
        ("SystemNumber", c_uint, 4),        # bits 21..18
        ("WhichChannel", c_uint, 1),        # bit 22
        ("BoardNumber", c_uint, 4),         # bits 26..23
        ("SampleResolution", c_uint, 3),    # bits 29..27
        ("DataFormat", c_uint, 2)           # bits 31..30
    ]

class HEADER1(Structure):
    _fields_ = [
        ("RecordNumber", c_uint, 24),       # bits 23..0
        ("BoardType", c_uint, 8)            # bits 31..24
    ]

class HEADER2(Structure):
    _fields_ = [
        ("TimeStampLowPart", c_uint32)      # bits 31..0
    ]

class HEADER3(Structure):
    _fields_ = [
        ("TimeStampHighPart", c_uint, 8),   # bits 7..0
        ("ClockSource", c_uint, 2),         # bits 9..8
        ("ClockEdge", c_uint, 1),           # bit 10
        ("SampleRate", c_uint, 7),          # bits 17..11
        ("InputRange", c_uint, 5),          # bits 22..18
        ("InputCoupling", c_uint, 2),       # bits 24..23
        ("InputImpedance", c_uint, 2),      # bits 26..25
        ("ExternalTriggered", c_uint, 1),   # bit 27
        ("ChannelBTriggered", c_uint, 1),   # bit 28
        ("ChannelATriggered", c_uint, 1),   # bit 29
        ("TimeOutOccurred", c_uint, 1),     # bit 30
        ("ThisChannelTriggered", c_uint, 1) # bit 31
    ]

class AtsHeader(Structure):
    # https://docs.alazartech.com/ats-sdk-user-guide/latest/programmers-guide.html#record-headers-and-timestamps
    _fields_ = [
        ("hdr0", HEADER0),
        ("hdr1", HEADER1),
        ("hdr2", HEADER2),
        ("hdr3", HEADER3)
    ]

    @property
    def record_number(self):
        return self.hdr1.RecordNumber

    @property
    def timestamp(self):
        # Combine TimeStampLowPart and TimeStampHighPart to form the full timestamp
        return (self.hdr2.TimeStampLowPart) + \
               (self.hdr3.TimeStampHighPart << 32) 


class AtsFooter(Structure):
    # https://github.com/alazartech/ats-footers/blob/release/atsfooters/src/atsfooters_internal.hpp
    _fields_ = [
        ('aux_and_pulsar_low', c_uint8),  
        ('pulsar_high', c_uint8),        
        ('tt_low', c_uint16),             
        ('tt_med', c_uint16), 
        ('tt_high', c_uint16),
        ('rn_low', c_uint16), 
        ('rn_high', c_uint16),  
        ('fc_low', c_uint16),
        ('fc_high', c_uint8), 
        ('type', c_uint8) 
    ]

    @property
    def record_number(self):
        # Combine rn_low and rn_high to form the full record number
        return (self.rn_low) + \
               (self.rn_high << 16) 

    @property
    def timestamp(self):
        # Combine tt_low, tt_med, and tt_high to form the full timestamp
        return (self.tt_low) + \
               (self.tt_med << 16) + \
               (self.tt_high << 32)
    
    