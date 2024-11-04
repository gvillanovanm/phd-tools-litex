# Arty DDR3 project

The `arty.yml` file serves as the configuration file, similar to MIG. For this configuration, I was inspired by the following resource:  
[Art y A7 DRAM Configuration](https://github.com/epsilon537/boxlambda/blob/master/gw/components/litedram/artya7dram.yml)

## Facts about the Generator

* for_sim: The interface related to DDR is removed.
* for_fpga: The interface related to DDR is included, and the design incorporates many "built-in" FPGA blocks (e.g., BUFG).

## Before synthesis: simulation

### Verilator (wip)
* I've tried to use Verilator, but Im getting some error.

### ModelSim (todo)

