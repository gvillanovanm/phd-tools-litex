# INSTALLATION

In the litex repo, type:

```
$ mkdir install; cd install 
$ ../litex_setup.py --init --install --user
$ ../litex_setup.py update
```

```
export PATH=$PATH:~/.local/bin # temporary (limited to the current terminal)
```

Install a RISC-V toolchain (Only if you want to test/create a SoC with a CPU):

```
pip3 install meson ninja
apt update
../litex_setup.py --gcc=riscv
```

Go to litex-boards/litex_boards/targets and execute the target you want to build.
... and/or install Verilator and test LiteX directly on your computer without any FPGA board:

```
$ sudo apt install libevent-dev libjson-c-dev verilator
$ litex_sim --cpu-type=vexriscv
```
