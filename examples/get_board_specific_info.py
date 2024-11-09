from atsbindings import Board, Ats


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
      + f"which may be sampled at rates as low as {sample_rates[0]} " 
      + f"or as high as {sample_rates[-1]}."
)

# Get available input impedances
impedances = [str(i) for i in bsi.input_impedances]
print(f"Input impedance options: {', '.join(impedances)}")

# Get input ranges for first available impedance
ranges = bsi.input_ranges(bsi.input_impedances[0])
input_ranges = [str(v) for v in ranges]
if len(input_ranges) == 1:
      print(f"With input impedance {impedances[0]}, the fixed input range" 
            + f" is {input_ranges[0]}")
else:
      print(f"With input impedance {impedances[0]}, the narrowest input range" 
            + f" is {input_ranges[0]} and widest is {input_ranges[-1]}")

# Get the external trigger ranges
etr = bsi.external_trigger_ranges
print(f"The external trigger ranges are {', '.join([r.name[4:] for r in etr])}")

# Get supported external clock types and ranges if available
clks = bsi.supported_external_clocks
if len(clks) > 0:
    print(f"The supported external clocks are {', '.join([c.name for c in clks])}")
    eclk_range = bsi.external_clock_frequency_ranges(clks[0])
    print(f"The supported frequency range for {clks[0].name} is {eclk_range.min} to {eclk_range.max}")
else:
    print("This board does not support external clocking")
