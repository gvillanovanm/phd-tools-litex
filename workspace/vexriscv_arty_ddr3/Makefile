# CPU Configs
CPU_TYPE     =vexriscv # Options: vexriscv, picorv32, etc.

# Sim Configs
SIM_OUT_DIR  =sim

# Baremetal
BAREMETAL_PATH =firmware
export SOC_DIRECTORY=/home/gvillanovanm/phd/tools/phd-tools-litex/litex/soc

# FPGA Build Configs
FPGA_TARGET  =digilent_arty
FPGA_OUT_DIR =fpga

# ----------------------------------------------------------------------
#
# SIMULATION
#
# ----------------------------------------------------------------------

# - The --no-compile-gateware option is used to skip the gateware compilation step, which are not necessary since we are just preparing the SoC here for bare-metal demo compilation.
# - Integrated-main-ram-size is very import to avoid DRAM, the DPU will be like this.
sim_build:
	litex_sim                                 \
	--cpu-type=$(CPU_TYPE)                    \
	--output-dir=$(SIM_OUT_DIR)               \
	--no-compile-gateware

# - Attention: In this example, the linker generated for simulation is not mapping DDR3 mem map
sim_run:
	litex_sim                                 \
	--cpu-type=$(CPU_TYPE)                    \
	--output-dir=$(SIM_OUT_DIR)               \
	--ram-init=$(BAREMETAL_PATH)/demo.bin

sim_fw:
	@echo "Compiling baremetal code..."
	export BUILD_DIR=../$(SIM_OUT_DIR) && \
	make clean -C $(BAREMETAL_PATH) && \
	make -C $(BAREMETAL_PATH)

baremetal_build:
	litex_bare_metal_demo --build-path=$(SIM_OUT_DIR)
	rm demo.*
	mv demo $(BAREMETAL_PATH)

# ----------------------------------------------------------------------
#
# FPGA
# 
# ----------------------------------------------------------------------
fpga_build:
	python3 -m litex_boards.targets.$(FPGA_TARGET) \
	--cpu-type=$(CPU_TYPE)                         \
	--output-dir=$(FPGA_OUT_DIR) --build

fpga_load:
	python3 -m litex_boards.targets.$(FPGA_TARGET) \
	--cpu-type=$(CPU_TYPE)                         \
	--output-dir=$(FPGA_OUT_DIR) --load

fpga_fw:
	@echo "Compiling baremetal code for fpga..."
	export BUILD_DIR=../$(FPGA_OUT_DIR) && \
	make clean -C $(BAREMETAL_PATH) && \
	make -C $(BAREMETAL_PATH)

# Load firmware from serial and execute it
fpga_load_fw:
	litex_term /dev/ttyUSB1 --speed 115200 --kernel $(BAREMETAL_PATH)/demo.bin

fpga_clean:
	rm -rf fpga

clean_all:
	rm -rf firmware fpga prog sim
