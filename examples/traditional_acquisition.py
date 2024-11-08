from atsbindings import Board, Buffer, Ats


# Parameters
channels = [True, True] # [channel A, channel B, etc] (extend for >2 channel boards)
input_ranges = [2.0, 2.0] # +/- V (match size of channels list) (each must match one of the available input ranges)
sample_rate = 20e6 # must match one of the available internally generated sample rates
samples_per_record = 2048
records_per_buffer = 128
buffers_to_acquire = 8
buffer_count = 8
trigger_source = Ats.TriggerSources.TRIG_EXTERNAL
include_headers = True # Required for timestamps
interleave_samples = False # Required for high-performance, but not supported on all boards

# Initialize board, set acquisition parameters
board = Board()

board.set_capture_clock(
    source=Ats.ClockSources.INTERNAL_CLOCK,
    rate=Ats.SampleRates.from_hz(sample_rate)
)

nchannels_present = len(channels)
nchannels_active = sum(channels)
for i in range(nchannels_present):
    board.input_control_ex(
        channel=Ats.Channels.from_int(i),
        coupling=Ats.Couplings.DC_COUPLING,
        input_range=Ats.InputRanges.from_v(input_ranges[i]),
        impedance=Ats.Impedances.IMPEDANCE_50_OHM,
    )

board.set_trigger_operation(
    operation=Ats.TriggerOperations.TRIG_ENGINE_OP_J,
    engine1=Ats.TriggerEngines.TRIG_ENGINE_J,
    source1=trigger_source,
    slope1=Ats.TriggerSlopes.TRIGGER_SLOPE_POSITIVE,
    level1=128,
    engine2=Ats.TriggerEngines.TRIG_ENGINE_K,
    source2=Ats.TriggerSources.TRIG_DISABLE,
    slope2=Ats.TriggerSlopes.TRIGGER_SLOPE_POSITIVE,
    level2=192
)

board.set_external_trigger(
    coupling=Ats.Couplings.DC_COUPLING,
    range=Ats.ExternalTriggerRanges.ETR_5V
)

board.set_trigger_time_out(0) # setting 0 makes digitizer wait for trigger (like 'Normal' triggering)

board.set_trigger_delay(0)

board.configure_aux_io(
    mode=Ats.AuxIOModes.AUX_OUT_TRIGGER,
    parameter=0
)


# Create buffers
buffers = []
for _ in range(buffer_count):
    buffer = Buffer(board, nchannels_active, records_per_buffer, 
                    samples_per_record, 
                    include_header=include_headers,
                    interleave_samples=interleave_samples)
    buffers.append(buffer)


# Get board ready for acquisition
board.set_record_size(pre_trigger_samples=0, post_trigger_samples=samples_per_record)

channel_mask = sum([c*Ats.Channels.from_int(i) for i,c in enumerate(channels)])

flags = Ats.ADMAModes.ADMA_TRADITIONAL_MODE | Ats.ADMAFlags.ADMA_EXTERNAL_STARTCAPTURE 
if include_headers:
    flags = flags | Ats.ADMAFlags.ADMA_ENABLE_RECORD_HEADERS
if interleave_samples:
    flags = flags | Ats.ADMAFlags.ADMA_INTERLEAVE_SAMPLES

board.before_async_read(
    channels=channel_mask,
    transfer_offset=0, # pre-trigger values
    samples_per_record=samples_per_record,
    records_per_buffer=records_per_buffer,
    records_per_acquisition=buffers_to_acquire*records_per_buffer,
    flags=flags
)

# Post buffers
for buffer in buffers:
    board.post_async_buffer(
        buffer=buffer.address, 
        buffer_length=buffer.size
    )
    
# Begin acquiring
try:
    buffers_completed = 0
    
    board.start_capture()

    while buffers_completed < buffers_to_acquire:
        buffer_idx = buffers_completed % buffer_count
        buffer:Buffer = buffers[buffer_idx]

        board.wait_async_buffer_complete(buffer.address)
        buffers_completed += 1

        # Check headers
        if include_headers:
            include_headers = buffer.get_headers()
            print("Record #:", include_headers[0].hdr1.RecordNumber, "Timestamp:", include_headers[0].hdr2.TimeStampLowPart)

        # Copy data, repost buffer
        tmp_data = buffer.get_data()
        print(tmp_data.shape)

        board.post_async_buffer(
            buffer=buffer.address, 
            buffer_length=buffer.size
        )


except Exception as e:
    print("An error occurred:", e)

finally:
    board.abort_async_read()


print(f"Acquisition done")

try:
    import matplotlib.pyplot as plt
except:
    print("Matplot lib not installed. Skipping plotting.")
    exit()

fig,ax = plt.subplots()

for c in range(nchannels_active):
    if interleave_samples:
        ax.plot(tmp_data[0,:,c])
    else:
        ax.plot(tmp_data[0,c,:])
plt.show()