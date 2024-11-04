# Arty DDR3 project

The `arty.yml` file serves as the configuration file, similar to MIG. For this configuration, I was inspired by the following resource:  
[Art y A7 DRAM Configuration](https://github.com/epsilon537/boxlambda/blob/master/gw/components/litedram/artya7dram.yml)

## Facts about the generator

* for_sim: the interface related to DDR is removed
* for_fpga: the interface related to DDR is included and the design includes a lot of "built-in" FPGA blocks (eg, BUFG).

## Before synthesis: simulation

* I've tried to use Verilator, but Im getting some error.

* ModelSim:

