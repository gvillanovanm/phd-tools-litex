# README

## 1. Installation

### Environment used

* Ubuntu 22.04.3
* LiteX master commit 1204cfda9d18df45f6cb3aa2434cf91afe1c3b34

### LiteX installation

https://www.swhwc.info/linux-on-litex.html

```bash
sudo apt update
sudo apt upgrade
sudo apt install openocd fakeroot verilator python3 meson gtkterm gawk texinfo git python3-pip bison device-tree-compiler autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev build-essential flex gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build wget

# Create litex workspace 
mkdir -p workspace/litex/

# Install litex
cd workspace/litex/
wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py
chmod 777 litex_setup.py
python3 ./litex_setup.py --config=full --init --install --user

# Export litex var
export PATH=$PATH:~/.local/bin

# Install RISC-V
pip3 install meson ninja
sudo ./litex_setup.py --gcc=riscv

# Test on bord arty
cd ..

export LITEX_ENV_VIVADO=/Xilinx/Vivado/2024.2

# https://docs.nordicsemi.com/bundle/ncs-2.2.0/page/zephyr/boards/riscv/litex_vexriscv/doc/index.html
./litex-boards/litex_boards/targets/digilent_arty.py --build --timer-uptime --csr-json csr.json
```

### Load

```bash
./litex-boards/litex_boards/targets/digilent_arty.py --timer-uptime --csr-json csr.json --load
```

In terminal, test the integrated BIOS in ROM. 
 
```bash
picocom -b 115200 /dev/ttyUSB1
litex> help # to see the commands
```

To programming this board, have a look in this tutorial: https://github.com/tock/tock/blob/master/boards/litex/arty/README.md

### Next Steps

#### QUESTION: How can one customize SoC with it? What is the development flow?
* see: /home/gvillanovanm/Github/phd/tools/phd-tools-litex/workspace/litex/installation/litex/litex-boards/litex_boards/targets/digilent_arty.py

## 2. Export Variables

* var-setup.sh
