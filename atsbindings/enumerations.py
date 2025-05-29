from enum import Enum, IntEnum
from ctypes import Structure, c_uint32, c_uint16, c_uint8, c_uint


"""
This module provides enumerations and helper functions for interacting with the
ATS API. These classes enable intuitive interactions with the API, including 
translating between human-readable formats and API-compatible formats.

Classes:
    - ClockSources: Enumerates clock source options for configuring the acquisition clock.
    - SampleRates: Enumerates sample rates for acquisition, with methods to convert between human-readable formats and API values.
    - ClockEdges: Enumerates clock edge configurations (rising or falling).
    - Channels: Enumerates supported input channels for the digitizer.
    - ADMAModes: Enumerates supported AutoDMA modes for data transfer.
    - ADMAFlags: Enumerates additional AutoDMA configuration flags.
    - AuxInputLevels: Enumerates auxiliary input levels.
    - BoardKind: Enumerates supported AlazarTech board types.
    - BoardOptionsLow, BoardOptionsHigh: Enumerates board options (lower/upper 32-bit parts).
    - InputRanges: Enumerates input voltage ranges for configuring channel inputs.
    - Capabilities: Enumerates device capabilities supported by the board.
    - Couplings: Enumerates input coupling configurations (AC, DC, Ground).
    - TriggerEngines: Enumerates supported trigger engines.
    - TriggerOperations: Enumerates operations for combining trigger engines.
    - TriggerSources: Enumerates supported trigger sources.
    - TriggerSlopes: Enumerates trigger slopes (positive or negative).
    - Impedances: Enumerates supported input impedance values.
    - ExternalTriggerRanges: Enumerates external trigger voltage ranges.
    - LED: Enumerates LED states (on/off).
    - AuxIOModes: Enumerates auxiliary I/O modes.
    - Parameters: Enumerates device parameters for advanced configuration.
    - ECCModes: Enumerates ECC (error-correcting code) modes.
    - PackModes: Enumerates packing modes for data transfer.
    - APITraceStates: Enumerates states for enabling/disabling API tracing.
    - HEADER0, HEADER1, HEADER2, HEADER3, AtsHeader: Define record header structures for acquiring metadata from the digitizer.
    - AtsFooter: Defines footer structure for additional metadata in record headers.
"""


class ClockSources(Enum):
    """
    Enumerates the clock source options available for configuring the acquisition clock.

    Enumeration Members:
        INTERNAL_CLOCK (int): Uses the digitizer's internal clock.
        FAST_EXTERNAL_CLOCK (int): Uses an external fast clock.
        MEDIUM_EXTERNAL_CLOCK (int): Uses an external medium-speed clock.
        SLOW_EXTERNAL_CLOCK (int): Uses an external slow clock.
        EXTERNAL_CLOCK_AC (int): Uses an AC-coupled external clock.
        EXTERNAL_CLOCK_DC (int): Uses a DC-coupled external clock.
        EXTERNAL_CLOCK_10MHz_REF (int): Synchronizes to a 10 MHz external reference clock.
        INTERNAL_CLOCK_10MHz_REF (int): Internal 10MHz reference. 
        EXTERNAL_CLOCK_10MHz_PXI (int): Uses a PXI-bus-sourced 10 MHz clock.

    Methods:
        __str__(): Provides a human-readable string representation of the clock source.
        from_str(source_str: str): Converts a human-readable clock source string to its enum equivalent.
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetCaptureClock.html#c.ALAZAR_CLOCK_SOURCES
    """

    INTERNAL_CLOCK = 1
    FAST_EXTERNAL_CLOCK = 2
    MEDIUM_EXTERNAL_CLOCK = 3
    SLOW_EXTERNAL_CLOCK = 4
    EXTERNAL_CLOCK_AC = 5
    EXTERNAL_CLOCK_DC = 6
    EXTERNAL_CLOCK_10MHz_REF = 7
    INTERNAL_CLOCK_10MHz_REF = 8
    EXTERNAL_CLOCK_10MHz_PXI = 10

    def __str__(self) -> str:
        """Provides a human-readable string version"""      
        words = self.name.split('_')
        for i in range(len(words)):
            if words[i].upper() in ["DC", "AC"]:  # Check if the word is an abbreviation (all uppercase)
                continue  # Don't change it
            words[i] = words[i].capitalize()  # Capitalize normal words
        
        return ' '.join(words)

    @classmethod
    def from_str(cls, source_str: str):
        """Returns the enumeration matching the human-readable string."""
        normalized_str = source_str.replace(' ', '_').upper()
        try:
            return cls[normalized_str]
        except KeyError:
            raise ValueError(f"'{source_str}' is not a valid ClockSources enum string")


