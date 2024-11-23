from atsbindings import Board, Buffer, Ats


# Parameters
channels = [True, True] # [channel A, channel B, etc] (extend for >2 channel boards)
input_ranges = [0.4, 0.4] # +/- V (match size of channels list) (each must match one of the available input ranges)
sample_rate = 20e6 # Hz, must match one of the available internally generated sample rates
samples_per_record = 1024
records_per_buffer = 128
buffers_to_acquire = 4
buffer_count = 4
trigger_source = Ats.TriggerSources.TRIG_EXTERNAL
acquisition_mode = Ats.ADMAModes.ADMA_TRADITIONAL_MODE
enable_headers = True # Required for timestamps in Traditional ADMA mode
enable_footers = False # Required for timestamps in NPT ADMA mode
interleave_samples = False # Required for high-performance, but not supported on all boards
data_packing = Ats.PackModes.PACK_DEFAULT # Check whether board supports packing modes


if enable_headers:
    assert acquisition_mode == Ats.ADMAModes.ADMA_TRADITIONAL_MODE, \
        "Headers are only available in Traditional Mode"
if enable_footers:
    assert acquisition_mode == Ats.ADMAModes.ADMA_NPT, \
        "Footers are only available in NPT Mode"
    assert data_packing == Ats.PackModes.PACK_DEFAULT, \
        "Footers are not available in data packing modes."
if data_packing == Ats.PackModes.PACK_12_BITS_PER_SAMPLE:
    assert interleave_samples, "12-bit packing mode only supported with interleaved samples"

# Initialize board, set acquisition parameters
board = Board()

board.set_capture_clock(
    source=Ats.ClockSources.INTERNAL_CLOCK,
    rate=Ats.SampleRates.from_hertz(sample_rate)
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
    range=Ats.ExternalTriggerRanges.ETR_2V5
)

board.set_trigger_time_out(0) # setting 0 makes digitizer wait for trigger (like 'Normal' triggering)

board.set_trigger_delay(0)

board.configure_aux_io(
    mode=Ats.AuxIOModes.AUX_OUT_TRIGGER,
    parameter=0
)

# Set data packing
board.set_parameter(
    Ats.Channels.CHANNEL_ALL, Ats.Parameters.PACK_MODE, data_packing
)

# Create buffers
buffers = []
for _ in range(buffer_count):
    buffer = Buffer(
        board, 
        nchannels_active, 
        records_per_buffer, 
        samples_per_record, 
        enable_headers,
        enable_footers,
        interleave_samples,
        data_packing
    )
    buffers.append(buffer)


# Get board ready for acquisition
board.set_record_size(pre_trigger_samples=0, post_trigger_samples=samples_per_record)

channel_mask = sum([c*Ats.Channels.from_int(i) for i,c in enumerate(channels)])

flags = Ats.ADMAFlags.ADMA_EXTERNAL_STARTCAPTURE | acquisition_mode
if enable_headers:
    flags = flags | Ats.ADMAFlags.ADMA_ENABLE_RECORD_HEADERS
if enable_footers:
    flags = flags | Ats.ADMAFlags.ADMA_ENABLE_RECORD_FOOTERS
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
        if enable_headers:
            headers = buffer.get_headers()
            print("Record #:", headers[0].record_number, ", Timestamp:", headers[0].timestamp)

        # Check footers
        if enable_footers:
            footers = buffer.get_footers()
            print("Record #:", footers[0].record_number, ", Timestamp:", footers[0].timestamp)

        # Copy data, repost buffer
        tmp_data = buffer.get_data()

        board.post_async_buffer(
            buffer=buffer.address, 
            buffer_length=buffer.size
        )


except Exception as e:
    print("An error occurred:", e)

finally:
    board.abort_async_read()


print(f"Acquisition done")


# Optional plotting
try:
    import matplotlib.pyplot as plt
except:
    print("Matplotlib not installed. Skipping plotting.")
    exit()

fig,ax = plt.subplots()

for c in range(nchannels_active):
    if interleave_samples:
        ax.plot(tmp_data[0,:,c])
    else:
        ax.plot(tmp_data[0,c,:])
plt.show()