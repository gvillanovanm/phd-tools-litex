# --sys-clk-freq=$(SYS_CLK_FREQ) \
# --uart-baudrate=$(UART_BAUDRATE) \
CPU_RST_ADDR    = # --cpu-reset-address CPU_RESET_ADDRESS
# Output Directories
# OUTPUT_DIR     ?= vexriscv_lite_sim
# GATEWARE_DIR   ?= $(OUTPUT_DIR)/gateware

# ----------------------------------------------------------------------
# for SIMULATION, maybe we need to use the same thing but using litex_sim
# ----------------------------------------------------------------------
# cmd: litex_sim --integrated-main-ram-size=0x10000 --cpu-type=vexriscv --no-compile-gateware 
# Notes:
# * The --no-compile-gateware option is used to skip the gateware compilation step, which are
#   not necessary since we are just preparing the SoC here for bare-metal demo compilation.
# * Integrated-main-ram-size is very import to avoid DRAM, the DPU will be like this.

# Config
CPU_TYPE     =vexriscv # Options: vexriscv, picorv32, etc.
CPU_VARIANT  =lite     # Options: standard, lite, full, etc.
CPU_INT_RAM  =0x10000

soc_sim:
	litex_sim \
	--integrated-main-ram-size=$(CPU_INT_RAM) \
	--cpu-type=$(CPU_TYPE) \
	--no-compile-gateware

soc_sim_sw:
	litex_bare_metal_demo --build-path=sw/sim/

soc_sim_sw_comp:
	make -C sw

soc_sim_run:
	litex_sim --integrated-main-ram-size=0x10000 --cpu-type=vexriscv --ram-init=sw/main.bin

# custom?

# --cpu-variant=$(CPU_VARIANT) \
	--output-dir=$(OUTPUT_DIR) \
	--gateware-dir=$(GATEWARE_DIR) \
	--software-dir=$(SOFTWARE_DIR) \
	--doc

# ----------------------------------------------------------------------
# SoC GEN
# ----------------------------------------------------------------------
soc_gen:
	litex_soc_gen 					\
	--cpu-type=$(CPU_TYPE) 			\
	--cpu-variant=$(CPU_VARIANT) 	\
	--output-dir=$(OUTPUT_DIR)		\
	--gateware-dir=$(GATEWARE_DIR)  \
	--software-dir=$(SOFTWARE_DIR)  \
	--doc

# ----------------------------------------------------------------------
# for FPGA
# ----------------------------------------------------------------------
PYTHON_TARGET=/litex/litex-boards/litex_boards/targets/digilent_arty.py
fpga_gen:
	$(PYTHON_TARGET) --output-dir=fpga_gen_try --build