class SampleRates(Enum):
    """
    Enumerates the sample rates available for configuring data acquisition.

    Enumeration Members (using only KSPS and MSPS in enumerations names for simplicity):
        SAMPLE_RATE_1KSPS (int): 1 kS/s (kilo samples per second).
        SAMPLE_RATE_2KSPS (int): 2 kS/s.
        SAMPLE_RATE_5KSPS (int): 5 kS/s.
        SAMPLE_RATE_10KSPS (int): 10 kS/s.
        SAMPLE_RATE_20KSPS (int): 20 kS/s.
        SAMPLE_RATE_50KSPS (int): 50 kS/s.
        SAMPLE_RATE_100KSPS (int): 100 kS/s.
        SAMPLE_RATE_200KSPS (int): 200 kS/s.
        SAMPLE_RATE_500KSPS (int): 500 kS/s.
        SAMPLE_RATE_1MSPS (int): 1 MS/s (mega samples per second).
        SAMPLE_RATE_2MSPS (int): 2 MS/s.
        SAMPLE_RATE_5MSPS (int): 5 MS/s.
        SAMPLE_RATE_10MSPS (int): 10 MS/s.
        SAMPLE_RATE_20MSPS (int): 20 MS/s.
        SAMPLE_RATE_25MSPS (int): 25 MS/s.
        SAMPLE_RATE_50MSPS (int): 50 MS/s.
        SAMPLE_RATE_100MSPS (int): 100 MS/s.
        SAMPLE_RATE_125MSPS (int): 125 MS/s.
        SAMPLE_RATE_160MSPS (int): 160 MS/s.
        SAMPLE_RATE_180MSPS (int): 180 MS/s.
        SAMPLE_RATE_200MSPS (int): 200 MS/s.
        SAMPLE_RATE_250MSPS (int): 250 MS/s.
        SAMPLE_RATE_300MSPS (int): 300 MS/s.
        SAMPLE_RATE_350MSPS (int): 350 MS/s.
        SAMPLE_RATE_370MSPS (int): 370 MS/s.
        SAMPLE_RATE_400MSPS (int): 400 MS/s.
        SAMPLE_RATE_500MSPS (int): 500 MS/s.
        SAMPLE_RATE_800MSPS (int): 800 MS/s.
        SAMPLE_RATE_1000MSPS (int): 1 GS/s (giga samples per second).
        SAMPLE_RATE_1200MSPS (int): 1.2 GS/s.
        SAMPLE_RATE_1333MSPS_RECUR_DECIMAL (int): 1.333 GS/s
        SAMPLE_RATE_1500MSPS (int): 1.5 GS/s.
        SAMPLE_RATE_1600MSPS (int): 1.6 GS/s.
        SAMPLE_RATE_1800MSPS (int): 1.8 GS/s.
        SAMPLE_RATE_2000MSPS (int): 2 GS/s.
        SAMPLE_RATE_2400MSPS (int): 2.4 GS/s.
        SAMPLE_RATE_2666MSPS_RECUR_DECIMAL (int): 2.666 GS/s
        SAMPLE_RATE_3000MSPS (int): 3 GS/s.
        SAMPLE_RATE_3600MSPS (int): 3.6 GS/s.
        SAMPLE_RATE_4000MSPS (int): 4 GS/s.
        SAMPLE_RATE_5000MSPS (int): 5 GS/s.
        SAMPLE_RATE_10000MSPS (int): 10 GS/s.
        SAMPLE_RATE_USER_DEF (int): User-defined sample rate.

    Methods:
        from_hertz(hz: int): Returns the enumeration member for a given sample rate in hertz.
        from_str(rate_str: str): Converts a human-readable sample rate string (e.g., "1 MS/s") to its enumeration member.
        to_hertz: Converts the enumeration member to its sample rate in hertz.
        __str__(): Provides a human-readable string representation of the sample rate.
    
    Reference:
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
    SAMPLE_RATE_300MSPS = 0x00000090
    SAMPLE_RATE_350MSPS = 0x00000094
    SAMPLE_RATE_370MSPS = 0x00000096
    SAMPLE_RATE_400MSPS = 0x0000002D
    SAMPLE_RATE_500MSPS = 0x00000030
    SAMPLE_RATE_800MSPS = 0x00000032
    SAMPLE_RATE_1000MSPS = 0x00000035
    SAMPLE_RATE_1200MSPS = 0x00000037
    SAMPLE_RATE_1333MSPS_RECUR_DECIMAL = 0x000000C0
    SAMPLE_RATE_1500MSPS = 0x0000003A
    SAMPLE_RATE_1600MSPS = 0x0000003B
    SAMPLE_RATE_1800MSPS = 0x0000003D
    SAMPLE_RATE_2000MSPS = 0x0000003F
    SAMPLE_RATE_2400MSPS = 0x0000006A
    SAMPLE_RATE_2666MSPS_RECUR_DECIMAL = 0x000000C1
    SAMPLE_RATE_3000MSPS = 0x00000075
    SAMPLE_RATE_3600MSPS = 0x0000007B
    SAMPLE_RATE_4000MSPS = 0x00000080
    SAMPLE_RATE_5000MSPS = 0x000000A0
    SAMPLE_RATE_10000MSPS = 0x000000B0
    SAMPLE_RATE_USER_DEF = 0x00000040

    # Class method to find the enum by Hz value
    @classmethod
    def from_hertz(cls, hz: int):
        """
        Returns the enumeration member for a given sample rate in hertz.
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
            300000000: cls.SAMPLE_RATE_300MSPS,
            350000000: cls.SAMPLE_RATE_350MSPS,
            370000000: cls.SAMPLE_RATE_370MSPS,
            400000000: cls.SAMPLE_RATE_400MSPS,
            500000000: cls.SAMPLE_RATE_500MSPS,
            800000000: cls.SAMPLE_RATE_800MSPS,
            1000000000: cls.SAMPLE_RATE_1000MSPS,
            1200000000: cls.SAMPLE_RATE_1200MSPS,
            1333333333: cls.SAMPLE_RATE_1333MSPS_RECUR_DECIMAL, # not exactly 4/3, but probably close enough
            1500000000: cls.SAMPLE_RATE_1500MSPS,
            1600000000: cls.SAMPLE_RATE_1600MSPS,
            1800000000: cls.SAMPLE_RATE_1800MSPS,
            2000000000: cls.SAMPLE_RATE_2000MSPS,
            2400000000: cls.SAMPLE_RATE_2400MSPS,
            2666666667: cls.SAMPLE_RATE_2666MSPS_RECUR_DECIMAL, # not exactly 8/3, but probably close enough
            3000000000: cls.SAMPLE_RATE_3000MSPS,
            3600000000: cls.SAMPLE_RATE_3600MSPS,
            4000000000: cls.SAMPLE_RATE_4000MSPS,
            5000000000: cls.SAMPLE_RATE_5000MSPS,
            10000000000: cls.SAMPLE_RATE_10000MSPS
        }
        if hz in _rate_map.keys():
            return _rate_map[hz]
        raise ValueError(f"No matching sample rate found for {hz} Hz")
    
    @classmethod
    def from_str(cls, rate_str: str):
        """Converts a human-readable sample rate string (e.g., "1 MS/s") to its 
        enumeration member.
        """
        v, u = rate_str.split()
        if u == "kS/s":
            return cls[f"SAMPLE_RATE_{v}KSPS"]
        elif u == "MS/s":
            return cls[f"SAMPLE_RATE_{v}MSPS"]
        elif u == "GS/s":
            return cls[f"SAMPLE_RATE_{round(v*1000)}MSPS"]
        else:
            raise ValueError("Invalid rate string unit: {u}")

    @property
    def to_hertz(self) -> int:
        """Converts the enumeration member to its sample rate in hertz."""
        # recurring decimal special cases
        if self.name == "SAMPLE_RATE_1333MSPS_RECUR_DECIMAL":
            return 1333333333
        elif self.name == "SAMPLE_RATE_2666MSPS_RECUR_DECIMAL":
            return 2666666667
        
        rate = self.name[12:]
        if rate[-4:] == "KSPS":
            return round(float(rate[:-4])*1e3)
        elif rate[-4:] == "MSPS":
            return round(float(rate[:-4])*1e6)
        
    def __str__(self) -> str:
        """Provides a human-readable string representation of the sample rate."""
        h = self.to_hertz
        if h < 1e6:
            return f"{round(h/1000)} kS/s"
        elif h < 1e9:
            return f"{round(h/1000000)} MS/s"
        else:
            return f"{h/1000000000:.1f} GS/s"
        

class ClockEdges(Enum):
    """
    Enumerates the clock edge configurations used for data acquisition.

    Enumeration Members:
        CLOCK_EDGE_RISING (int): Configures the acquisition to trigger on the rising edge of the clock signal.
        CLOCK_EDGE_FALLING (int): Configures the acquisition to trigger on the falling edge of the clock signal.

    Methods:
        from_str(edge_str: str): Converts a human-readable string ("Rising" or "Falling") to its corresponding enumeration member.
        __str__(): Provides a human-readable string representation of the clock edge ("Rising" or "Falling").
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetCaptureClock.html#c.ALAZAR_CLOCK_EDGES
    """
    CLOCK_EDGE_RISING = 0
    CLOCK_EDGE_FALLING = 1

    @classmethod
    def from_str(cls, edge_str:str):
        """
        Converts a human-readable string ("Rising" or "Falling") to its 
        corresponding enumeration member."""
        if edge_str.lower() == "rising":
            return cls.CLOCK_EDGE_RISING
        elif edge_str.lower() == "falling":
            return cls.CLOCK_EDGE_FALLING
        else:
            raise ValueError(
                f"'{edge_str}' is not a valid ClockEdges enum string"
            )
        
    def __str__(self):
        """Provides a human-readable string representation of the clock edge 
        ("Rising" or "Falling").
        """
        if self.value == 0:
            return "Rising"
        else:
            return "Falling"
        

