from enum import Enum
import ctypes
from ctypes import (byref, POINTER, c_byte, c_char_p, c_uint8, c_uint16, 
                    c_uint32, c_void_p, c_long, c_float)

import numpy as np


class ClockSources(Enum):
    INTERNAL_CLOCK = 0x1
    EXTERNAL_CLOCK = 0x2
    FAST_EXTERNAL_CLOCK = 0x2
    MEDIUM_EXTERNAL_CLOCK = 0x3
    SLOW_EXTERNAL_CLOCK = 0x4
    EXTERNAL_CLOCK_AC = 0x5
    EXTERNAL_CLOCK_DC = 0x6
    EXTERNAL_CLOCK_10MHz_REF = 0x7
    INTERNAL_CLOCK_10MHz_REF = 0x8
    EXTERNAL_CLOCK_10MHz_PXI = 0xA
    INTERNAL_CLOCK_DIV_4 = 0xF
    INTERNAL_CLOCK_DIV_5 = 0x10
    MASTER_CLOCK = 0x11
    INTERNAL_CLOCK_SET_VCO = 0x12


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


class ClockEdges(Enum):
    CLOCK_EDGE_RISING = 0
    CLOCK_EDGE_FALLING = 1


class Channels(Enum):
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


class ADMAModes(Enum):
    ADMA_TRADITIONAL_MODE = 0
    ADMA_NPT = 0x200
    ADMA_CONTINUOUS_MODE = 0x100
    ADMA_TRIGGERED_STREAMING = 0x400
    ADMA_EXTERNAL_STARTCAPTURE = 0x1
    ADMA_ENABLE_RECORD_HEADERS = 0x8
    ADMA_ALLOC_BUFFERS = 0x20
    ADMA_FIFO_ONLY_STREAMING = 0x800
    ADMA_INTERLEAVE_SAMPLES = 0x1000
    ADMA_GET_PROCESSED_DATA = 0x2000
    ADMA_DSP = 0x4000
    ADMA_ENABLE_RECORD_FOOTERS = 0x10000


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


class ExternalTriggerRanges(Enum):
    ETR_5V_50OHM = 0x00000000
    ETR_1V_50OHM = 0x00000001
    ETR_TTL = 0x00000002
    ETR_2V5_50OHM = 0x00000003
    ETR_5V_300OHM = 0x00000004
    ETR_5V = 0
    ETR_1V = 1
    ETR_2V5 = 3


class LED(Enum):
    LED_OFF = 0
    LED_ON = 1


class AuxIOModes(Enum):
    AUX_OUT_TRIGGER = 0
    AUX_IN_TRIGGER_ENABLE = 1
    AUX_OUT_PACER = 2
    AUX_IN_AUXILIARY = 13
    AUX_OUT_SERIAL_DATA = 14


# Load the ATS API
ats = ctypes.CDLL("ATSApi.dll")


# Define error checking function
ats.AlazarErrorToText.restype = c_char_p
ats.AlazarErrorToText.argtypes = [c_uint32]
def check_return_code(res, func, args):
    if res != 512:
        exception_text = f"Error calling wrapper function {func.__name__}, " \
            + f"with arguments {str(args)}: {str(ats.AlazarErrorToText(res))}"
        raise Exception(exception_text)


def ctypes_sig(argtypes, restype=c_uint32, errcheck=check_return_code):
    """
    Automates setting wrapped ctypes function signature fields
    """
    def decorator(func):
        func_name = "Alazar"
        acronyms = ["sdk", "id", "io", "cpld", "fpga", "led"]
        for x in func.__name__.split('_'):
            if x in acronyms: 
                x = x.upper()
            else:
                x = x.capitalize()
            func_name += x
        
        print(func_name)

        ctypes_func = getattr(ats, func_name)
        ctypes_func.restype = restype
        ctypes_func.argtypes = argtypes
        if errcheck is not None:
            ctypes_func.errcheck = errcheck

        # Wrapped function to call the actual ctypes function
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


@ctypes_sig([POINTER(c_byte), POINTER(c_byte), POINTER(c_byte)])
def get_sdk_version() -> tuple[int,int,int]:
    major = c_byte(0)
    minor = c_byte(0)
    revision = c_byte(0)
    ats.AlazarGetSDKVersion(byref(major), byref(minor), byref(revision))
    return (major.value, minor.value, revision.value)


@ctypes_sig([POINTER(c_byte), POINTER(c_byte), POINTER(c_byte)])
def get_driver_version() -> tuple[int,int,int]:
    major = c_byte(0)
    minor = c_byte(0)
    revision = c_byte(0)
    ats.AlazarGetDriverVersion(byref(major), byref(minor), byref(revision))
    return (major.value, minor.value, revision.value)


