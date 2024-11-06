# Environment used

* Ubuntu 22.04.3
* LiteX master commit 1204cfda9d18df45f6cb3aa2434cf91afe1c3b34

# LiteX installation

https://www.swhwc.info/linux-on-litex.html

```bash
apt update
apt upgrade
apt install openocd fakeroot verilator python3 meson gtkterm gawk texinfo git python3-pip bison device-tree-compiler autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev build-essential flex gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build wget

mkdir -p workspace/litex/installation/litex
cd workspace/litex/installation/litex
wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py
chmod 777 litex_setup.py
python3 ./litex_setup.py --config=full --init --install --user
export PATH=$PATH:~/.local/bin

# Install RISC-V
pip3 install meson ninja
./litex_setup.py --gcc=riscv

# Test
cd ..

export LITEX_ENV_VIVADO=/Xilinx/Vivado/2024.1

# https://docs.nordicsemi.com/bundle/ncs-2.2.0/page/zephyr/boards/riscv/litex_vexriscv/doc/index.html
./litex-boards/litex_boards/targets/digilent_arty.py --build --timer-uptime --csr-json csr.json

# It's need to update
pip3 install -U meson
```