class Channels(IntEnum):
    """
    Enumerates the supported input channels for the digitizer.

    Enumeration Members:
        CHANNEL_ALL (int): Represents all available channels.
        CHANNEL_A (int): Represents input channel A.
        CHANNEL_B (int): Represents input channel B.
        CHANNEL_C (int): Represents input channel C.
        CHANNEL_D (int): Represents input channel D.
        CHANNEL_E (int): Represents input channel E.
        CHANNEL_F (int): Represents input channel F.
        CHANNEL_G (int): Represents input channel G.
        CHANNEL_H (int): Represents input channel H.
        CHANNEL_I (int): Represents input channel I.
        CHANNEL_J (int): Represents input channel J.
        CHANNEL_K (int): Represents input channel K.
        CHANNEL_L (int): Represents input channel L.
        CHANNEL_M (int): Represents input channel M.
        CHANNEL_N (int): Represents input channel N.
        CHANNEL_O (int): Represents input channel O.
        CHANNEL_P (int): Represents input channel P.

    Methods:
        from_int(i: int): Returns the corresponding channel enumeration for an integer value, assuming the integer maps to
                          the channel's alphabetical position (e.g., 0 -> A, 1 -> B).
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarInputControl.html#c.ALAZAR_CHANNELS
    """
    CHANNEL_ALL = 0
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
    def from_int(cls, i: int):
        """Returns the corresponding channel enumeration for an integer value, 
        assuming the integer maps to the channel's alphabetical position (e.g., 
        0 -> A, 1 -> B).
        """
        c = chr(i + ord('A'))
        return getattr(cls, "CHANNEL_" + c)


class ADMAModes(IntEnum):
    """
    Enumerates the supported AutoDMA modes for data transfer in dual-port acquisitions.

    Enumeration Members:
        ADMA_TRADITIONAL_MODE (int): Transfers data using the traditional DMA method.
        ADMA_CONTINUOUS_MODE (int): Enables continuous streaming of data.
        ADMA_NPT (int): Uses the No PreTrigger (NPT) AutoDMA mode for data transfer.
        ADMA_TRIGGERED_STREAMING (int): Streams data triggered by an external event.

    Methods:
        from_str(mode: str): Converts a human-readable string representation of the AutoDMA mode 
                             (e.g., "Traditional", "Continuous") to its enumeration member.
        __str__(): Provides a human-readable string representation of the AutoDMA mode.
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarBeforeAsyncRead.html#c.ALAZAR_ADMA_MODES
    """
    ADMA_TRADITIONAL_MODE = 0
    ADMA_CONTINUOUS_MODE = 0x100
    ADMA_NPT = 0x200
    ADMA_TRIGGERED_STREAMING = 0x400

    @classmethod
    def from_str(cls, mode: str):
        """Converts a human-readable string representation of the AutoDMA mode 
        (e.g., "Traditional", "Continuous") to its enumeration member.
        """
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
        
    def __str__(self) -> str:
        """Provides a human-readable string representation of the AutoDMA mode."""
        if self.value == 0:
            return "Traditional"
        elif self.value == 0x100:
            return "Continuous"
        elif self.value == 0x200:
            return "NPT"
        else:
            return "Triggered streaming"
        

class ADMAFlags(IntEnum):
    """
    Enumerates additional configuration flags for AutoDMA data transfer.

    Enumeration Members:
        ADMA_EXTERNAL_STARTCAPTURE (int): Enables external triggering for starting data capture.
        ADMA_ENABLE_RECORD_HEADERS (int): Includes record headers in the transferred data.
        ADMA_ALLOC_BUFFERS (int): Automatically allocates buffers for data transfer.
        ADMA_FIFO_ONLY_STREAMING (int): Enables FIFO-only streaming mode for data transfer.
        ADMA_INTERLEAVE_SAMPLES (int): Interleaves samples from multiple channels in the transferred data.
        ADMA_GET_PROCESSED_DATA (int): Requests processed data from the device (e.g., averaged or filtered).
        ADMA_DSP (int): Enables digital signal processing on the device.
        ADMA_ENABLE_RECORD_FOOTERS (int): Includes record footers in the transferred data.
        ADMA_PARALLEL_DMA (int): Enables parallel DMA transfers for increased throughput.

    Notes:
        These flags are typically combined to define the behavior of the AutoDMA transfer mode.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarBeforeAsyncRead.html#c.ALAZAR_ADMA_FLAGS
    """
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
    """
    Enumerates auxiliary input levels for the digitizer.

    Enumeration Members:
        AUX_INPUT_LOW (int): Represents a low-level input signal.
        AUX_INPUT_HIGH (int): Represents a high-level input signal.

    Notes:
        These levels are used to interpret the state of auxiliary inputs connected to the digitizer.
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarGetParameter.html#c.ALAZAR_AUX_INPUT_LEVELS
    """
    AUX_INPUT_LOW = 0
    AUX_INPUT_HIGH = 1


