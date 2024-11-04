# INSTALLATION

In the litex repo (on Docker), type:

```bash
$ mkdir install; cd install 
$ ../litex_setup.py --init --install --user
$ ../litex_setup.py update
export PATH=$PATH:~/.local/bin
```

Install a RISC-V toolchain (Only if you want to test/create a SoC with a CPU):

```bash
pip3 install meson ninja
apt update
../litex_setup.py --gcc=riscv
```

Go to litex-boards/litex_boards/targets and execute the target you want to build.
... and/or install Verilator and test LiteX directly on your computer without any FPGA board:

```bash
$ sudo apt install libevent-dev libjson-c-dev verilator
$ litex_sim --cpu-type=vexriscv
```
Here’s a revised version of your text with improved clarity and grammar:

## Temporary Workaround if Already Installed and Using Docker

If LiteX is already installed and you're using Docker, just re-run the script to ensure that all variables are properly set:

```bash
$ mkdir install; cd install 
$ ../litex_setup.py --init --install --user
$ ../litex_setup.py update
export PATH=$PATH:~/.local/bin
```