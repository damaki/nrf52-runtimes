# This script extends bb-runtimes to define the nRF52 targets

import sys
import os
import pathlib

# Add bb-runtimes to the search path so that we can include and extend it
sys.path.append(str(pathlib.Path(__file__).parent / "bb-runtimes"))

import arm.cortexm
import build_rts
from support import add_source_search_path

class NRF52(arm.cortexm.ArmV7MTarget):
    @property
    def name(self):
        return 'nRF52'

    @property
    def parent(self):
        return arm.cortexm.CortexMArch

    @property
    def loaders(self):
        return ('ROM', )

    @property
    def has_fpu(self):
        return True

    @property
    def system_ads(self):
        # Use custom System package since system-xi-cortexm4 assumes
        # 4-bit interrupt priorities, but the nRF52 only supports
        # 3-bit interrupt priorities. This requires different
        # definitions for Priority and Interrupt_Priority in System.
        return {'light': 'system-xi-arm.ads',
                'light-tasking': 'nrf52_src/system-xi-nrf52-sfp.ads',
                'embedded': 'nrf52_src/system-xi-nrf52-full.ads'}

    @property
    def compiler_switches(self):
        # The required compiler switches
        return ('-mlittle-endian', '-mthumb', '-mfloat-abi=hard',
                '-mfpu=fpv4-sp-d16', '-mcpu=cortex-m4')

    def __init__(self):
        super(NRF52, self).__init__()

        self.add_linker_script('nrf52_src/common-ROM.ld', loader='ROM')
        self.add_linker_script('nrf52_src/memory-map_%s.ld' % self.name,
                               'memory-map.ld')

        self.add_gnat_sources(
            "nrf52_src/s-bbbopa.ads",
            'nrf52_src/s-bbmcpa.ads',
            'nrf52_src/start-common.S',
            'nrf52_src/start-rom.S',
            'nrf52_src/setup_board.ads')

        self.add_gnarl_sources(
            'nrf52_src/s-bbpara.ads',
            'nrf52_src/s-bbbosu.adb',
            'src/s-bcpcst__pendsv.adb')


class NRF52833(NRF52):
    @property
    def name(self):
        return "nrf52833"

    @property
    def use_semihosting_io(self):
        return True

    def __init__(self):
        super(NRF52833, self).__init__()

        self.add_gnat_sources(
            "nrf52_src/nrf52833/setup_board.adb",
            "nrf52_src/nrf52833/svd/i-nrf52.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-clock.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-ficr.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-gpio.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-uicr.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-nvmc.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-rtc.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-uart.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-temp.ads",
            "nrf52_src/nrf52833/svd/i-nrf52-approtect.ads",
        )

        # ravenscar support
        self.add_gnarl_sources(
            "nrf52_src/nrf52833/svd/handler.S",
            "nrf52_src/nrf52833/svd/a-intnam.ads",
        )


class NRF52840(NRF52):
    @property
    def name(self):
        return 'nrf52840'

    @property
    def use_semihosting_io(self):
        return True

    def __init__(self):
        super(NRF52840, self).__init__()

        self.add_gnat_sources(
            'nrf52_src/nrf52840/setup_board.adb',
            'nrf52_src/nrf52840/svd/i-nrf52.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-ccm.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-clock.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-ficr.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-gpio.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-uicr.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-nvmc.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-rtc.ads',
            'nrf52_src/nrf52840/svd/i-nrf52-temp.ads')
        self.add_gnarl_sources(
            'nrf52_src/nrf52840/svd/handler.S',
            'nrf52_src/nrf52840/svd/a-intnam.ads')


class NRF52832(NRF52):
    @property
    def name(self):
        return 'nrf52832'

    @property
    def use_semihosting_io(self):
        return True

    def __init__(self):
        super(NRF52832, self).__init__()

        self.add_gnat_sources(
            'nrf52_src/nrf52832/setup_board.adb',
            'nrf52_src/nrf52832/svd/i-nrf52.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-clock.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-ficr.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-gpio.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-uicr.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-nvmc.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-rtc.ads',
            'nrf52_src/nrf52832/svd/i-nrf52-temp.ads')

        self.add_gnarl_sources(
            'nrf52_src/nrf52832/svd/handler.S',
            'nrf52_src/nrf52832/svd/a-intnam.ads')

def build_configs(target):
    if target == "nrf52832":
        return NRF52832()
    elif target == "nrf52833":
        return NRF52833()
    elif target == "nrf52840":
        return NRF52840()
    else:
        assert False, "unexpected target: %s" % target

def patch_bb_runtimes():
    """Patch some parts of bb-runtimes to use our own targets and data"""
    add_source_search_path(os.path.dirname(__file__))

    build_rts.build_configs = build_configs

if __name__ == "__main__":
    patch_bb_runtimes()
    build_rts.main()