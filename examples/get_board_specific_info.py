from atsbindings.bindings import Board


# Initialize first board/subsystem and report the model number ('kind')
board = Board()
board_kind = board.get_board_kind()
print(f"Board model: {board_kind.name}")

# Get board specific info
bsi = board.bsi
sample_rates = [str(r) for r in bsi.sample_rates]
print(f"This board features {board.bsi.channels} channels, "
      + f"which may be sampled at rates as low as {sample_rates[0]} " 
      + f"or as high as {sample_rates[-1]}."
)

impedances = [str(i.in_ohms)+" ohms" for i in bsi.input_impedances]
print(f"Input impedance options: {', '.join(impedances)}")

ranges = bsi.input_ranges(bsi.input_impedances[0])
input_ranges = [str(v) for v in ranges]
print(f"With input impedance {impedances[0]}, the narrowest input range" 
      + f" is {input_ranges[0]} and widest is {input_ranges[-1]}")

etr = bsi.external_trigger_ranges
print(f"The external trigger ranges are {', '.join([r.name[4:] for r in etr])}")

clks = bsi.supported_clocks
print(f"The supported clocks are {', '.join([c.name for c in clks])}")

if len(clks) > 1:
    eclk_range = bsi.external_clock_frequency_range(clks[1])
    print(f"The supported frequency range for {clks[1].name} is {eclk_range[0]} to {eclk_range[1]}")
else:
    print("This board does not support external clocking")