@ctypes_sig([], errcheck=None)
def num_of_systems() -> int:
    return ats.AlazarNumOfSystems()


@ctypes_sig([c_uint32], errcheck=None)
def boards_in_system_by_system_id(sid:int) -> int:
    return ats.AlazarBoardsInSystemBySystemID(sid)


@ctypes_sig([c_uint32, c_uint32], restype=c_void_p, errcheck=None)
def get_board_by_system_id(system_id, board_id):
    return ats.AlazarGetBoardBySystemID(system_id, board_id)


@ctypes_sig([c_void_p, c_uint32], restype=c_void_p)
def alloc_buffer_u8(board_handle, size_bytes):
    return ats.AlazarAllocBufferU8(board_handle, size_bytes)


@ctypes_sig([c_void_p, c_uint32], restype=c_void_p)
def alloc_buffer_u16(board_handle, size_bytes):
    return ats.AlazarAllocBufferU16(board_handle, size_bytes)


@ctypes_sig([c_void_p, c_void_p])
def free_buffer_u8(board_handle, address):
    return ats.AlazarFreeBufferU8(board_handle, address)


@ctypes_sig([c_void_p, c_void_p])
def free_buffer_u16(board_handle, address):
    return ats.AlazarFreeBufferU16(board_handle, address)


