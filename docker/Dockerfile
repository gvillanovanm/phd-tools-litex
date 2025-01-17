# Use an Ubuntu base image
FROM --platform=linux/amd64 ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    openocd fakeroot verilator python3 meson gtkterm gawk texinfo git python3-pip \
    bison device-tree-compiler autoconf automake autotools-dev curl python3 libmpc-dev \
    libmpfr-dev libgmp-dev build-essential flex gperf libtool patchutils bc zlib1g-dev \
    libexpat-dev ninja-build wget libevent-dev libjson-c-dev

# Download and install LiteX
RUN mkdir /litex && \
    cd /litex && \
    wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py && \
    chmod 777 litex_setup.py && \
    python3 ./litex_setup.py --config=full --init --install --user

# Add LiteX to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Install additional tools for RISC-V
RUN cd /litex && \
    pip3 install meson ninja && \
    echo "y" | python3 ./litex_setup.py --gcc=riscv && \
    rm -rf /var/lib/apt/lists/*

# Export Vivado environment variable (adjust path as necessary)
ENV LITEX_ENV_VIVADO=/opt/Xilinx/Vivado/2024.2

# Default command: start a shell
CMD ["/bin/bash"]