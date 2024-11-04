run:
	@echo 'Open the Makefile and see the cmds'
	
mkdir_build:
	@if [ ! -d "build" ]; then \
		echo "Creating build directory..."; \
		mkdir build; \
	else \
		echo "Build directory already exists."; \
	fi

for_sim: mkdir_build
	litedram_gen arty.yml --sim --gateware-dir rtl --software-dir sw --name litedram

for_fpga: mkdir_build
	litedram_gen arty.yml --gateware-dir rtl --software-dir sw --name litedram

help:
	litedram_gen --help

bl_tpl_sim: mkdir_build
# litedram_gen arty_boxlambd.yml --sim --gen_user_clkx2 --gateware-dir sim/rtl --software-dir sim/sw --name litedram
# --gen_user_clkx2 (unreconized)
	litedram_gen arty_boxlambd.yml --sim --gateware-dir sim/rtl --software-dir sim/sw --name litedram # for sim

bl_tpl_fpga: mkdir_build
	litedram_gen arty_boxlambd.yml --gateware-dir arty/rtl --software-dir arty/sw --name litedram # for fpga

# ------------------------------------------------------------------------
# Verilator
# ------------------------------------------------------------------------
ver_sim:
	verilator --cc ./litedram.v --exe sim_init.cpp --trace

ver_sim_b:
	make -j -C obj_dir -f Vlitedram.mk Vlitedram

# ------------------------------------------------------------------------
# QUESTA
# ------------------------------------------------------------------------
csim:
	vlog rtl/litedram.v rtl/litedram_tb.sv

vsim: csim
	vsim -batch -do "run -all" work.litedram_tb

vsim_gui: csim
	vsim -debugdb


# ------------------------------------------------------------------------
# Clean
# ------------------------------------------------------------------------
clean:
	rm -rf rtl sw work build