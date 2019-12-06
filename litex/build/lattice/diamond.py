# This file is Copyright (c) 2015-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# This file is Copyright (c) 2017-2018 Sergiusz Bazanski <q3k@q3k.org>
# This file is Copyright (c) 2017 William D. Jones <thor0505@comcast.net>
# License: BSD

import os
import sys
import subprocess
import shutil

from migen.fhdl.structure import _Fragment

from litex.build.generic_platform import *
from litex.build import tools
from litex.build.lattice import common

# Helpers ------------------------------------------------------------------------------------------

def _produces_jedec(device):
    return device.startswith("LCMX")

# Constraints (.lpf) -------------------------------------------------------------------------------

def _format_constraint(c):
    if isinstance(c, Pins):
        return ("LOCATE COMP ", " SITE " + "\"" + c.identifiers[0] + "\"")
    elif isinstance(c, IOStandard):
        return ("IOBUF PORT ", " IO_TYPE=" + c.name)
    elif isinstance(c, Misc):
        return ("IOBUF PORT ", " " + c.misc)


def _format_lpf(signame, pin, others, resname):
    fmt_c = [_format_constraint(c) for c in ([Pins(pin)] + others)]
    lpf = []
    for pre, suf in fmt_c:
        lpf.append(pre + "\"" + signame + "\"" + suf + ";")
    return "\n".join(lpf)


def _build_lpf(named_sc, named_pc, build_name):
    lpf = []
    lpf.append("BLOCK RESETPATHS;")
    lpf.append("BLOCK ASYNCPATHS;")
    for sig, pins, others, resname in named_sc:
        if len(pins) > 1:
            for i, p in enumerate(pins):
                lpf.append(_format_lpf(sig + "[" + str(i) + "]", p, others, resname))
        else:
            lpf.append(_format_lpf(sig, pins[0], others, resname))
    if named_pc:
        lpf.append("\n\n".join(named_pc))
    tools.write_to_file(build_name + ".lpf", "\n".join(lpf))

# Project (.tcl) -----------------------------------------------------------------------------------

def _build_tcl(device, sources, vincpaths, build_name):
    tcl = []
    # Create project
    tcl.append(" ".join([
        "prj_project",
        "new -name \"{}\"".format(build_name),
        "-impl \"impl\"",
        "-dev {}".format(device),
        "-synthesis \"synplify\""
    ]))

    # Add include paths
    for path in vincpaths:
        tcl.append("prj_impl option {include path} {\"" + path + "\"}")

    # Add sources
    for filename, language, library in sources:
        tcl.append("prj_src add \"" + filename.replace("\\", "/") + "\" -work " + library)

    # Set top level
    tcl.append("prj_impl option top \"{}\"".format(build_name))

    # Save project
    tcl.append("prj_project save")

    # Build flow
    tcl.append("prj_run Synthesis -impl impl -forceOne")
    tcl.append("prj_run Translate -impl impl")
    tcl.append("prj_run Map -impl impl")
    tcl.append("prj_run PAR -impl impl")
    tcl.append("prj_run Export -impl impl -task Bitgen")
    if _produces_jedec(device):
        tcl.append("prj_run Export -impl impl -task Jedecgen")
    tools.write_to_file(build_name + ".tcl", "\n".join(tcl))

# Script -------------------------------------------------------------------------------------------

def _build_script(build_name, device, toolchain_path, ver=None):
    if sys.platform in ("win32", "cygwin"):
        script_ext = ".bat"
        script_contents = "@echo off\nrem Autogenerated by LiteX / git: " + tools.get_litex_git_revision() + "\n\n"
        copy_stmt = "copy"
        fail_stmt = " || exit /b"
    else:
        script_ext = ".sh"
        script_contents = "# Autogenerated by LiteX / git: " + tools.get_litex_git_revision() + "\nset -e\n"
        copy_stmt = "cp"
        fail_stmt = ""

    if sys.platform not in ("win32", "cygwin"):
        script_contents += "bindir={}\n".format(toolchain_path)
        script_contents += ". ${{bindir}}/diamond_env{fail_stmt}\n".format(fail_stmt=fail_stmt)
    script_contents += "{pnmainc} {tcl_script}{fail_stmt}\n".format(
        pnmainc    = os.path.join(toolchain_path, "pnmainc"),
        tcl_script = build_name + ".tcl",
        fail_stmt  = fail_stmt)
    for ext in (".bit", ".jed"):
        if ext == ".jed" and not _produces_jedec(device):
            continue
        script_contents += "{copy_stmt} {diamond_product} {migen_product} {fail_stmt}\n".format(
            copy_stmt       = copy_stmt,
            fail_stmt       = fail_stmt,
            diamond_product = os.path.join("impl", build_name + "_impl" + ext),
            migen_product   = build_name + ext)

    build_script_file = "build_" + build_name + script_ext
    tools.write_to_file(build_script_file, script_contents, force_unix=False)
    return build_script_file

def _run_script(script):
    if sys.platform in ("win32", "cygwin"):
        shell = ["cmd", "/c"]
    else:
        shell = ["bash"]

    if subprocess.call(shell + [script]) != 0:
        raise OSError("Subprocess failed")

# LatticeDiamondToolchain --------------------------------------------------------------------------

class LatticeDiamondToolchain:
    attr_translate = {
        # FIXME: document
        "keep":             ("syn_keep", "true"),
        "no_retiming":      ("syn_no_retiming", "true"),
        "async_reg":        None,
        "mr_ff":            None,
        "mr_false_path":    None,
        "ars_ff1":          None,
        "ars_ff2":          None,
        "ars_false_path":   None,
        "no_shreg_extract": None
    }

    special_overrides = common.lattice_ecpx_special_overrides

    def build(self, platform, fragment,
        build_dir      = "build",
        build_name     = "top",
        toolchain_path = None,
        run            = True,
        **kwargs):

        # Create build directory
        if toolchain_path is None:
            toolchain_path = "/opt/Diamond"
        os.makedirs(build_dir, exist_ok=True)
        cwd = os.getcwd()
        os.chdir(build_dir)

        # Finalize design
        if not isinstance(fragment, _Fragment):
            fragment = fragment.get_fragment()
        platform.finalize(fragment)

        # Generate verilog
        v_output = platform.get_verilog(fragment, name=build_name, **kwargs)
        named_sc, named_pc = platform.resolve_signals(v_output.ns)
        v_file = build_name + ".v"
        v_output.write(v_file)
        platform.add_source(v_file)

        # Generate design constraints file (.lpf)
        _build_lpf(named_sc, named_pc, build_name)

        # Generate design script file (.tcl)
        _build_tcl(platform.device, platform.sources, platform.verilog_include_paths, build_name)

        # Generate build script
        script = _build_script(build_name, platform.device, toolchain_path)

        # Run
        if run:
            _run_script(script)

        os.chdir(cwd)

        return v_output.ns

    def add_period_constraint(self, platform, clk, period):
        # TODO: handle differential clk
        platform.add_platform_command("""FREQUENCY PORT "{clk}" {freq} MHz;""".format(
            freq=str(float(1/period)*1000), clk="{clk}"), clk=clk)
