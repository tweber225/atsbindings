from atsbindings import Board, Ats

"""
Example shows how to retrieve board-specific information, alogn with other 
parameters such as board serial number, bits per sample, and memory size.
"""

# Initialize first board/subsystem and report the model number ('kind')
board = Board()
board_kind = board.get_board_kind()
sn = board.query_capability(Ats.Capabilities.GET_SERIAL_NUMBER)
print(f"Board model: {board_kind.name} (S/N: {sn})")

# Get board specific info
bsi = board.bsi

# Get available internal clock sample rates
sample_rates = [str(r) for r in bsi.sample_rates]
print(f"This board features {board.bsi.channels} channels, "
      f"which may be sampled at rates as low as {sample_rates[0]} " 
      f"or as high as {sample_rates[-1]}."
)

# Get selectable BW filter
if bsi.bandwidth_limit:
    print("The board features a software-selectable bandwidth limiting filter.")
else:    
    print("The board does not feature a software-selectable bandwidth limiting filter.")

# Get input couplings
couplings = [str(c) for c in bsi.input_couplings]
print(f"Input coupling options: {', '.join(couplings)}")

# Get data packing options
packings = [str(p) for p in bsi.data_packings][1:] # Skip first option which is default non-packed
if len(packings) > 0:
    print(f"Data packing options: {', '.join(packings)}")
else:
    print("The board does not support data packing")

# Get available input impedances
impedances = [str(i) for i in bsi.input_impedances]
print(f"Input impedance options: {', '.join(impedances)}")

# Get input ranges for first available impedance
ranges = bsi.input_ranges(bsi.input_impedances[0])
input_ranges = [str(v) for v in ranges]
if len(input_ranges) == 1:
    print(f"With input impedance {impedances[0]}, the fixed input range" 
          f" is {input_ranges[0]}")
else:
    print(f"With input impedance {impedances[0]}, the narrowest input range" 
          f" is {input_ranges[0]} and widest is {input_ranges[-1]}")

# Get the external trigger ranges
etr = bsi.external_trigger_ranges
print(f"The external trigger ranges are {', '.join([r.name[4:] for r in etr])}")

# Get supported clock types and ranges if available
clks = bsi.supported_clocks
print(f"The supported clocks are {', '.join([str(c) for c in clks])}")
if len(clks) > 1:
    eclk_range = bsi.external_clock_frequency_ranges(clks[1])
    print(f"The supported frequency range for "
          f"{clks[1]} is {eclk_range.min} to {eclk_range.max}")

# Record size limitations
samples_per_channel, sample_size = board.get_channel_info()
print(f"The sample resolution is {sample_size} and the board contains memory for {round(samples_per_channel/2**20)} megasamples.")
print(f"The minimum record size is {bsi.min_record_size} and can be increased "
      f"in increments of {bsi.record_resolution}.")