class BoardType(Enum):
    """
    Enumerates the supported AlazarTech digitizer board models.

    Enumeration Members:
        ATS_NONE (int): No board.
        ATS850 (int): Represents the ATS850 board.
        ATS310 (int): Represents the ATS310 board.
        ATS330 (int): Represents the ATS330 board.
        ATS855 (int): Represents the ATS855 board.
        ATS315 (int): Represents the ATS315 board.
        ATS335 (int): Represents the ATS335 board.
        ATS460 (int): Represents the ATS460 board.
        ATS860 (int): Represents the ATS860 board.
        ATS660 (int): Represents the ATS660 board.
        ATS665 (int): Represents the ATS665 board.
        ATS9462 (int): Represents the ATS9462 board.
        ATS9434 (int): Represents the ATS9434 board.
        ATS9870 (int): Represents the ATS9870 board.
        ATS9350 (int): Represents the ATS9350 board.
        ATS9325 (int): Represents the ATS9325 board.
        ATS9440 (int): Represents the ATS9440 board.
        ATS9410 (int): Represents the ATS9410 board.
        ATS9351 (int): Represents the ATS9351 board.
        ATS9310 (int): Represents the ATS9310 board.
        ATS9461 (int): Represents the ATS9461 board.
        ATS9850 (int): Represents the ATS9850 board.
        ATS9625 (int): Represents the ATS9625 board.
        ATG6500 (int): Represents the ATG6500 board.
        ATS9626 (int): Represents the ATS9626 board.
        ATS9360 (int): Represents the ATS9360 board.
        AXI9870 (int): Represents the AXI9870 board.
        ATS9370 (int): Represents the ATS9370 board.
        ATU7825 (int): Represents the ATU7825 board.
        ATS9373 (int): Represents the ATS9373 board.
        ATS9416 (int): Represents the ATS9416 board.
        ATS9637 (int): Represents the ATS9637 board.
        ATS9120 (int): Represents the ATS9120 board.
        ATS9371 (int): Represents the ATS9371 board.
        ATS9130 (int): Represents the ATS9130 board.
        ATS9352 (int): Represents the ATS9352 board.
        ATS9453 (int): Represents the ATS9453 board.
        ATS9146 (int): Represents the ATS9146 board.
        ATS9000 (int): Represents the ATS9000 board.
        ATST371 (int): Represents the ATST371 board
        ATS9437 (int): Represents the ATS9437 board.
        ATS9618 (int): Represents the ATS9618 board.
        ATS9358 (int): Represents the ATS9358 board.
        ATS9353 (int): Represents the ATS9353 board.
        ATS9872 (int): Represents the ATS9872 board.
        ATS9470 (int): Represents the ATS9470 board.
        ATS9628 (int): Represents the ATS9628 board.
        ATS9874 (int): Represents the ATS9874 board.
        ATS9473 (int): Represents the ATS9473 board.
        ATS9280 (int): Represents the ATS9280 board.
        ATS4001 (int): Represents the ATS4001 board.
        ATS9182 (int): Represents the ATS9182 board.
        ATS9364 (int): Represents the ATS9364 board.
        ATS9442 (int): Represents the ATS9442 board.
        ATS9376 (int): Represents the ATS9376 board.
        ATS9380 (int): Represents the ATS9380 board.
        ATS9428 (int): Represents the ATS9428 board.

    Notes:
        Each member corresponds to a specific AlazarTech digitizer model. These identifiers are used to distinguish board
        types during initialization and configuration.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarGetBoardKind.html#c.BoardTypes
    """
    ATS_NONE = 0
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
    ATS9434 = 12
    ATS9870 = 13
    ATS9350 = 14
    ATS9325 = 15
    ATS9440 = 16
    ATS9410 = 17
    ATS9351 = 18
    ATS9310 = 19
    ATS9461 = 20
    ATS9850 = 21
    ATS9625 = 22
    ATG6500 = 23
    ATS9626 = 24
    ATS9360 = 25
    AXI9870 = 26
    ATS9370 = 27
    ATU7825 = 28
    ATS9373 = 29
    ATS9416 = 30
    ATS9637 = 31
    ATS9120 = 32
    ATS9371 = 33
    ATS9130 = 34
    ATS9352 = 35
    ATS9453 = 36
    ATS9146 = 37
    ATS9000 = 38
    ATST371 = 39
    ATS9437 = 40
    ATS9618 = 41
    ATS9358 = 42
    ATS9353 = 44
    ATS9872 = 45
    ATS9470 = 46
    ATS9628 = 47
    ATS9874 = 48
    ATS9473 = 49
    ATS9280 = 50
    ATS4001 = 51
    ATS9182 = 52
    ATS9364 = 53
    ATS9442 = 54
    ATS9376 = 55
    ATS9380 = 56
    ATS9428 = 57


class BoardOptionsLow(Enum):
    """
    With `BoardOptionsHigh`, enumerates configuration options for AlazarTech digitizer boards.

    Enumeration Members:
        OPTION_STREAMING_DMA (int): Enables DMA-based streaming.
        OPTION_EXTERNAL_CLOCK (int): Allows the use of an external clock.
        OPTION_DUAL_PORT_MEMORY (int): Enables dual-port memory configuration.
        OPTION_180MHZ_OSCILLATOR (int): Enables a 180 MHz oscillator.
        OPTION_LVTTL_EXT_CLOCK (int): Configures the board for an LVTTL external clock.
        OPTION_SW_SPI (int): Enables software-controlled SPI for advanced configurations.
        OPTION_ALT_INPUT_RANGES (int): Enables alternative input ranges.
        OPTION_VARIABLE_RATE_10MHZ_PLL (int): Configures a variable rate 10 MHz PLL.
        OPTION_MULTI_FREQ_VCO (int): Enables multiple frequency VCOs.
        OPTION_2GHZ_ADC (int): Activates a 2 GHz ADC mode.
        OPTION_DUAL_EDGE_SAMPLING (int): Enables dual-edge sampling for higher precision.
        OPTION_DCLK_PHASE (int): Adjusts the phase of the data clock.
        OPTION_WIDEBAND (int): Activates wideband signal handling.

    Notes:
        These options represent board-level capabilities and configurations that 
        can be set to optimize performance for specific acquisition scenarios.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarQueryCapability.html#c.ALAZAR_BOARD_OPTIONS_LOW
    """
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
    """
    With `BoardOptionsLow`, enumerates configuration options for AlazarTech digitizer boards.

    Enumeration Members:
        OPTION_OEM_FPGA (int): Indicates the use of a custom OEM FPGA configuration.

    Notes:
        These options represent board-level capabilities and configurations that 
        can be set to optimize performance for specific acquisition scenarios.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarQueryCapability.html#c.ALAZAR_BOARD_OPTIONS_HIGH
    """
    OPTION_OEM_FPGA = (1 << 15)


class InputRanges(Enum):
    """
    Enumerates the supported input voltage ranges for channel configuration.

    Enumeration Members:
        INPUT_RANGE_PM_20_MV (int): ±20 mV.
        INPUT_RANGE_PM_40_MV (int): ±40 mV.
        INPUT_RANGE_PM_50_MV (int): ±50 mV.
        INPUT_RANGE_PM_80_MV (int): ±80 mV.
        INPUT_RANGE_PM_100_MV (int): ±100 mV.
        INPUT_RANGE_PM_125_MV (int): ±125 mV.
        INPUT_RANGE_PM_200_MV (int): ±200 mV.
        INPUT_RANGE_PM_250_MV (int): ±250 mV.
        INPUT_RANGE_PM_400_MV (int): ±400 mV.
        INPUT_RANGE_PM_500_MV (int): ±500 mV.
        INPUT_RANGE_PM_560_MV (int): ±560 mV.
        INPUT_RANGE_PM_800_MV (int): ±800 mV.
        INPUT_RANGE_PM_1_V (int): ±1 V.
        INPUT_RANGE_PM_1_V_25 (int): ±1.25 V.
        INPUT_RANGE_PM_2_V (int): ±2 V.
        INPUT_RANGE_PM_2_V_5 (int): ±2.5 V.
        INPUT_RANGE_PM_4_V (int): ±4 V.
        INPUT_RANGE_PM_5_V (int): ±5 V.
        INPUT_RANGE_PM_8_V (int): ±8 V.
        INPUT_RANGE_PM_10_V (int): ±10 V.
        INPUT_RANGE_PM_16_V (int): ±16 V.
        INPUT_RANGE_PM_20_V (int): ±20 V.
        INPUT_RANGE_PM_40_V (int): ±40 V.

    Methods:
        from_v(v: float): Returns the enumeration member for a given voltage range in volts.
        from_str(range_str: str): Converts a human-readable string (e.g., "±100 mV") to its enumeration member.
        to_volts: Converts the enumeration member to its voltage range in volts.
        __str__(): Provides a human-readable string representation of the input range (e.g., "±100 mV").

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarInputControl.html#c.ALAZAR_INPUT_RANGES
    """
    INPUT_RANGE_PM_20_MV = 0x1
    INPUT_RANGE_PM_40_MV = 0x2
    INPUT_RANGE_PM_50_MV = 0x3
    INPUT_RANGE_PM_80_MV = 0x4
    INPUT_RANGE_PM_100_MV = 0x5
    INPUT_RANGE_PM_125_MV = 0x28
    INPUT_RANGE_PM_200_MV = 0x6
    INPUT_RANGE_PM_250_MV = 0x30
    INPUT_RANGE_PM_400_MV = 0x7
    INPUT_RANGE_PM_500_MV = 0x8
    INPUT_RANGE_PM_560_MV = 0x62
    INPUT_RANGE_PM_800_MV = 0x9
    INPUT_RANGE_PM_1_V = 0xA
    INPUT_RANGE_PM_1_V_25 = 0x21
    INPUT_RANGE_PM_2_V = 0xB
    INPUT_RANGE_PM_2_V_5 = 0x25
    INPUT_RANGE_PM_4_V = 0xC
    INPUT_RANGE_PM_5_V = 0xD
    INPUT_RANGE_PM_8_V = 0xE
    INPUT_RANGE_PM_10_V = 0xF
    INPUT_RANGE_PM_16_V = 0x12
    INPUT_RANGE_PM_20_V = 0x10
    INPUT_RANGE_PM_40_V = 0x11
    # There are numerous unipolar ranges (e.g. 0 to 1 V), not supported here

    @classmethod
    def from_volts(cls, v: float):
        """
        Returns the enumeration member for a given voltage range in volts.
        """
        whole_num = int(v)
        decimal = float(v) - whole_num
        millivolts = int(1000 * decimal)
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
    def from_str(cls, range_str: str):
        """Converts a human-readable string to its corresponding enumeration member."""
        strsplit = range_str.split()
        v = float(strsplit[0].replace("±",""))
        u = strsplit[1].lower()
        if u == "mv":
            return cls.from_volts(v/1000)
        elif u == "v":
            return cls.from_volts(v)
        raise ValueError(f"No matching input range for string, {range_str}")
        
    @property
    def to_volts(self) -> float:
        """Converts the enumeration member to its voltage range in volts."""
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
        elif self.name == "INPUT_RANGE_PM_560_MV":
            return 0.56
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
        """Provides a human-readable string representation of the input range."""
        r = self.to_volts
        if r < 1:
            return f"±{int(r*1000)} mV"
        else:
            return f"±{r} V"


