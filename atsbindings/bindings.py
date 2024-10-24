import ctypes
from ctypes import (byref, POINTER, c_byte, c_char_p, c_uint8, c_uint16, 
                    c_uint32, c_void_p, c_long, c_float)

import numpy as np

from atsbindings.enumerations import *
from atsbindings.board_specific_info import BoardSpecificInfo



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