class Buffer:
    """
    Buffer for AutoDMA transfers.
    """
    def __init__(self, board:'Board', bytes_per_sample:int, size_bytes:int):
        self.size_bytes = size_bytes
        self.bytes_per_sample = bytes_per_sample
        self._board_handle = board._handle

        self._addr = None
        if self.bytes_per_sample == 1:
            self._addr = alloc_buffer_u8(self._board_handle, size_bytes)
            c_sample_type = c_uint8
            np_dtype = np.uint8
        elif self.bytes_per_sample == 2:
            self._addr = alloc_buffer_u16(self._board_handle, size_bytes)
            c_sample_type = c_uint16
            np_dtype = np.uint16
        else:
            raise ValueError("Invalid buffer data type")

        if self._addr is None:
            raise ValueError("Error allocating buffer")

        ctypes_array = (
            c_sample_type * (size_bytes // bytes_per_sample)
        ).from_address(self._addr)
        
        self.buffer = np.frombuffer(ctypes_array, dtype=np_dtype)
        
        # hold a reference to this array or else it will be garbage collected
        self.ctypes_buffer = ctypes_array

    def __del__(self):
        if self.bytes_per_sample == 1:
            free_buffer_u8(self._board_handle, self._addr)
        elif self.bytes_per_sample == 2:
            free_buffer_u16(self._board_handle, self._addr)


class Board:
    def __init__(self, system_id=1, board_id=1):
        self._sid = system_id
        self._bid = board_id

        self._handle = get_board_by_system_id(self._sid, self._bid)
        if self._handle == 0:
            raise Exception(f"Board {self._sid}.{self._bid} not found")

    @ctypes_sig([c_void_p])
    def abort_async_read(self):
        """
        Aborts a dual-port acquisition, and any in-process DMA transfers. 
        """
        ats.AlazarAbortAsyncRead(self._handle)

    @ctypes_sig([c_void_p, c_uint32, c_long, c_uint32, c_uint32, c_uint32, 
                 c_uint32])
    def before_async_read(self, channels, transfer_offset, samples_per_record,
                          records_per_buffer, records_per_acquisition, flags):
        """
        Configure board to make an asynchronous AutoDMA acquisition. 
        """
        ats.AlazarBeforeAsyncRead(self._handle, channels, transfer_offset, 
                                  samples_per_record, records_per_buffer, 
                                  records_per_acquisition, flags)

    @ctypes_sig([c_void_p], errcheck=None)
    def busy(self):
        """
        Determines if an acquisition is in progress. 
        """
        return ats.AlazarBusy(self._handle) > 0

    @ctypes_sig([c_void_p, c_uint32, c_uint32])
    def configure_aux_io(self, mode, parameter):
        """
        Configures the AUX I/O connector as an input or output signal.
        """
        ats.AlazarConfigureAuxIO(self._handle, mode, parameter)
    
    @ctypes_sig([c_void_p], errcheck=None)
    def get_board_kind(self):
        """
        Get a board kind (model number) of the digitizer board.
        """
        return BoardKind(ats.AlazarGetBoardKind(self._handle))

    @ctypes_sig([c_void_p, POINTER(c_byte), POINTER(c_byte)])
    def get_board_revision(self):
        """
        Get the PCB hardware revision level of the digitizer board. 
        """
        major = c_byte(0)
        minor = c_byte(0)
        ats.AlazarGetBoardRevision(self._handle, byref(major), byref(minor))
        return (major.value, minor.value)

    @ctypes_sig([c_void_p, POINTER(c_byte), POINTER(c_byte)])
    def get_cpld_version(self):
        major = c_byte(0)
        minor = c_byte(0)
        ats.AlazarGetCPLDVersion(self._handle, byref(major), byref(minor))
        return (major.value, minor.value)
		
    @ctypes_sig([c_void_p, POINTER(c_byte), POINTER(c_byte)])
    def get_fpga_version(self):
        major = c_byte(0)
        minor = c_byte(0)
        ats.AlazarGetFPGAVersion(self._handle, byref(major), byref(minor))
        return (major.value, minor.value)

    @ctypes_sig([c_void_p, c_uint32, c_uint32, c_uint32, c_uint32])
    def input_control_ex(self, channel, coupling, input_range, impedance):
        """
        Select the input coupling, range and impedance of a digitizer channel. 
        """
        ats.AlazarInputControlEx(self._handle, channel, coupling, input_range, 
                                 impedance)

    @ctypes_sig([c_void_p, c_void_p, c_uint32])
    def post_async_buffer(self, buffer, bufferLength):
        """
        Posts a DMA buffer to a board.
        """
        ats.AlazarPostAsyncBuffer(self._handle, buffer, bufferLength)

    @ctypes_sig([c_void_p, c_uint32, c_uint32, POINTER(c_uint32)])
    def query_capability(self, capability:Capabilities):
        """
        Get a device attribute as an unsigned 32-bit integer. 
        """
        reserved = c_uint32(0)
        retval = c_uint32(0)
        ats.AlazarQueryCapability(self._handle, capability.value, reserved, byref(retval))
        return retval.value

    @ctypes_sig([c_void_p, c_uint32, c_uint32, c_uint32, c_uint32])
    def set_capture_clock(self, source, rate, edge, decimation):
        """
        Configure the sample clock source, edge and decimation. 
        """
        rate = int(rate)
        ats.AlazarSetCaptureClock(self._handle, source, rate, edge, decimation)

    @ctypes_sig([c_void_p, c_float])
    def set_external_clock_level(self, level_percent:float):
        """
        Set the external clock comparator level. 
        """
        ats.AlazarSetExternalClockLevel(self._handle, level_percent)

    @ctypes_sig([c_void_p, c_uint32, c_uint32])
    def set_external_trigger(self, coupling, range):
        """
        Set the external trigger range and coupling. 
        """
        ats.AlazarSetExternalTrigger(self._handle, coupling, range)

    @ctypes_sig([c_void_p, c_uint32])
    def set_led(self, led_state:LED):
        """
        Control the LED on the board mounting bracket. 
        """
        ats.AlazarSetLED(self._handle, led_state.value)

    @ctypes_sig([c_void_p, c_uint32, c_uint32])
    def set_record_size(self, pre_trigger_samples, post_trigger_samples):
        """
        Set the number of pre-trigger and post-trigger samples per record. 
        """
        ats.AlazarSetRecordSize(self._handle, pre_trigger_samples, 
                                post_trigger_samples)

    @ctypes_sig([c_void_p, c_uint32])
    def set_trigger_delay(self, delay_samples):
        """
        Set the time, in sample clocks, to wait after receiving a trigger 
        event before capturing a record for the trigger. 
        """
        ats.AlazarSetTriggerDelay(self._handle, delay_samples)

    @ctypes_sig([c_void_p, c_uint32, 
                 c_uint32, c_uint32, c_uint32, c_uint32,
                 c_uint32, c_uint32, c_uint32, c_uint32])        
    def set_trigger_operation(self, operation,
                              engine1, source1, slope1, level1,
                              engine2, source2, slope2, level2):
        """
        Configures the trigger system. 
        """
        ats.AlazarSetTriggerOperation(
            self._handle, operation,
            engine1, source1, slope1, level1,
            engine2, source2, slope2, level2
        )
            
    @ctypes_sig([c_void_p, c_uint32])
    def set_trigger_time_out(self, timeout_ticks):
        """
        Set the time to wait for a trigger event before automatically 
        generating a trigger event. 
        """
        ats.AlazarSetTriggerTimeOut(self._handle, timeout_ticks)

    @ctypes_sig([c_void_p])
    def start_capture(self):
        '''Starts the acquisition.'''
        ats.AlazarStartCapture(self._handle)

    @ctypes_sig([c_void_p, c_void_p, c_uint32])
    def wait_async_buffer_complete(self, buffer, timeout_ms):
        """
        This function returns when a board has received sufficient triggers 
        to fill the specified buffer, or when the timeout internal elapses. 
        """
        ats.AlazarWaitAsyncBufferComplete(self._handle, buffer, timeout_ms)