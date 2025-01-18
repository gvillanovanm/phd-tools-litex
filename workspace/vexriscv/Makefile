# ----------------------------------------------------------------------------------------------
# SIMULATION
# * The --no-compile-gateware option is used to skip the gateware compilation step, which are
#   not necessary since we are just preparing the SoC here for bare-metal demo compilation.
# * Integrated-main-ram-size is very import to avoid DRAM, the DPU will be like this.
# ----------------------------------------------------------------------------------------------

CPU_TYPE     =vexriscv # Options: vexriscv, picorv32, etc.
CPU_VARIANT  =lite     # Options: standard, lite, full, etc.
CPU_INT_RAM  =0x10000

soc_sim:
	litex_sim \
	--integrated-main-ram-size=$(CPU_INT_RAM) \
	--cpu-type=$(CPU_TYPE) \
	--no-compile-gateware

soc_sim_sw:
	@echo "Move this folder and adapt the Makefile generated manually!"
	litex_bare_metal_demo --build-path=sw/sim/

soc_sim_sw_comp:
	make -C sw

soc_sim_run:
	litex_sim \
	--integrated-main-ram-size=$(CPU_INT_RAM) \
	--cpu-type=$(CPU_TYPE) \
	--ram-init=sw/main.bin

# ----------------------------------------------------------------------
#
# FPGA
# 
# ----------------------------------------------------------------------
# PYTHON_TARGET=/litex/litex-boards/litex_boards/targets/digilent_arty.py
PYTHON_TARGET=./digilent_arty.py
fpga_build:
	$(PYTHON_TARGET) \
	--integrated-main-ram-size=$(CPU_INT_RAM) \
	--cpu-type=$(CPU_TYPE) \
	--output-dir=fpga --build

fpga_load:
	$(PYTHON_TARGET) \
	--integrated-main-ram-size=$(CPU_INT_RAM) \
	--cpu-type=$(CPU_TYPE) \
	--output-dir=fpga --load

# load SW from serial and execute it
fpga_load_sw:
	litex_term /dev/ttyUSB1 --speed 115200 --kernel sw/main.bin

fpga_clean:
	rm -rf fpga

# --sys-clk-freq=$(SYS_CLK_FREQ) \
# --uart-baudrate=$(UART_BAUDRATE) \
CPU_RST_ADDR    = # --cpu-reset-address CPU_RESET_ADDRESS
# Output Directories
# OUTPUT_DIR     ?= vexriscv_lite_sim
# GATEWARE_DIR   ?= $(OUTPUT_DIR)/gateware

# custom?

# --cpu-variant=$(CPU_VARIANT)   \
  --output-dir=$(OUTPUT_DIR)     \
  --gateware-dir=$(GATEWARE_DIR) \
  --software-dir=$(SOFTWARE_DIR) \
  --doc

# ----------------------------------------------------------------------
#
# SoC GEN to-do
#
# ----------------------------------------------------------------------
soc_gen:
	litex_soc_gen                   \
	--cpu-type=$(CPU_TYPE)          \
	--cpu-variant=$(CPU_VARIANT)    \
	--output-dir=$(OUTPUT_DIR)      \
	--gateware-dir=$(GATEWARE_DIR)  \
	--software-dir=$(SOFTWARE_DIR)  \
	--doc