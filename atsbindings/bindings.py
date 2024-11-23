from pathlib import Path
import tomllib
import re
import ctypes
from functools import cached_property
from ctypes import (byref, POINTER, c_byte, c_char_p, c_uint8, c_uint16, 
                    c_uint32, c_void_p, c_long, c_float, cast, create_string_buffer,
                    sizeof)

import numpy as np

from .enumerations import *


class Frequency(float):
    """Subclass of float to allow automatic string formatting."""
    def __new__(cls, value):
        return super().__new__(cls, value)
    
    def __str__(self):
        if self >= 1e6:
            return f"{self/1e6:.1f} MHz"
        elif self >= 1e3:
            return f"{self/1e3:.1f} kHz"
        else:
            return f"{self:.1f} Hz"


class ExternalClockFrequencyRange:
    """Class to maintain min and max frequencies, i.e. a frequency range"""
    def __init__(self, min_hz, max_hz):
        self.min = Frequency(min_hz)
        self.max = Frequency(max_hz)


class BoardSpecificInfo:
    """Class to maintain board-specific information. When possible API enumerations are stored/returned."""
    def __init__(self, board_kind):
        if hasattr(board_kind, "name"):
            board_kind = board_kind.name

        # Open and read the TOML file
        fn = Path(__file__).parent / "board_specific_info.toml"
        with open(fn, "rb") as f:
            bsi = tomllib.load(f)

        self.channels:int = bsi[board_kind]["channels"]
        self._set_input_ranges(bsi[board_kind]["input_ranges"]) # available input range depends on input impedance, so this property is more complicated
        self.input_couplings:list[Couplings] = bsi[board_kind["input_coupling"]]
        self.data_packings:list[PackModes] = bsi[board_kind["data_packing"]]
        self.configure_lsb:bool = bsi[board_kind["configure_lsb"]]
        self.min_record_size:int = bsi[board_kind]["min_record_size"]
        self.pretrig_alignment:int = bsi[board_kind]["pretrig_alignment"]
        self.record_resolution:int = bsi[board_kind]["record_resolution"]
        self.max_npt_pretrig_length:int = bsi[board_kind]["max_npt_pretrig_length"]
        self._samples_per_timestamp:dict = bsi[board_kind]["samples_per_timestamp"]
        self._channel_configs:list = bsi[board_kind]["channel_configs"]
        self.sample_rates:list[SampleRates] = bsi[board_kind]["sample_rates"]
        self.bandwidth_limit:bool = bsi[board_kind["bandwidth_limit"]]
        self.external_trigger_ranges:list = bsi[board_kind]["external_trigger_levels"]
        self._set_external_clock_frequency_ranges(bsi[board_kind]["external_clock_frequency_limits"])

    def _set_input_ranges(self, input_impedance_ranges_dict:dict):
        self._input_impedances_ranges = {}
        for key in input_impedance_ranges_dict.keys():
            v,u = re.findall(r"(\d+)(ohm|Mohm)", key)[0]
            v = int(v)
            if u == "Mohm":
                v *= 1e6
            impedance = Impedances.from_ohms(v)

            ranges = []
            for r in input_impedance_ranges_dict[key]:
                v,u = re.findall(r"±(\d+)(mV|V)", r)[0]
                if u == "mV":
                    ranges.append(InputRanges.from_v(float(v)*1e-3))
                elif u == "V":
                    ranges.append(InputRanges.from_v(float(v)))
            self._input_impedances_ranges.update({impedance: ranges})
    
    @property
    def input_impedances(self):
        """Returns a list of the available input impedances."""
        return list(self._input_impedances_ranges.keys())
    
    def input_ranges(self, impedance:Impedances) -> list[InputRanges]:
        """Returns list of input ranges for the given input impedance."""
        return self._input_impedances_ranges[impedance]
    
    @property
    def input_couplings(self):
        return self._input_couplings
    
    @input_couplings.setter
    def input_couplings(self, coupling_strs:list[str]):
        self._input_couplings = []
        coupling_strs = [s.lower() for s in coupling_strs]
        if "ac" in coupling_strs:
            self._input_couplings.append(Couplings.AC_COUPLING)
        if "dc" in coupling_strs:
            self._input_couplings.append(Couplings.DC_COUPLING)
        if "ground" in coupling_strs:
            self._input_couplings.append(Couplings.GND_COUPLING)

    @property
    def data_packings(self):
        return self._data_packings
    
    @data_packings.setter
    def data_packings(self, packing_strs:list[str]):
        self._data_packings = [PackModes.PACK_DEFAULT]
        packing_strs = [s.lower() for s in packing_strs]
        if "8-bit" in packing_strs:
            self._input_couplings.append(PackModes.PACK_8_BITS_PER_SAMPLE)
        if "12-bit" in packing_strs:
            self._input_couplings.append(PackModes.PACK_12_BITS_PER_SAMPLE)

    def samples_per_timestamp(self, active_channels:int):
        """Returns the number of sample clock periods per timestamp increment. Depends on the number of active channels"""
        if active_channels == 1:
            chan_str = "1channel"
        else:
            chan_str = str(active_channels) + "channels"
        return self._samples_per_timestamp[chan_str]
    
    @property
    def channel_configs(self):
        code_values = []
        for config in self._channel_configs:
            code_value = 0
            for i,b in enumerate(config):
                code_value += 2**i*int(b)
            code_values.append(code_value)
        return code_values

    @property
    def sample_rates(self):
        return self._sample_rates
    
    @sample_rates.setter
    def sample_rates(self, rates):
        self._sample_rates = []
        for rate in rates:
            v,u = re.findall(r"(\d+)(kS/s|MS/s)", rate)[0]
            if u == "kS/s":
                self._sample_rates.append(SampleRates.from_hertz(float(v)*1e3))
            elif u == "MS/s":
                self._sample_rates.append(SampleRates.from_hertz(float(v)*1e6))
    
    @property
    def external_trigger_ranges(self):
        return self._external_trigger_ranges
    
    @external_trigger_ranges.setter
    def external_trigger_ranges(self, ranges):
        self._external_trigger_ranges = []
        for etl in ranges:
            if etl == "5 V":
                self._external_trigger_ranges.append(ExternalTriggerRanges.ETR_5V)
            elif etl == "1 V":
                self._external_trigger_ranges.append(ExternalTriggerRanges.ETR_1V)
            if etl == "TTL":
                self._external_trigger_ranges.append(ExternalTriggerRanges.ETR_TTL)
            if etl == "2.5 V":
                self._external_trigger_ranges.append(ExternalTriggerRanges.ETR_2V5)
    
    def _set_external_clock_frequency_ranges(self, clock_ranges):
        clocks = clock_ranges.keys()
        self._external_clock_frequency_ranges = {}
        for clock in clocks:
            range = ExternalClockFrequencyRange(clock_ranges[clock][0], clock_ranges[clock][1])

            if clock == "Fast":
                clock = ClockSources.FAST_EXTERNAL_CLOCK
            elif clock == "Medium":
                clock = ClockSources.MEDIUM_EXTERNAL_CLOCK
            elif clock == "Slow":
                clock = ClockSources.SLOW_EXTERNAL_CLOCK
            elif clock == "AC":
                clock = ClockSources.EXTERNAL_CLOCK_AC
            elif clock == "DC":
                clock = ClockSources.EXTERNAL_CLOCK_DC

            self._external_clock_frequency_ranges.update({clock : range})

    @property
    def supported_clocks(self) -> list[ClockSources]:
        clocks = [ClockSources.INTERNAL_CLOCK]
        for clock in list(self._external_clock_frequency_ranges.keys()):
            if clock == "Fast":
                clocks.append(ClockSources.FAST_EXTERNAL_CLOCK)
            elif clock == "Medium":
                clocks.append(ClockSources.MEDIUM_EXTERNAL_CLOCK)
            elif clock == "Slow":
                clocks.append(ClockSources.SLOW_EXTERNAL_CLOCK)
            elif clock == "AC":
                clocks.append(ClockSources.EXTERNAL_CLOCK_AC)
            elif clock == "DC":
                clocks.append(ClockSources.EXTERNAL_CLOCK_DC)
        return clocks
    
    @property
    def supported_trigger_sources(self) -> list[TriggerSources]:
        """Returns the valid trigger sources for this board. """
        trigger_sources = [
            TriggerSources.TRIG_CHAN_A,
            TriggerSources.TRIG_CHAN_B,
            TriggerSources.TRIG_EXTERNAL,
            TriggerSources.TRIG_DISABLE
        ]
        for i in range(self.channels - 2):
            trigger_sources.append(TriggerSources[f"TRIG_CHAN_{chr(ord('C') + i)}"])
        return trigger_sources
        
    def external_clock_frequency_ranges(self, clock_source:ClockSources):
        return self._external_clock_frequency_ranges[clock_source]