class Capabilities(Enum):
    """
    Enumerates the device capabilities and features supported by AlazarTech boards.

    Enumeration Members:
        GET_SERIAL_NUMBER (int): Retrieves the serial number of the board.
        GET_FIRST_CAL_DATE (int): Retrieves the date of the first calibration.
        GET_LATEST_CAL_DATE (int): Retrieves the most recent calibration date.
        GET_LATEST_TEST_DATE (int): Retrieves the date of the latest test.
        GET_LATEST_CAL_DATE_MONTH (int): Retrieves the month of the latest calibration date.
        GET_LATEST_CAL_DATE_DAY (int): Retrieves the day of the latest calibration date.
        GET_LATEST_CAL_DATE_YEAR (int): Retrieves the year of the latest calibration date.
        GET_BOARD_OPTIONS_LOW (int): Retrieves low-level board options.
        GET_BOARD_OPTIONS_HIGH (int): Retrieves high-level board options.
        MEMORY_SIZE (int): Retrieves the size of onboard memory.
        ASOPC_TYPE (int): Retrieves the FPGA signature 
        BOARD_TYPE (int): Retrieves the type of the board.
        GET_PCIE_LINK_SPEED (int): PCIe link generation.
        GET_PCIE_LINK_WIDTH (int): PCIe link width in lanes .
        GET_MAX_PRETRIGGER_SAMPLES (int): Retrieves the maximum number of pre-trigger samples supported.
        GET_CPF_DEVICE (int): User-programmable FPGA device. 1 = SL50, 2 = SE260 
        HAS_RECORD_FOOTERS_SUPPORT (int): Checks if record footers are supported.
        CAP_SUPPORTS_TRADITIONAL_AUTODMA (int): Checks if traditional AutoDMA is supported.
        CAP_SUPPORTS_NPT_AUTODMA (int): Checks if NPT AutoDMA is supported.
        CAP_MAX_NPT_PRETRIGGER_SAMPLES (int): Retrieves the maximum pre-trigger samples for NPT AutoDMA.
        CAP_IS_VFIFO_BOARD (int): Tests if this board of the virtual-FIFO type. 
        CAP_SUPPORTS_NATIVE_SINGLE_PORT (int): Checks if native single-port mode is supported.
        CAP_SUPPORT_8_BIT_PACKING (int): Checks if 8-bit packing is supported.
        CAP_SUPPORT_12_BIT_PACKING (int): Checks if 12-bit packing is supported.
        HAS_PARALLEL_DMA_SUPPORT (int): Queries if the board supports parallel DMA.
        HAS_SEQUENTIAL_DMA_SUPPORT (int): Queries if the board supports sequential DMA.
        HAS_RECORD_HEADERS_SUPPORT (int): Tests if this board supports record headers.
        CAP_SUPPORT_TRADITIONAL_SAMPLES_INTERLEAVED (int): Tests if this board supports samples interleaved in traditional mode.
        CAP_SUPPORT_SOFTWARE_CAL (int): Tests if this board supports software calibration.
        CAP_SUPPORTS_API_LOG_CLEAR (int): Tests if this board supports API log clear.
        CAP_SUPPORTS_TRIGGER_SKIPPING (int): Tests if this board supports trigger skipping.

    Notes:
        These capabilities are queried to determine hardware features and limitations.
        They are used for configuring the board and ensuring compatibility with acquisition requirements.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarQueryCapability.html#c.ALAZAR_CAPABILITIES
    """
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
    HAS_PARALLEL_DMA_SUPPORT = 0x10000072
    HAS_SEQUENTIAL_DMA_SUPPORT = 0x10000086
    HAS_RECORD_HEADERS_SUPPORT = 0x10000081
    CAP_SUPPORT_TRADITIONAL_SAMPLES_INTERLEAVED = 0x10000082
    CAP_SUPPORT_SOFTWARE_CAL = 0x10000083
    CAP_SUPPORTS_API_LOG_CLEAR = 0x10000084
    CAP_SUPPORTS_TRIGGER_SKIPPING = 0x10000085


class Couplings(Enum):
    """
    Enumerates the input coupling options for digitizer channels.

    Enumeration Members:
        AC_COUPLING (int): Configures the channel for AC coupling.
        DC_COUPLING (int): Configures the channel for DC coupling.
        GND_COUPLING (int): Grounds the channel, disconnecting the signal input.

    Methods:
        from_str(coupling: str): Converts a human-readable string representation of the coupling mode
                                 (e.g., "AC", "DC") to its enumeration member.
        __str__(): Provides a human-readable string representation of the coupling mode ("AC", "DC", or "Ground").

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarInputControl.html#c.ALAZAR_COUPLINGS
    """
    AC_COUPLING = 1
    DC_COUPLING = 2
    GND_COUPLING = 4

    @classmethod
    def from_str(cls, coupling: str):
        """Converts a human-readable string representation of the coupling mode
        (e.g., "AC", "DC") to its enumeration member.
        """
        coupling_ = coupling.lower()
        if coupling_ == "ac":
            return cls.AC_COUPLING
        elif coupling_ == "dc":
            return cls.DC_COUPLING
        elif coupling_ == "ground":
            return cls.GND_COUPLING
        else:
            raise ValueError(f"'{coupling}' is not a valid Couplings enum string")

    def __str__(self) -> str:
        """Provides a human-readable string representation of the coupling mode 
        ("AC", "DC", or "Ground").
        """
        if self.value == 1:
            return "AC"
        elif self.value == 2:
            return "DC"
        else:
            return "Ground"


