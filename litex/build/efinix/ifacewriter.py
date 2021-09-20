import os
from litex.build import tools

class InterfaceWriter():
    def __init__(self, filename, efinity_path):
        self.file = filename
        self.efinity_path = efinity_path
        self.blocks = []

    def header(self, build_name, partnumber):
        header = "# Autogenerated by LiteX / git: " + tools.get_litex_git_revision()
        header += """
import os
import sys
import pprint

home = '{0}'

os.environ['EFXPT_HOME']  = home + '/pt'
os.environ['EFXPGM_HOME'] = home + '/pgm'
os.environ['EFXDBG_HOME'] = home + '/debugger'
os.environ['EFXIPM_HOME'] = home + '/ipm'

sys.path.append(home + '/pt/bin')
sys.path.append(home + '/lib/python3.8/site-packages')

from api_service.design import DesignAPI
from api_service.device import DeviceAPI

is_verbose = {1}

design = DesignAPI(is_verbose)
device = DeviceAPI(is_verbose)

design.create('{2}', '{3}', './../build', overwrite=True)

"""
        return header.format(self.efinity_path, 'True', build_name, partnumber)

    def get_block(self, name):
        for b in self.blocks:
            if b['name'] == name:
                return b
        return None

    def generate_pll(self, block, verbose=True):
        name = block['name']
        cmd = '# ---------- PLL {} ---------\n'.format(name)
        cmd += 'design.create_block("{}", block_type="PLL")\n'.format(name)
        cmd += 'design.gen_pll_ref_clock("{}", pll_res="{}", refclk_src="{}", refclk_name="{}", ext_refclk_no="{}")\n\n' \
               .format(name, block['resource'], block['input_clock'], block['input_clock_name'], block['clock_no'])

        cmd += 'pll_config = {{ "REFCLK_FREQ":"{}" }}\n'.format(block['input_freq'] / 1e6)
        cmd += 'design.set_property("{}", pll_config, block_type="PLL")\n\n'.format(name)

         # Output clock 0 is enabled by default
        for i, clock in enumerate(block['clk_out']):
            if i > 0:
                cmd += 'pll_config = {{ "CLKOUT{}_EN":"1", "CLKOUT{}_PIN":"{}" }}\n'.format(i, i, clock[0])
                cmd += 'design.set_property("{}", pll_config, block_type="PLL")\n\n'.format(name)

        cmd += 'target_freq = {\n'
        for i, clock in enumerate(block['clk_out']):
            cmd += '    "CLKOUT{}_FREQ": "{}",\n'.format(i, clock[1] / 1e6)
            cmd += '    "CLKOUT{}_PHASE": "{}",\n'.format(i, clock[2])
        cmd += '}\n'
        cmd += 'calc_result = design.auto_calc_pll_clock("{}", target_freq)\n\n'.format(name)


        if verbose:
            cmd += 'print("#### {} ####")\n'.format(name)
            cmd += 'clksrc_info = design.trace_ref_clock("{}", block_type="PLL")\n'.format(name)
            cmd += 'pprint.pprint(clksrc_info)\n'
            cmd += 'clock_source_prop = ["REFCLK_SOURCE", "EXT_CLK", "CLKOUT0_EN", "CLKOUT1_EN","REFCLK_FREQ", "RESOURCE"]\n'
            cmd += 'clock_source_prop += ["M", "N", "O", "CLKOUT0_DIV", "CLKOUT2_DIV", "VCO_FREQ", "PLL_FREQ"]\n'
            cmd += 'prop_map = design.get_property("{}", clock_source_prop, block_type="PLL")\n'.format(name)
            cmd += 'pprint.pprint(prop_map)\n'

        cmd += '# ---------- END PLL {} ---------\n\n'.format(name)
        return cmd

    def generate(self):
        output = ''
        for b in self.blocks:
            if b['type'] == 'PLL':
                output += self.generate_pll(b)
        return output

    def footer(self):
        return """
# Check design, generate constraints and reports
#design.generate(enable_bitstream=True)
# Save the configured periphery design
design.save()"""