# Load the API DLL
try:
    ats = ctypes.CDLL("ATSApi.dll")
except OSError as e:
    raise RuntimeError(f"Could not find 'ATSApi.dll'. Check whether Alazar software is properly installed.")


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

class System:
    """
    Object to provide methods to system parameters.
    """
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
def _get_board_by_system_id(system_id, board_id):
    return ats.AlazarGetBoardBySystemID(system_id, board_id)


@ctypes_sig([c_void_p, c_uint32], restype=c_void_p, errcheck=None)
def _alloc_buffer_u8(board_handle, size_bytes):
    return ats.AlazarAllocBufferU8(board_handle, size_bytes)


@ctypes_sig([c_void_p, c_uint32], restype=c_void_p, errcheck=None)
def _alloc_buffer_u16(board_handle, size_bytes):
    return ats.AlazarAllocBufferU16(board_handle, size_bytes)


@ctypes_sig([c_void_p, c_void_p])
def _free_buffer_u8(board_handle, address):
    return ats.AlazarFreeBufferU8(board_handle, address)


@ctypes_sig([c_void_p, c_void_p])
def _free_buffer_u16(board_handle, address):
    return ats.AlazarFreeBufferU16(board_handle, address)
    

class Buffer:
    def __init__(self, board:'Board', channels:int,
                 records_per_buffer:int, samples_per_record:int, 
                 include_header:bool=False, include_footer:bool=False,
                 interleave_samples:bool=False,
                 data_packing=PackModes.PACK_DEFAULT):
        self._board = board
        self.channels = channels
        self.records_per_buffer = records_per_buffer
        self.samples_per_record = samples_per_record
        if include_header and include_footer:
            raise ValueError("Can not include both header and footer")
        self.include_header = include_header # header increases record size
        self.include_footer = include_footer # footers replace data at end of record
        self.interleave_samples = interleave_samples
        self.data_packing = data_packing

        # When interleaved, API returns 2 channels of headers, max
        nheaders = min(channels,2) if interleave_samples else channels

        size_per_record = int(
            channels * self.bytes_per_sample * samples_per_record 
            + self.header_size * nheaders
        )
        size = size_per_record * records_per_buffer
            
        self.address = None
        if self.bytes_per_sample == 1:
            self.address = _alloc_buffer_u8(self._bhandle, size)
            c_sample_type = c_uint8
            np_dtype = np.uint8
        elif self.bytes_per_sample == 2:
            self.address = _alloc_buffer_u16(self._bhandle, size)
            c_sample_type = c_uint16
            np_dtype = np.uint16
        elif self.bytes_per_sample == 1.5:   # 12-bit packing mode
            self.address = _alloc_buffer_u8(self._bhandle, size)
            c_sample_type = c_uint8
            np_dtype = np.uint8
        else:
            raise ValueError("Invalid buffer data type")

        if self.address is None:
            raise ValueError("Error allocating buffer")
        
        ctypes_array = (
            c_sample_type * (size // int(self.bytes_per_sample))
        ).from_address(self.address)
        
        self.buffer = np.frombuffer(ctypes_array, dtype=np_dtype)
        self.buffer.shape = (records_per_buffer, size_per_record//int(self.bytes_per_sample))

        self._ctypes_buffer = ctypes_array # hold ref to avoid GC

    def __del__(self):
        if self.bytes_per_sample == 1:
            _free_buffer_u8(self._bhandle, self.address)
        elif self.bytes_per_sample == 2:
            _free_buffer_u16(self._bhandle, self.address)

    @cached_property
    def size(self):
        """Returns the buffer size, including headers, in bytes"""
        return sizeof(self._ctypes_buffer)

    @property
    def _bhandle(self):
        return self._board._handle

    @cached_property
    def bytes_per_sample(self):
        if self.data_packing == PackModes.PACK_8_BITS_PER_SAMPLE:
            bytes_per_sample = 1
        elif self.data_packing == PackModes.PACK_12_BITS_PER_SAMPLE:
            bytes_per_sample = 1.5
        else:
            _, bits_per_sample = self._board.get_channel_info()
            bytes_per_sample = (bits_per_sample + 7)//8
        return bytes_per_sample
    
    @cached_property
    def header_size(self):
        """Returns 16 when headers are enable, 0 otherwise."""
        return 16 if self.include_header else 0
    
    @cached_property
    def footer_size(self):
        """Returns 16 when footers are enable, 0 otherwise."""
        return 16 if self.include_footer else 0
    
    def get_headers(self) -> list[AtsHeader]:
        """Returns the ALAZAR_HEADER object from the first 16 bytes of the buffer."""
        if not self.include_header:
            return None

        # Retrieve only the header associated with the first channel (2nd channel header is mostly redundant)
        headers_bytes = [hb.tobytes() for hb in self.buffer[:, :16//self.bytes_per_sample]]

        # Create a buffer and copy the data into it
        buffers = [create_string_buffer(hb, 16) for hb in headers_bytes]
        
        # Cast and return dereferenced header structures
        return [cast(b, POINTER(AtsHeader)).contents for b in buffers]
    
    def get_footers(self) -> list[AtsFooter]:
        if not self.include_footer:
            return None

        footer_data = self.buffer[:, (-16//self.bytes_per_sample):]
        if self.interleave_samples: 
            footer_data = footer_data[:, [0, 2, 4, 6, 1, 3, 5, 7]]
        footer_bytes = [fb.tobytes() for fb in footer_data]
        buffers = [create_string_buffer(hb, 16) for hb in footer_bytes]
        return [cast(b, POINTER(AtsFooter)).contents for b in buffers]
    
    def get_data(self):
        """Returns a copy of the buffer data, omitting headers or footers."""
        if self.interleave_samples:
            # Data order: [Records][Timepoints][Channels] (both headers, max 2, precede sample data)
            header_offset = self.header_size * min(self.channels,2) \
                // int(self.bytes_per_sample)
            footer_offset = self.footer_size // int(self.bytes_per_sample) 
            
            if self.data_packing == PackModes.PACK_12_BITS_PER_SAMPLE:
                # No footers for 12-bit packing mode
                data = np.array(self.buffer[:, header_offset:], dtype=np.uint16)
                data.shape = (128, -1, 3)
                unpacked0 = data[:,:,[0]] | ((data[:,:,[1]] & 0x0F) << 8)
                unpacked1 = (data[:,:,[1]] >> 4) | (data[:,:,[2]] << 4)
                data = np.concatenate((unpacked0,unpacked1),2)
                data.shape = (
                    self.records_per_buffer, 
                    self.samples_per_record, 
                    self.channels
                )
            else:
                data = np.array(self.buffer[:, header_offset:-footer_offset or None])
                data.shape = (
                    self.records_per_buffer, 
                    self.samples_per_record - footer_offset//self.channels, 
                    self.channels
                )
        else:
            # Data order: [Records][Channels][Timepoints]
            header_offset = self.header_size // self.bytes_per_sample
            footer_offset = self.footer_size // self.bytes_per_sample \
                // self.channels
            samples_per_record_minus_footer = self.samples_per_record - footer_offset
            data = np.empty(
                shape=(self.records_per_buffer, self.channels, samples_per_record_minus_footer)
            )
            for c in range(self.channels):
                data[:,c,:] = self.buffer[
                    :, 
                    c*samples_per_record_minus_footer + (c+1)*header_offset: (c+1)*samples_per_record_minus_footer + (c+1)*header_offset
                ]
        return data


class Board:
    def __init__(self, system_id=1, board_id=1):
        self._sid = system_id
        self._bid = board_id

        self._handle = _get_board_by_system_id(self._sid, self._bid)
        if self._handle == 0:
            raise Exception(f"Board {self._sid}.{self._bid} not found")
        
        self.bsi = BoardSpecificInfo(self.get_board_kind())

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
        0x7FFFFFFF codes for unlimited records per acquisition.
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
    def configure_aux_io(self, mode:AuxIOModes, parameter):
        """
        Configures the AUX I/O connector as an input or output signal.
        """
        ats.AlazarConfigureAuxIO(self._handle, mode.value, parameter)
    
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
    
    @ctypes_sig([c_void_p, c_void_p, c_void_p])
    def get_channel_info(self):
        '''Get the on-board memory in samples per channe and sample size in bits per sample'''
        memory_size = c_uint32(0)
        bits_per_sample = c_uint8(0)
        ats.AlazarGetChannelInfo(self._handle, byref(memory_size), byref(bits_per_sample))
        return (memory_size.value, bits_per_sample.value)

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
    
    @ctypes_sig([c_void_p, c_uint8, ])
    def get_parameter(self, channel:Channels, parameter:Parameters):
        """
        Get a device parameter.
        """
        parameter_value = c_long(-1)
        ats.AlazarGetParameter(self._handle, channel, parameter.value, byref(parameter_value))
        return parameter_value.value

    @ctypes_sig([c_void_p, c_uint32, c_uint32, c_uint32, c_uint32])
    def input_control_ex(self, channel:Channels, coupling:Couplings, 
                         input_range:InputRanges, impedance:Impedances):
        """
        Select the input coupling, range and impedance of a digitizer channel. 
        """
        ats.AlazarInputControlEx(self._handle, channel.value, coupling.value, 
                                 input_range.value, impedance.value)

    @ctypes_sig([c_void_p, c_void_p, c_uint32])
    def post_async_buffer(self, buffer, buffer_length):
        """
        Posts a DMA buffer to a board. 
        
        Parameters: buffer (address to buffer), buffer_length (buffer size)
        """
        ats.AlazarPostAsyncBuffer(self._handle, buffer, buffer_length)

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
    def set_capture_clock(self, source:ClockSources, rate:SampleRates, 
                          edge=ClockEdges.CLOCK_EDGE_RISING, decimation=0):
        """
        Configure the sample clock source, edge and decimation. 
        """
        eclks = [
            ClockSources.FAST_EXTERNAL_CLOCK, 
            ClockSources.MEDIUM_EXTERNAL_CLOCK, 
            ClockSources.SLOW_EXTERNAL_CLOCK,
            ClockSources.EXTERNAL_CLOCK_AC,
            ClockSources.EXTERNAL_CLOCK_DC
        ]
        if source in eclks:
            rate = SampleRates.SAMPLE_RATE_USER_DEF
        ats.AlazarSetCaptureClock(self._handle, source.value, rate.value, edge.value, decimation)

    @ctypes_sig([c_void_p, c_float])
    def set_external_clock_level(self, level_percent:float):
        """
        Set the external clock comparator level. 
        """
        ats.AlazarSetExternalClockLevel(self._handle, level_percent)

    @ctypes_sig([c_void_p, c_uint32, c_uint32])
    def set_external_trigger(self, coupling:Couplings, range:ExternalTriggerRanges):
        """
        Set the external trigger range and coupling. 
        """
        ats.AlazarSetExternalTrigger(self._handle, coupling.value, range.value)

    @ctypes_sig([c_void_p, c_uint32])
    def set_led(self, led_state:LED):
        """
        Control the LED on the board mounting bracket. 
        """
        ats.AlazarSetLED(self._handle, led_state.value)

    @ctypes_sig([c_void_p, c_uint8, c_uint32, c_long])
    def set_parameter(self, channel, parameter:Parameters, value):
        """
        Set a device parameter.
        """
        ats.AlazarSetParameter(self._handle, channel, parameter.value, value.value)

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
    def set_trigger_operation(self, operation:TriggerOperations,
                              engine1:TriggerEngines, source1:TriggerSources,
                              slope1:TriggerSlopes, level1:int,
                              engine2:TriggerEngines, source2:TriggerSources, 
                              slope2:TriggerSlopes, level2:int):
        """
        Configures the trigger system. 
        """
        ats.AlazarSetTriggerOperation(
            self._handle, operation.value,
            engine1.value, source1.value, slope1.value, level1,
            engine2.value, source2.value, slope2.value, level2
        )
            
    @ctypes_sig([c_void_p, c_uint32])
    def set_trigger_time_out(self, timeout_ticks):
        """
        Set the time in ticks (10 us) to wait for a trigger event before 
        automatically generating a trigger event. Enter 0 to wait forever.
        """
        ats.AlazarSetTriggerTimeOut(self._handle, timeout_ticks)

    @ctypes_sig([c_void_p])
    def start_capture(self):
        '''Starts the acquisition.'''
        ats.AlazarStartCapture(self._handle)

    @ctypes_sig([c_void_p, c_void_p, c_uint32])
    def wait_async_buffer_complete(self, buffer, timeout_ms=10_000):
        """
        This function returns when a board has received sufficient triggers 
        to fill the specified buffer, or when the timeout internal elapses. 
        """
        ats.AlazarWaitAsyncBufferComplete(self._handle, buffer, timeout_ms)