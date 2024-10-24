import requests
import toml
import tomllib
import re
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

from atsbindings.enumerations import *



class BoardSpecificInfo:
    def __init__(self, board_kind):
        if hasattr(board_kind, "name"):
            board_kind = board_kind.name

        # Open and read the TOML file
        fn = Path(__file__).parent / "board_specific_info.toml"
        with open(fn, "rb") as f:
            bsi = tomllib.load(f)

        self.channels:int = bsi[board_kind]["channels"]
        self._input_ranges:dict = bsi[board_kind]["input_ranges"]
        self.min_record_size:int = bsi[board_kind]["min_record_size"]
        self.pretrig_alignment:int = bsi[board_kind]["pretrig_alignment"]
        self.record_resolution:int = bsi[board_kind]["record_resolution"]
        self.max_npt_pretrig_length:int = bsi[board_kind]["max_npt_pretrig_length"]
        self._samples_per_timestamp:dict = bsi[board_kind]["samples_per_timestamp"]
        self._channel_configs:list = bsi[board_kind]["channel_configs"]
        self._sample_rates:list = bsi[board_kind]["sample_rates"]
        self._external_trigger_ranges:list = bsi[board_kind]["external_trigger_levels"]
        self._external_clock_frequency_limits:dict = bsi[board_kind]["external_clock_frequency_limits"]

    @property
    def input_impedances(self):
        imp_keys = self._input_ranges.keys()
        imp_values = []
        for key in imp_keys:
            imp_values.append(int(re.findall(r"\d+", key)[0]))
        return [Impedances.from_ohms(f) for f in imp_values]
    
    def input_ranges(self, impedance:Impedances) -> list[InputRanges]:
        ranges = self._input_ranges[f"{impedance.in_ohms}ohm"]
        ranges_v = []
        for r in ranges:
            v,u = re.findall(r"±(\d+)(mV|V)", r)[0]
            if u == "mV":
                ranges_v.append(float(v)*1e-3)
            elif u == "V":
                ranges_v.append(float(v))
        return [InputRanges.from_v(v) for v in ranges_v]
    
    def samples_per_timestamp(self, active_channels:int):
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
        rates = self._sample_rates
        rates_hz = []
        for rate in rates:
            v,u = re.findall(r"(\d+)(kS/s|MS/s)", rate)[0]
            if u == "kS/s":
                rates_hz.append(float(v)*1e3)
            elif u == "MS/s":
                rates_hz.append(float(v)*1e6)
        return [SampleRates.from_hz(v) for v in rates_hz]
    
    @property
    def external_trigger_ranges(self):
        external_trigger_ranges = []
        for etl in self._external_trigger_ranges:
            if etl == "5 V":
                external_trigger_ranges.append(ExternalTriggerRanges.ETR_5V)
            elif etl == "1 V":
                external_trigger_ranges.append(ExternalTriggerRanges.ETR_1V)
            if etl == "TTL":
                external_trigger_ranges.append(ExternalTriggerRanges.ETR_TTL)
            if etl == "2.5 V":
                external_trigger_ranges.append(ExternalTriggerRanges.ETR_2V5)
        return external_trigger_ranges
    
    @property
    def supported_clocks(self):
        ext_clocks = [ClockSources.INTERNAL_CLOCK] # they all suport internal clock
        for eclock in self._external_clock_frequency_limits.keys():
            if eclock == "Fast":
                ext_clocks.append(ClockSources.FAST_EXTERNAL_CLOCK)
            elif eclock == "Medium":
                ext_clocks.append(ClockSources.MEDIUM_EXTERNAL_CLOCK)
            elif eclock == "Slow":
                ext_clocks.append(ClockSources.SLOW_EXTERNAL_CLOCK)
            elif eclock == "AC":
                ext_clocks.append(ClockSources.EXTERNAL_CLOCK_AC)
            elif eclock == "DC":
                ext_clocks.append(ClockSources.EXTERNAL_CLOCK_DC)
        return ext_clocks
    
    def external_clock_frequency_range(self, clock_source:ClockSources):
        if clock_source == ClockSources.FAST_EXTERNAL_CLOCK:
            return self._external_clock_frequency_limits['Fast']
        elif clock_source == ClockSources.MEDIUM_EXTERNAL_CLOCK:
            return self._external_clock_frequency_limits['Medium']
        elif clock_source == ClockSources.SLOW_EXTERNAL_CLOCK:
            return self._external_clock_frequency_limits['Slow']
        elif clock_source == ClockSources.EXTERNAL_CLOCK_AC:
            return self._external_clock_frequency_limits['AC']
        elif clock_source == ClockSources.EXTERNAL_CLOCK_DC:
            return self._external_clock_frequency_limits['DC']