class TriggerEngines(Enum):
    """
    Enumerates the trigger engines available for AlazarTech digitizers.

    Enumeration Members:
        TRIG_ENGINE_J (int): Represents trigger engine J.
        TRIG_ENGINE_K (int): Represents trigger engine K.

    Notes:
        AlazarTech digitizers typically support two independent trigger engines, J and K, 
        which can be configured separately to detect different trigger conditions.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetTriggerOperation.html#c.ALAZAR_TRIGGER_ENGINES
    """
    TRIG_ENGINE_J = 0
    TRIG_ENGINE_K = 1


class TriggerOperations(Enum):
    """
    Enumerates the logical operations that can combine trigger conditions from 
    multiple trigger engines.

    Enumeration Members:
        TRIG_ENGINE_OP_J (int): Uses only trigger engine J.
        TRIG_ENGINE_OP_K (int): Uses only trigger engine K.
        TRIG_ENGINE_OP_J_OR_K (int): Triggers when either engine J or K condition is met.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetTriggerOperation.html#c.ALAZAR_TRIGGER_OPERATIONS
    """
    TRIG_ENGINE_OP_J = 0
    TRIG_ENGINE_OP_K = 1
    TRIG_ENGINE_OP_J_OR_K = 2


class TriggerSources(Enum):
    """
    Enumerates the supported trigger sources for AlazarTech digitizers.

    Enumeration Members:
        TRIG_CHAN_A (int): Uses channel A as the trigger source.
        TRIG_CHAN_B (int): Uses channel B as the trigger source.
        TRIG_EXTERNAL (int): Uses an external signal as the trigger source.
        TRIG_DISABLE (int): Disables triggering.
        TRIG_CHAN_C (int): Uses channel C as the trigger source (if available).
        TRIG_CHAN_D (int): Uses channel D as the trigger source (if available).
        TRIG_CHAN_E (int): Uses channel E as the trigger source (if available).
        TRIG_CHAN_F (int): Uses channel F as the trigger source (if available).
        TRIG_CHAN_G (int): Uses channel G as the trigger source (if available).
        TRIG_CHAN_H (int): Uses channel H as the trigger source (if available).
        TRIG_CHAN_I (int): Uses channel I as the trigger source (if available).
        TRIG_CHAN_J (int): Uses channel J as the trigger source (if available).
        TRIG_CHAN_K (int): Uses channel K as the trigger source (if available).
        TRIG_CHAN_L (int): Uses channel L as the trigger source (if available).
        TRIG_CHAN_M (int): Uses channel M as the trigger source (if available).
        TRIG_CHAN_N (int): Uses channel N as the trigger source (if available).
        TRIG_CHAN_O (int): Uses channel O as the trigger source (if available).
        TRIG_CHAN_P (int): Uses channel P as the trigger source (if available).

    Methods:
        from_str(trigger: str): Converts a human-readable string (e.g., "Channel A", "External") 
                                to its enumeration member.
        channel_index: Returns the zero-based index of the input channel (e.g., A=0, B=1) 
                       for trigger sources that correspond to channels.
        __str__(): Provides a human-readable string representation of the trigger source.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetTriggerOperation.html#c.ALAZAR_TRIGGER_SOURCES
    """
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

    @classmethod
    def from_str(cls, trigger: str):
        """Converts a human-readable string (e.g., "Channel A", "External") 
        to its enumeration member.
        """
        trigger_str = trigger.lower()
        if trigger_str[:7] == "channel":
            return cls[f"TRIG_CHAN_{trigger_str[-1].upper()}"]
        elif trigger_str == "external":
            return cls.TRIG_EXTERNAL
        elif trigger_str == "disable":
            return cls.TRIG_DISABLE
        else:
            raise ValueError(f"'{trigger}' is not a valid TriggerSources enum string")
        
    @property
    def channel_index(self) -> int:
        """Returns the zero-based index of the input channel (e.g., A=0, B=1) 
        for trigger sources that correspond to channels.
        """
        if self not in [TriggerSources.TRIG_EXTERNAL, TriggerSources.TRIG_DISABLE]:
            index = self.value
            if index > 3: index -= 2
            return index
        else:
            raise RuntimeError("Trigger source is not an input channel")

    def __str__(self) -> str:
        """Returns the zero-based index of the input channel for trigger sources 
        corresponding to channels.
        """
        if self.name[5:9] == "CHAN":
            return f"Channel {self.name[-1]}"
        elif self.name[5:] == "EXTERNAL":
            return "External"
        else:
            return "Disable"


class TriggerSlopes(Enum):
    """
    Enumerates the supported trigger slope configurations for AlazarTech digitizers.

    Enumeration Members:
        TRIGGER_SLOPE_POSITIVE (int): Triggers on the positive slope (rising edge) of the signal.
        TRIGGER_SLOPE_NEGATIVE (int): Triggers on the negative slope (falling edge) of the signal.

    Methods:
        from_str(slope: str): Converts a human-readable string (e.g., "Positive", "Negative") 
                              to its corresponding enumeration member.
        __str__(): Provides a human-readable string representation of the trigger slope.


    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetTriggerOperation.html#c.ALAZAR_TRIGGER_SLOPES
    """
    TRIGGER_SLOPE_POSITIVE = 1
    TRIGGER_SLOPE_NEGATIVE = 2
        
    @classmethod
    def from_str(cls, slope: str):
        """Converts a human-readable string representation of the trigger slope 
        ("Positive" or "Negative") to its corresponding enumeration member.
        """
        slope_str = slope.lower()
        if slope_str == "positive":
            return cls.TRIGGER_SLOPE_POSITIVE
        elif slope_str == "negative":
            return cls.TRIGGER_SLOPE_NEGATIVE
        else:
            raise ValueError(f"'{slope}' is not a valid TriggerSlopes enum string")
        
    def __str__(self) -> str:
        """
        Provides a human-readable representation of the trigger slope.

        Returns:
            str: "Positive" for rising edge or "Negative" for falling edge.
        """
        if self.value == 1:
            return "Positive"
        else:
            return "Negative"


