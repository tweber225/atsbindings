import numpy as np
import time

from atsbindings.bindings import Board, Buffer
from atsbindings.enumerations import (
    ClockSources, SampleRates, 
    Channels, Couplings, InputRanges, Impedances,
    TriggerOperations, TriggerEngines, TriggerSources, TriggerSlopes,
    ExternalTriggerRanges,
    AuxIOModes, 
    ADMAModes, ADMAFlags
)


# Parameters
channels = [True, True] # [channel A, channel B, etc] (extend for >2 channel boards)
input_ranges = [1.0, 1.0] # +/- V (match size of channels list) (must match ones of the available ranges)
sample_rate = 20e6 # must match one of the available internally generated sample rates
samples_per_record = 512
records_per_buffer = 128
buffers_to_acquire = 256
buffer_count = 16

# Initialize board
board = Board()

board.set_capture_clock(
    source=ClockSources.INTERNAL_CLOCK,
    rate=SampleRates.from_hz(sample_rate)
)

nchannels_present = len(channels)
nchannels_active = sum(channels)
for i in range(nchannels_present):
    board.input_control_ex(
        channel=Channels.from_int(i),
        coupling=Couplings.DC_COUPLING,
        input_range=InputRanges.from_v(input_ranges[i]),
        impedance=Impedances.IMPEDANCE_50_OHM,
    )

board.set_trigger_operation(
    operation=TriggerOperations.TRIG_ENGINE_OP_J,
    engine1=TriggerEngines.TRIG_ENGINE_J,
    source1=TriggerSources.TRIG_EXTERNAL,
    slope1=TriggerSlopes.TRIGGER_SLOPE_POSITIVE,
    level1=192,
    engine2=TriggerEngines.TRIG_ENGINE_K,
    source2=TriggerSources.TRIG_DISABLE,
    slope2=TriggerSlopes.TRIGGER_SLOPE_POSITIVE,
    level2=192
)

board.set_external_trigger(
    coupling=Couplings.DC_COUPLING,
    range=ExternalTriggerRanges.ETR_5V
)

board.set_trigger_time_out(0)

board.set_trigger_delay(0)

board.configure_aux_io(
    mode=AuxIOModes.AUX_OUT_TRIGGER,
    parameter=0
)


# Create buffers
memory_size, bits_per_sample = board.get_channel_info()
bytes_per_sample = (bits_per_sample + 7)//8

bytes_per_record = nchannels_active * bytes_per_sample * samples_per_record
bytes_per_buffer = bytes_per_record * records_per_buffer

buffers = []
for _ in range(buffer_count):
    buffer =  Buffer(board, bytes_per_sample, bytes_per_buffer)
    buffers.append(buffer)


# Get board ready for acquisition
board.set_record_size(pre_trigger_samples=0, post_trigger_samples=samples_per_record)

channel_mask = [c*Channels.from_int(i).value for i,c in enumerate(channels)]
channel_mask = sum(channel_mask)
flags = ADMAModes.ADMA_TRADITIONAL_MODE.value | ADMAFlags.ADMA_EXTERNAL_STARTCAPTURE.value 
board.before_async_read(
    channels=channel_mask,
    transfer_offset=0, # pre-trigger values
    samples_per_record=samples_per_record,
    records_per_buffer=records_per_buffer,
    records_per_acquisition=0x7FFFFFFF, #buffers_to_acquire*records_per_buffer,
    flags=flags
)

# Post buffers
for buffer in buffers:
    board.post_async_buffer(
        buffer=buffer._addr, 
        bufferLength=buffer.size_bytes
    )
    
# Begin acquiring
try:
    buffers_completed = 0
    
    board.start_capture()

    t0 = time.perf_counter()
    t_cap0 = t0

    while buffers_completed < buffers_to_acquire:
        buffer_idx = buffers_completed % buffer_count
        buffer:Buffer = buffers[buffer_idx]


        t_w = time.perf_counter()
        board.wait_async_buffer_complete(buffer._addr)
        print(time.perf_counter()-t_w)
        buffers_completed += 1

        # Copy data and repost buffer
        #tmp_data = np.array(buffer.buffer)
        board.post_async_buffer(
            buffer=buffer._addr, 
            bufferLength=buffer.size_bytes
        )

        # Process data
        #p = np.mean(tmp_data)
        p=0
        t = time.perf_counter()
        dt = t-t0
        data_rate = bytes_per_buffer/dt/1024/1024
        t0 = t
        print(f"Mean of buffer {buffers_completed-1}: {p} ({data_rate:.1f} MB/s)")

except:
    pass
    
dt_cap = time.perf_counter() - t_cap0
print(f"Acquisition done, took {dt_cap} sec ({buffers_to_acquire*records_per_buffer/dt_cap} trigs/sec))")
# Clean up
board.abort_async_read()