def update_bsi_file(url="https://docs.alazartech.com/ats-sdk-user-guide/latest/board-specific-info.html"):

    # Fetch the webpage with board-specific info, use BS4 to parse HTML
    response = requests.get(url)
    response.encoding = 'utf-8'
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # INPUT RANGES
    impedance_section = soup.find('section', id='supported-impedances-and-input-ranges')

    # Create a nested defaultdict to store the data
    model_impedance_range = defaultdict(lambda: defaultdict(list))

    # Extract all <dt> and <dd> pairs
    for dt, dd in zip(impedance_section.find_all('dt'), impedance_section.find_all('dd')):
        # Get the model and impedance entries from the <dt> tag
        entries = [entry.strip() for entry in dt.get_text().split(',')]

        # Get the input ranges from the <dd> tag
        ranges = [r.strip() for r in dd.get_text().split(', ')]

        # For each entry, split it into model and impedance
        pattern = r"(\d+)(MΩ|Ω)"
        for entry in entries:
            model, impedance = entry.split('/')
            if "Ω" in impedance:
                d,u = re.findall(pattern, impedance)[0]
                if u == "MΩ":
                    impedance = str(int(float(d)*1e6)) + "ohm"
                else:
                    impedance = d + "ohm"
            # Store the ranges under the appropriate impedance level for each model
            model_impedance_range[model][impedance].extend(ranges)

    # SAMPLES PER RECORD
    samples_section = soup.find('section', id='samples-per-record-requirements')

    # Create a dictionary to store the extracted data
    samples_per_record_requirements = defaultdict(dict)

    # Find the table and iterate over the rows
    table = samples_section.find('table')
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')

        # Extract the board types
        board_models = [model.strip() for model in columns[0].get_text().split(',')]

        # Extract the parameters from the table columns
        min_record_size = int(columns[1].get_text().strip())
        pretrig_alignment = int(columns[2].get_text().strip())
        resolution = int(columns[3].get_text().strip())
        max_npt_pretrig_length = columns[4].get_text().strip()
        if max_npt_pretrig_length != '':
            max_npt_pretrig_length = int(max_npt_pretrig_length)

        # Store the parameters for each board model
        for model in board_models:
            samples_per_record_requirements[model] = {
                'Min Record Size': min_record_size,
                'Pretrig Alignment': pretrig_alignment,
                'Resolution': resolution,
                'Max NPT Pretrig Length': max_npt_pretrig_length or 'N/A'  # Handle empty cells
            }

    # SAMPLE RATES
    sample_rate_section = soup.find('section', id='supported-sample-rates')

    # Create a defaultdict to store the data
    internal_clock_sample_rates = defaultdict(list)

    # Extract all <dt> and <dd> pairs
    for dt, dd in zip(sample_rate_section.find_all('dt'), sample_rate_section.find_all('dd')):
        # Get the digitizer models from the <dt> tag
        models = [model.strip() for model in dt.get_text().split(',')]

        # Get the sample rates from the <dd> tag
        rates = dd.get_text().strip().split(', ')

        # Store the sample rates for each model
        for model in models:
            internal_clock_sample_rates[model].extend(rates)

    # SAMPLES PER TIMESTAMP
    timestamp_section = soup.find('section', id='samples-per-timestamp-and-trigger-delay-alignment')

    # Initialize a dictionary to store the data
    samples_per_timestamp = defaultdict(dict)

    # Locate the table and extract rows
    table = timestamp_section.find('table')
    rows = table.find_all('tr')[2:]  # Skip the header rows

    # Define the channel labels (1 ch., 2 ch., etc.)
    channel_labels = ["1channel", "2channels", "4channels", "8channels", "16channels"]

    # Parse each row to extract board names and their values
    for row in rows:
        cells = row.find_all('td')

        # Extract board names (can be multiple per row)
        boards = [board.strip() for board in cells[0].get_text().split(',')]

        # Extract the samples per timestamp values for each channel
        values = [cell.get_text().strip() or None for cell in cells[1:]]  # Handle empty cells

        # Store data for each board
        for board in boards:
            for i, value in enumerate(values):
                if value is not None:  # Store only non-empty values
                    samples_per_timestamp[board][channel_labels[i]] = int(value)

    # CHANNEL CONFIGURATIONS
    config_section = soup.find('section', id='possible-input-channel-configurations')

    # Initialize a dictionary to store the configurations
    channel_configs = {
        2: [],
        4: [],
        16: []
    }
    possible_channels_per_board = channel_configs.keys()

    # Find the table and extract rows
    table = config_section.find('table')
    rows = table.find_all('tr')[2:]  # Skip the header rows

    # Parse the rows and store configurations
    for row in rows:
        cells = row.find_all('td')

        # Extract the channel configuration name (A, B, A+B, etc.)
        config_name = cells[0].get_text().strip()

        # Check if the configuration is available for each channel count
        for nchannels, cell in zip(possible_channels_per_board, cells[1:]):  # Columns 2, 4, and 16
            if cell.get_text().strip() == '✓':
                bit_code = ['0'] * nchannels  # Start with all bits off

                if '+..+' in config_name:
                    start, end = config_name.split('+..+')
                    # Generate all characters between start and end (inclusive)
                    config_name = ' + '.join(chr(c) for c in range(ord(start.strip()), ord(end.strip()) + 1))
                    
                for char in config_name.replace(' ', '').split('+'):
                    bit_code[ord(char) - ord('A')] = '1'

                bit_code = ''.join(bit_code)

                channel_configs[nchannels].append(bit_code)

    # EXTERNAL TRIGGER LEVEL
    trigger_section = soup.find('section', id='external-trigger-level-support')

    # Define the trigger levels corresponding to the table headers
    trigger_levels = ["1 V", "2.5 V", "5 V", "TTL"]

    # Initialize a dictionary to store the supported trigger levels for each board
    external_trigger_levels = defaultdict(list)

    # Locate the table and iterate over the rows
    table = trigger_section.find('table')
    rows = table.find_all('tr')[1:]  # Skip the header row

    # Parse each row to extract board names and their supported trigger levels
    for row in rows:
        cells = row.find_all('td')

        # Extract the board name
        board_name = cells[0].get_text().strip()

        # Extract and store the supported trigger levels as a list
        for i, cell in enumerate(cells[1:]):  # Iterate over the trigger level columns
            if cell.get_text().strip() == '✓':  # If supported
                external_trigger_levels[board_name].append(trigger_levels[i])

    # EXTERNAL CLOCK FREQUENCY LIMITS
    clock_section = soup.find('section', id='frequency-limits-for-external-clock-types')

    # Define the external clock types
    clock_types = ["Fast", "Medium", "Slow", "AC", "DC"]

    # Initialize a dictionary to store the frequency limits for each board
    external_clock_frequency_limits = defaultdict(lambda: defaultdict(dict))

    # Locate the table and iterate over the rows
    table = clock_section.find('table')
    rows = table.find_all('tr')[2:]  # Skip the header rows

    # Parse each row to extract the board names and frequency limits
    for row in rows:
        cells = row.find_all('td')

        # Extract the board name
        board_name = cells[0].get_text().strip()

        # Extract and store the frequency limits for each clock type
        for i, clock_type in enumerate(clock_types):
            low_freq = cells[1 + 2 * i].get_text().strip()  # Low frequency column
            high_freq = cells[2 + 2 * i].get_text().strip()  # High frequency column
            
            # Store only if there is a valid value
            if low_freq or high_freq:

                if low_freq[-1] == "k":
                    low_freq = int(float(low_freq[:-1])*1e3)
                else: # otherwise it's in MHz
                    low_freq = int(float(low_freq)*1e6)
                if high_freq[-1] == "k":
                    high_freq = int(float(high_freq[:-1])*1e3)
                else: # otherwise it's in MHz
                    high_freq = int(float(high_freq)*1e6)

                external_clock_frequency_limits[board_name][clock_type] = [
                    low_freq if low_freq else None, high_freq if high_freq else None
                ]


    m1 = model_impedance_range.keys()
    m2 = internal_clock_sample_rates.keys()
    m3 = samples_per_timestamp.keys()
    models = list(set(m1) & set(m2) & set(m3))
    models = sorted(models)

    class InlineDict(dict, toml.decoder.InlineTableDict):
        # Flags to save nested dictionary as flat in toml file (less messy)
        pass


    # Make list of board specific info
    bsi = defaultdict()
    for model in models:
        s = list(samples_per_timestamp[model].keys())[-1]
        channels = int(''.join([c for c in s if c.isdigit()]))

        bsi[model] = {
            "channels": channels,
            "input_ranges": InlineDict(model_impedance_range[model]),
            "min_record_size": samples_per_record_requirements[model]['Min Record Size'],
            "pretrig_alignment": samples_per_record_requirements[model]['Pretrig Alignment'],
            "record_resolution": samples_per_record_requirements[model]['Resolution'],
            "max_npt_pretrig_length": samples_per_record_requirements[model]['Max NPT Pretrig Length'],
            "samples_per_timestamp": InlineDict(samples_per_timestamp[model]),
            "channel_configs": channel_configs[channels],
            "sample_rates": internal_clock_sample_rates[model],
            "external_trigger_levels": external_trigger_levels[model],
            "external_clock_frequency_limits": InlineDict(external_clock_frequency_limits[model])
        }

    # Save the board information to a TOML file
    fn = Path(__file__).parent / "board_specific_info.toml"
    with open(fn, "w", encoding="utf-8") as f:
        toml.dump(bsi, f, encoder=toml.TomlPreserveInlineDictEncoder())


#BoardSpecificInfo("ATS9440")
#update_bsi_file()