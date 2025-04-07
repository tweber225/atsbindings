# atsbindings
Python bindings for the [AlazarTech C API](https://docs.alazartech.com/ats-sdk-user-guide/latest/index.html) built using [ctypes](https://docs.python.org/3/library/ctypes.html). This library provides a relatively thin layer over the C API, offering direct function mapping. In prinicple, all AlazarTech boards are supported; however, please see the **Board Notes** section below for tested models and specific quirks.

Developers familiar with the AlazarTech API can get started quickly. For those with limited experience, it is recommended to read the official API [Programmer's Guide](https://docs.alazartech.com/ats-sdk-user-guide/latest/programmers-guide.html) and review the [acquisition.py](examples/acquisition.py) example to understand how the bindings translate into Python.

## Design
- **Pythonic Naming Convention:**\
  C API functions are renamed to follow Python conventions with the leading "Alazar" namespace removed. For example:
  - `AlazarSetCaptureClock()` → `set_capture_clock()`
- **`Board` Class:**\
  Functions requiring a board handle as the first argument are grouped into a `Board` class. This class automatically manages the board handle.
- **`Buffer` Class:**\
  Simplifies configuration for AutoDMA transfer by automatically setting up a ctypes array of the correct type and size. Includes:
  - Methods for converting acquired data to a NumPy array.
  - Support for interleaved channels.
  - Support for 12-bit unpacking (currently slow).
- **Enumerations:**\
  Enumerations (under the `Ats` namespace) include helper methods to:
  - Convert to and from string representations.
  - Create values from integer and floating-point inputs.\
    Example:
    ```
    >>> from atsbindings import Ats
    >>> sample_rate = 250e6
    >>> Ats.SampleRates.from_hertz(2 * sample_rate)
    <SampleRates.SAMPLE_RATE_500MSPS: 48>
    ```
- **`BoardSpecificInfo`:**\
  Provides board-specific parameters and feature details, as described in the [API documentation](https://docs.alazartech.com/ats-sdk-user-guide/latest/board-specific-info.html).\
  See the [get_board_specific_info.py](examples/get_board_specific_info.py) example for usage.
- **`System` Class:**\
  Offers system-level information such as:
  - Number of boards detected.
  - DLL versions.
  - Other global properties.

## Features Not Included
- **High-Level API:**\
  A more pythonic interface is beyond the scope of this wrapper package. See the [Dirigo plugin](https://github.com/dirigo-developers/dirigo-alazar) for a higher level API.
- **Single-Port Acquisitions:**\
  Deprecated, lower-performance data transfer method.
- **Linux Support:**\
  Currently, this library supports Windows only.
- **Miscellaneous Functions:**\
  Some less commonly used functions have been omitted for clarity. Contact [TDW](https://github.com/tweber225) if you need something not currently available.

## Limitations
While this library closely wraps the C API, the Python interpreter introduces some overhead that may affect performance in certain scenarios. To minimize this impact:
- Limit the frequency of wrapper calls.
- Use relatively large buffer sizes for data transfer. ([Alazar documentation](https://docs.alazartech.com/ats-sdk-user-guide/latest/reference/AlazarBeforeAsyncRead.html) suggest setting the buffer size between 1 MB and 16 MB.)

## Installation
1. **Install the Digitizer Driver:**\
   Download and install the appropriate driver from the AlazarTech [downloads page](https://www.alazartech.com/en/downloads/).
2. **Install Alazar DSO:**\
   Download and install the Alazar DSO software to verify hardware functionality.
3. **Install the Digitizer:**\
   Power down the computer, install the digitizer in an appropriate extension slot, and power up.
4. **Test with Alazar DSO:**\
   Run Alazar DSO to confirm the card is functioning correctly. _If the card does not work in DSO, it will not work with `atsbindings`_!
5. **Install `atsbindings`:**\
   Install atsbindings from PyPI (or clone this repository and install it with pip). Using a virtual environment manager such as Conda is recommended.
6. **Run Examples:**\
   Try the example scripts in the [examples](examples/) folder to validate your installation.

## Board Notes
This library has been tested with the following boards:
- **ATS9373:**
  - For 2-channel acquisiton, samples must be interleaved.
  - No Traditional AutoDMA mode on this board.
- **ATS9870:**
  - LED example does not work properly (LED remains alway on).
- **ATS9350**
- **ATS9440**
- **ATS460**

## Contributing
Contributions are welcome! If you encounter an issue, have a feature suggestion, or want to contribute code, please open an issue or submit a pull request.

## Legal Disclaimer
This library is provided "as is" without any warranties, express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, or non-infringement. The authors are not responsible for any damage to hardware, data loss, or other issues arising from the use or misuse of this library. Users are advised to thoroughly test this library with their specific hardware and configurations before deployment.

This library depends on the AlazarTech C API and its associated drivers, which must be installed and configured separately. Compatibility and performance depend on the proper installation and operation of these third-party components.

This library is an independent implementation based on publicly available documentation from AlazarTech. It is not affiliated with, endorsed by, or officially supported by AlazarTech.

Use this library at your own risk. Proper operation of hardware and compliance with applicable laws and regulations is the sole responsibility of the user.

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
