from SPEC_CMDS import abreviate_spec_name, launch_cmd_rate, spec_path
import platform
import os

config_name = "gem5"

def getExecPath(app: str):
    mach=platform.machine()
    if(mach == "aarch64"):
        #ARM
        execpath="%s/benchspec/CPU/%s/run/run_base_refrate_%s-64.0000/" % (spec_path, abreviate_spec_name[app], config_name)
    elif(mach == "x86_64"):
        #X86
        execpath="%s/benchspec/CPU/%s/run/run_base_refrate_%s-m64.0000/" % (spec_path, abreviate_spec_name[app], config_name)
    else:
        print("ERROR: Not supported architecture")
        exit -1
    return execpath

def getNameApp(app_name: str):
    if ("gcc" in app_name):
        return "cpu"+app_name
    elif ("xalan" in app_name):
        return "cpuxalan"
    elif ("cactuBSSN" in app_name):
        return "cactusBSSN"
    else:
        return app_name

def getExecCmd(app: str):
    mach=platform.machine()
    if(mach == "aarch64"):
        #ARM
        exec_cmd="./%s_r_base.%s-64" % (getNameApp(app), config_name)
    elif(mach == "x86_64"):
        #X86
        exec_cmd="./%s_r_base.%s-m64" % (getNameApp(app), config_name)
    return exec_cmd

def getExecArgs(app: str, cmd: str):
    return launch_cmd_rate[abreviate_spec_name[app]][int(cmd)].split()

def getExec(app: str):
    return os.path.join(getExecPath(app),getExecCmd(app))
