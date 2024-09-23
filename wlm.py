"""
Module to work with High Finesse Angstrom WS7 Wavelength Meter
Or send Dummy data in debug mode
"""

import argparse
import ctypes, random, time, math

DLL_PATH = "C:\Windows\System32\wlmData.dll"

class WavelengthMeter:

    def __init__(self, dllpath=DLL_PATH, debug=False):
        """
        Wavelength meter class.
        Argument: Optional path to the dll. Default: "C:\Windows\System32\wlmData.dll"
        """
        self.channels = []
        self.dllpath = dllpath
        self.debug = debug
        if not debug:
            self.dll = ctypes.WinDLL(dllpath)
            self.dll.GetWavelengthNum.restype = ctypes.c_double
            self.dll.GetFrequencyNum.restype = ctypes.c_double
            self.dll.GetSwitcherMode.restype = ctypes.c_long

    def GetExposureMode(self):
        if not self.debug:
            return (self.dll.GetExposureMode(ctypes.c_bool(0))==1)
        else:
            return True

    def SetExposureMode(self, b):
        if not self.debug:
            return self.dll.SetExposureMode(ctypes.c_bool(b))
        else:
            return 0

    def GetWavelength(self, channel: int=1):
        if not self.debug:
            return self.dll.GetWavelengthNum(ctypes.c_long(channel), ctypes.c_double(0))
        else:
            return []

    def GetFrequency(self, channel: int=1):
        if not self.debug:
            return self.dll.GetFrequencyNum(ctypes.c_long(channel), ctypes.c_double(0))*1000
        else:
            return []

    def GetAll(self):
        return {
            "debug": self.debug,
            "wavelength": self.GetWavelength(),
            "frequency": self.GetFrequency(),
            "exposureMode": self.GetExposureMode()
        }

    @property
    def wavelengths(self):
        return [self.GetWavelength(i + 1) for i in range(8)]

    ## For debugging purposes
    @property
    def wavelength(self):
        return self.GetWavelength(1)

    @property
    def frequencies(self):
        return [self.GetFrequency(i + 1) for i in range(8)]

    @property
    def switcher_mode(self):
        if not self.debug:
            return self.dll.GetSwitcherMode(ctypes.c_long(0))
        else:
            return 0

    @switcher_mode.setter
    def switcher_mode(self, mode):
        if not self.debug:
            self.dll.SetSwitcherMode(ctypes.c_long(int(mode)))
        else:
            pass




# Simulate WavelengthMeter data or use real data (depending on debug mode)
def get_wavemeter_data(wlm):
    
    if wlm.debug:
        base_wavelengths = [460.861, 689.264, 679.289, 707.202, 921.724, 800.0, 650.0, 500.0]
        base_frequencies = [384229.18, 384227.29, 384232.37, 384229.26, 384230.5, 384231.0, 384228.5, 384227.0]
        wavelengths_data = [base + random.uniform(-0.01, 0.01) for base in base_wavelengths]
        frequencies_data = [base + random.uniform(-0.5, 0.5) for base in base_frequencies]

        # Time-dependent triangular scan on wavelength[0]
        current_time = time.time() 
        wavelengths_data[0] = base_wavelengths[0] + triangular_wave(current_time, 0.1, 20)
    else:
        wavelengths_data = wlm.wavelengths
        frequencies_data = wlm.frequencies

    return {
        "wavelengths": wavelengths_data,
        "frequencies": frequencies_data
    }

## Dummuy data generation of triangular wave
def triangular_wave(t, amplitude=0.5, period=10):
    """Generates a triangular wave with the given amplitude and period."""
    return amplitude * (2 / math.pi) * math.asin(math.sin(2 * math.pi * t / period))



if __name__ == '__main__':
    # Command line arguments parsing
    parser = argparse.ArgumentParser(description='Reads out wavelength values from the High Finesse Angstrom WS7 wavemeter.')
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True, default=False,
                        help='Runs the script in debug mode simulating wavelength values')
    parser.add_argument('channels', metavar='ch', type=int, nargs='*',
                        help='Channel to get the wavelength, by default all channels from 1 to 8',
                        default=range(1, 9))

    args = parser.parse_args()

    wlm = WavelengthMeter(debug=args.debug)

    # Print wavelength data for the specified channels
    for i in args.channels:
        print(f"Wavelength at channel {i}:\t{wlm.wavelengths[i-1]:.4f} nm")

    # Example of real data interaction (or simulated)
    data = get_wavemeter_data(wlm)
    print("Wavelengths:", data['wavelengths'])
    print("Frequencies:", data['frequencies'])