class Impedances(Enum):
    """
    Enumerates the supported input impedance configurations for AlazarTech digitizers.

    Enumeration Members:
        IMPEDANCE_1M_OHM (int): Input impedance of 1 MΩ.
        IMPEDANCE_50_OHM (int): Input impedance of 50 Ω.
        IMPEDANCE_75_OHM (int): Input impedance of 75 Ω.
        IMPEDANCE_100_OHM (int): Input impedance of 100 Ω.
        IMPEDANCE_300_OHM (int): Input impedance of 300 Ω.

    Methods:
        from_ohms(ohms: int): Returns the enumeration member corresponding to the specified impedance in ohms.
        from_str(ohms: str): Converts a human-readable string (e.g., "50 Ω", "1 MΩ") to its enumeration member.
        in_ohms: Converts the enumeration member to its impedance value in ohms.
        __str__(): Provides a human-readable string representation of the impedance (e.g., "50 Ω", "1 MΩ").

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarInputControl.html#c.ALAZAR_IMPEDANCES
    """
    IMPEDANCE_1M_OHM = 1
    IMPEDANCE_50_OHM = 2
    IMPEDANCE_75_OHM = 4
    IMPEDANCE_100_OHM = 10
    IMPEDANCE_300_OHM = 8

    @classmethod
    def from_ohms(cls, ohms: int):
        """Returns the enumeration member for a given impedance in ohms."""
        if ohms == 1_000_000:
            return cls.IMPEDANCE_1M_OHM
        elif ohms == 50:
            return cls.IMPEDANCE_50_OHM
        elif ohms == 75:
            return cls.IMPEDANCE_75_OHM
        elif ohms == 100:
            return cls.IMPEDANCE_100_OHM
        elif ohms == 300:
            return cls.IMPEDANCE_300_OHM
        raise ValueError(f"No matching input impedance found for {ohms} ohms")
    
    @classmethod
    def from_str(cls, ohms: str):
        """Converts a human-readable string to its corresponding enumeration member."""
        ohms_ = ohms.lower()
        if ohms_ in ["50 ohm", "50 Ω".lower()]:
            return cls.IMPEDANCE_50_OHM
        elif ohms_ in ["1 mohm", "1 MΩ".lower()]:
            return cls.IMPEDANCE_1M_OHM
        elif ohms_ in ["75 ohm", "75 Ω".lower()]:
            return cls.IMPEDANCE_75_OHM
        elif ohms_ in ["100 ohm", "100 Ω".lower()]:
            return cls.IMPEDANCE_100_OHM
        elif ohms_ == ["300 ohm", "300 Ω".lower()]:
            return cls.IMPEDANCE_300_OHM
        raise ValueError(f"No matching input impedance found for {ohms}")
    
    @property
    def in_ohms(self) -> int:
        """Converts the enumeration member to its impedance value in ohms."""
        if self.value == 1:
            return 1_000_000
        elif self.value == 2:
            return 50
        elif self.value == 4:
            return 75
        elif self.value == 10:
            return 100
        elif self.value == 8:
            return 300
        
    def __str__(self) -> str:
        """Provides a human-readable string representation of the impedance."""
        r = self.in_ohms
        if r == 1e6:
            return f"1 MΩ"
        else:
            return f"{int(r)} Ω"


class ExternalTriggerRanges(Enum):
    """
    Enumerates the supported external trigger voltage ranges for AlazarTech digitizers.

    Enumeration Members:
        ETR_5V_50OHM (int): ±5 V range, 50 Ω impedance.
        ETR_1V_50OHM (int): ±1 V range, 50 Ω impedance.
        ETR_TTL (int): TTL logic level (0 to 5 V, high impedance).
        ETR_2V5_50OHM (int): ±2.5 V range, 50 Ω impedance.
        ETR_5V_300OHM (int): ±5 V range, 300 Ω impedance.

    Methods:
        from_str(rng: str): Converts a human-readable string (e.g., "±5 V", "TTL") to its enumeration member.
        to_volts: Converts the enumeration member to its voltage range in volts.
        __str__(): Provides a human-readable string representation of the trigger range.
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetExternalTrigger.html#c.ALAZAR_EXTERNAL_TRIGGER_RANGES
    """
    ETR_5V_50OHM = 0
    ETR_1V_50OHM = 1
    ETR_TTL = 2
    ETR_2V5_50OHM = 3
    ETR_5V_300OHM = 4

    @classmethod
    def from_str(cls, rng: str):
        if rng == "±5 V, 50 Ω": 
            return cls.ETR_5V_50OHM
        elif rng == "±1 V, 50 Ω": 
            return cls.ETR_1V_50OHM
        elif rng == "TTL": 
            return cls.ETR_TTL
        elif rng == "±2.5 V, 50 Ω": 
            return cls.ETR_2V5_50OHM
        elif rng == "±5 V, 300 Ω": 
            return cls.ETR_5V_300OHM
        
    @property
    def to_volts(self) -> float:
        if self.name == "ETR_5V_50OHM": 
            return 5.0
        elif self.name == "ETR_1V_50OHM": 
            return 1.0
        elif self.name == "ETR_TTL": 
            return 5.0 # Not +/-5V in this case, 0V to 5V
        elif self.name == "ETR_2V5_50OHM": 
            return 2.5
        elif self.name == "ETR_5V_300OHM":
            return 5.0
        
    def __str__(self):
        if self.name == "ETR_5V_50OHM": 
            return "±5 V, 50 Ω"
        elif self.name == "ETR_1V_50OHM": 
            return "±1 V, 50 Ω"
        elif self.name == "ETR_TTL": 
            return "TTL"
        elif self.name == "ETR_2V5_50OHM": 
            return "±2.5 V, 50 Ω"
        elif self.name == "ETR_5V_300OHM": 
            return "±5 V, 300 Ω"
        

class LED(Enum):
    """
    Enumerates the states of the LED indicator on the mounting bracket of some 
    AlazarTech digitizers.

    Enumeration Members:
        LED_OFF (int): Turns the LED off.
        LED_ON (int): Turns the LED on.
    
    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarSetLED.html#c.ALAZAR_LED
    """
    LED_OFF = 0
    LED_ON = 1


class AuxIOModes(Enum):
    """
    Enumerates the modes for auxiliary I/O (input/output) functionality on AlazarTech digitizers.

    Enumeration Members:
        AUX_OUT_TRIGGER (int): Configures the auxiliary I/O as a trigger output.
        AUX_IN_TRIGGER_ENABLE (int): Configures the auxiliary I/O as a trigger enable input.
        AUX_OUT_PACER (int): Configures the auxiliary I/O as a pacer output.
        AUX_IN_AUXILIARY (int): Configures the auxiliary I/O as an auxiliary input.
        AUX_OUT_SERIAL_DATA (int): Configures the auxiliary I/O as a serial data output.

    Notes:
        These modes allow auxiliary I/O to serve various purposes, including signaling and
        synchronization with external devices.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarConfigureAuxIO.html#c.ALAZAR_AUX_IO_MODES
    """
    AUX_OUT_TRIGGER = 0
    AUX_IN_TRIGGER_ENABLE = 1
    AUX_OUT_PACER = 2
    AUX_IN_AUXILIARY = 13
    AUX_OUT_SERIAL_DATA = 14


