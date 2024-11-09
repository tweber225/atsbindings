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


class SampleRates(Enum):
    SAMPLE_RATE_1KSPS = 0x1
    SAMPLE_RATE_2KSPS = 0x2
    SAMPLE_RATE_5KSPS = 0x5
    SAMPLE_RATE_10KSPS = 0x8
    SAMPLE_RATE_20KSPS = 0xA
    SAMPLE_RATE_50KSPS = 0xC
    SAMPLE_RATE_100KSPS = 0xE
    SAMPLE_RATE_200KSPS = 0x10
    SAMPLE_RATE_500KSPS = 0x12
    SAMPLE_RATE_1MSPS = 0x14
    SAMPLE_RATE_2MSPS = 0x18
    SAMPLE_RATE_5MSPS = 0x1A
    SAMPLE_RATE_10MSPS = 0x1C
    SAMPLE_RATE_20MSPS = 0x1E
    SAMPLE_RATE_25MSPS = 0x21
    SAMPLE_RATE_50MSPS = 0x22
    SAMPLE_RATE_100MSPS = 0x24
    SAMPLE_RATE_125MSPS = 0x25
    SAMPLE_RATE_160MSPS = 0x26
    SAMPLE_RATE_180MSPS = 0x27
    SAMPLE_RATE_200MSPS = 0x28
    SAMPLE_RATE_250MSPS = 0x2B
    SAMPLE_RATE_400MSPS = 0x2D
    SAMPLE_RATE_500MSPS = 0x30
    SAMPLE_RATE_800MSPS = 0x32
    SAMPLE_RATE_1000MSPS = 0x35
    SAMPLE_RATE_1200MSPS = 0x37
    SAMPLE_RATE_1500MSPS = 0x3A
    SAMPLE_RATE_1600MSPS = 0x3B
    SAMPLE_RATE_1800MSPS = 0x3D
    SAMPLE_RATE_2000MSPS = 0x3F
    SAMPLE_RATE_2400MSPS = 0x6A
    SAMPLE_RATE_3000MSPS = 0x75
    SAMPLE_RATE_3600MSPS = 0x7B
    SAMPLE_RATE_4000MSPS = 0x80
    SAMPLE_RATE_USER_DEF = 0x40

    # Class method to find the enum by Hz value
    @classmethod
    def from_hz(cls, hz):
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
    
    @property
    def in_hz(self):
        rate = self.name[12:]
        if rate[-4:] == "KSPS":
            return int(float(rate[:-4])*1e3)
        elif rate[-4:] == "MSPS":
            return int(float(rate[:-4])*1e6)
        
    def __str__(self) -> str:
        h = self.in_hz
        if h < 1e6:
            return f"{int(h/1000)} kS/s"
        elif h < 1e9:
            return f"{int(h/1000000)} MS/s"
        else:
            return f"{h/1000000000:.1f} GS/s"
        

class ClockEdges(Enum):
    CLOCK_EDGE_RISING = 0
    CLOCK_EDGE_FALLING = 1


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
    
    @property
    def in_v(self):
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
        r = self.in_v
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


class TriggerSlopes(Enum):
    TRIGGER_SLOPE_POSITIVE = 1
    TRIGGER_SLOPE_NEGATIVE = 2


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
        if ohms == 75:
            return cls.IMPEDANCE_75_OHM
        if ohms == 300:
            return cls.IMPEDANCE_300_OHM
        raise ValueError(f"No matching input impedance found for {ohms} ohms")
    
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
            return f"1 Mohm"
        else:
            return f"{int(r)} ohm"


class ExternalTriggerRanges(Enum):
    ETR_5V = 0
    ETR_1V = 1
    ETR_TTL = 2
    ETR_2V5 = 3
    ETR_5V_300OHM = 4  
    

class LED(Enum):
    LED_OFF = 0
    LED_ON = 1


class AuxIOModes(Enum):
    AUX_OUT_TRIGGER = 0
    AUX_IN_TRIGGER_ENABLE = 1
    AUX_OUT_PACER = 2
    AUX_IN_AUXILIARY = 13
    AUX_OUT_SERIAL_DATA = 14


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
    
    