class Parameters(Enum):
    """
    Enumerates the advanced device parameters for configuring and querying 
    AlazarTech digitizers. For use with `set_parameter()` and/or `get_parameter()`.

    Enumeration Members:
        DATA_WIDTH (int): The number of bits per sample.
        SETGET_ASYNC_BUFFSIZE_BYTES (int): The size of API-allocated DMA buffers in bytes.
        SETGET_ASYNC_BUFFCOUNT (int): The number of API-allocated DMA buffers.
        GET_ASYNC_BUFFERS_PENDING (int): DMA buffers currently posted to the board .
        GET_ASYNC_BUFFERS_PENDING_FULL (int): DMA buffers waiting to be processed by the application.
        GET_ASYNC_BUFFERS_PENDING_EMPTY (int): DMA buffers waiting to be filled by the board.
        SET_DATA_FORMAT (int): 0 if the data format is unsigned, and 1 otherwise.
        GET_DATA_FORMAT (int): 0 if the data format is unsigned, and 1 otherwise.
        GET_SAMPLES_PER_TIMESTAMP_CLOCK (int): Number of samples per timestamp clock.
        GET_RECORDS_CAPTURED (int): Records captured since the start of the buffer.
        ECC_MODE (int): ECC mode. Member of `ECCModes`.
        GET_AUX_INPUT_LEVEL (int): Read the TTL level of the AUX connector. Member of `AuxInputLevels`.
        GET_CHANNELS_PER_BOARD (int): Number of analog channels supported by this digitizer.
        GET_FPGA_TEMPERATURE (int): Current FPGA temperature in degrees Celcius (32-bit floating point).
        PACK_MODE (int): Get/Set the pack mode as a member of `PackModes`.
        API_FLAGS (int): Get/Set the state of the API logging as a member of `APITraceStates`.
        SET_SOFTWARE_CAL_MECHANISM (int): Use software calibration mechanism if set to 1, else use standard hardware calibration.
        API_LOG_CLEAR (int): Clear the log file of the API logging mechanism.
        SETGET_TRIGGER_SKIPPING (int): Sets or gets the current value of trigger skipping. 
        GET_ADC_TEMPERATURE (int): Current ADC temperature in degrees Celcius (32-bit floating point).
        GET_ONBOARD_MEMORY_USED (int): Get the percentage of on-board memory used. Feature only supported for certain board types.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarGetParameter.html#c.ALAZAR_PARAMETERS
    """
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
    """
    Enumerates the ECC (Error-Correcting Code) modes for AlazarTech digitizers.

    Enumeration Members:
        ECC_DISABLE (int): Disables ECC mode, providing no error correction.
        ECC_ENABLE (int): Enables ECC mode, allowing error correction for enhanced data reliability.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarGetParameter.html#c.ALAZAR_ECC_MODES
    """
    ECC_DISABLE = 0
    ECC_ENABLE = 1


class PackModes(Enum):
    """
    Enumerates the data packing modes for AlazarTech digitizers.

    Enumeration Members:
        PACK_DEFAULT (int): No packing; data is stored in its native format.
        PACK_8_BITS_PER_SAMPLE (int): Packs data to 8 bits per sample.
        PACK_12_BITS_PER_SAMPLE (int): Packs data to 12 bits per sample.

    Methods:
        from_str(pack: str): Converts a human-readable string (e.g., "8-bit", "12-bit") 
                             to its corresponding enumeration member.
        __str__(): Provides a human-readable string representation of the packing mode.


    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarGetParameter.html#c.ALAZAR_PACK_MODES
    """
    PACK_DEFAULT = 0
    PACK_8_BITS_PER_SAMPLE = 1
    PACK_12_BITS_PER_SAMPLE = 2
    
    @classmethod
    def from_str(cls, pack: str):
        """Converts a human-readable string (e.g., "8-bit", "12-bit") to its 
        corresponding enumeration member.
        """
        pack_lower = pack.lower()
        if pack_lower == "none":
            return cls.PACK_DEFAULT
        elif pack_lower == "8-bit":
            return cls.PACK_8_BITS_PER_SAMPLE
        elif pack_lower == "12-bit":
            return cls.PACK_12_BITS_PER_SAMPLE
        else:
            raise ValueError(f"'{pack}' is not a valid PackModes enum string")

    def __str__(self) -> str:
        """Provides a human-readable string representation of the packing mode."""
        if self.value == 0:
            return "None"
        elif self.value == 1:
            return "8-bit"
        else:
            return "12-bit"
        

class APITraceStates(Enum):
    """
    Enumerates the states for enabling or disabling API tracing in AlazarTech digitizers.

    Enumeration Members:
        API_DISABLE_TRACE (int): Disables API tracing.
        API_ENABLE_TRACE (int): Enables API tracing.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarGetParameter.html#c.ALAZAR_API_TRACE_STATES
    """
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
    """
    Represents the record header structure used in AlazarTech digitizers.

    The `AtsHeader` structure provides metadata about each record captured by the digitizer,
    including information about the record number, timestamp, and configuration details.

    Attributes (note that some of these may not be implemented by the card/API):
        hdr0 (HEADER0): Contains metadata such as serial number, system number, and data format.
        hdr1 (HEADER1): Contains metadata such as the record number and board type.
        hdr2 (HEADER2): Contains the low part of the timestamp.
        hdr3 (HEADER3): Contains the high part of the timestamp and additional 
                        configuration details, including clock source, sample rate, 
                        input range, and triggering information.

    Properties:
        record_number (int): The record number extracted from `hdr1`.
        timestamp (int): The full timestamp, combining the low and high parts from `hdr2` and `hdr3`.

    Reference:
    https://docs.alazartech.com/ats-sdk-user-guide/latest/programmers-guide.html#record-headers-and-timestamps
    """
    _fields_ = [
        ("hdr0", HEADER0),
        ("hdr1", HEADER1),
        ("hdr2", HEADER2),
        ("hdr3", HEADER3)
    ]

    @property
    def record_number(self) -> int:
        """The record number in the acquisition."""
        return self.hdr1.RecordNumber

    @property
    def timestamp(self) -> int:
        """The full timestamp, combining the low and high parts.
        
        Timestamp ticks are a number of sample clock periods, see board-specific information.
        """
        return (self.hdr2.TimeStampLowPart) + \
               (self.hdr3.TimeStampHighPart << 32) 


class AtsFooter(Structure):
    """
    Represents the footer structure used in AlazarTech digitizers.

    The `AtsFooter` structure provides additional metadata about each record 
    captured by the digitizer, including auxiliary and timestamp information, 
    which may be included in acquisition data when footers are enabled.

    Attributes:
        aux_and_pulsar_low (c_uint8): Auxiliary and low part of pulsar data.
        pulsar_high (c_uint8): High part of pulsar data.
        tt_low (c_uint16): Low part of the timestamp.
        tt_med (c_uint16): Middle part of the timestamp.
        tt_high (c_uint16): High part of the timestamp.
        rn_low (c_uint16): Low part of the record number.
        rn_high (c_uint16): High part of the record number.
        fc_low (c_uint16): Low part of the frame count.
        fc_high (c_uint8): High part of the frame count.
        type (c_uint8): Type of footer record.

    Properties:
        record_number (int): The full record number, combining the low and high parts.
        timestamp (int): The full timestamp, combining the low, middle, and high parts.

    Reference:
    https://github.com/alazartech/ats-footers/blob/release/atsfooters/src/atsfooters_internal.hpp
    """
    # 
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
    def record_number(self) -> int:
        """The record number in the acquisition."""
        return (self.rn_low) + \
               (self.rn_high << 16) 

    @property
    def timestamp(self) -> int:
        """The full timestamp."""
        return (self.tt_low) + \
               (self.tt_med << 16) + \
               (self.tt_high << 32)
    
    