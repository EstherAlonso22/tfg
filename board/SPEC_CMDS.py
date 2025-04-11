import platform

spec_path = "/afs/atc.unican.es/u/p/prietop/SPEC17"
config_name = "gem5"

perlbench_path = "%s/benchspec/CPU/500.perlbench_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
perlbench = {
    1 : "-I%s/lib %s/checkspam.pl 2500 5 25 11 150 1 1 1 1" % (perlbench_path, perlbench_path),
    2 : "-I%s/lib %s/diffmail.pl 4 800 10 17 19 300" % (perlbench_path, perlbench_path),
    3 : "-I%s/lib %s/splitmail.pl 6400 12 26 16 100 0" % (perlbench_path, perlbench_path)
}
gcc_path = "%s/benchspec/CPU/502.gcc_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
gcc = {
    1 : "%s/gcc-pp.c -O3 -finline-limit=0 -fif-conversion -fif-conversion2 -o %s/gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.s"
    % (gcc_path, gcc_path),
    2 : "%s/gcc-pp.c -O2 -finline-limit=36000 -fpic -o %s/gcc-pp.opts-O2_-finline-limit_36000_-fpic.s" % (gcc_path, gcc_path),
    3 : "%s/gcc-smaller.c -O3 -fipa-pta -o %s/gcc-smaller.opts-O3_-fipa-pta.s" % (gcc_path, gcc_path),
    4 : "%s/ref32.c -O5 -o %s/ref32.opts-O5.s" % (gcc_path, gcc_path),
    5 : "%s/ref32.c -O3 -fselective-scheduling -fselective-scheduling2 -o %s/ref32.opts-O3_-fselective-scheduling_-fselective-scheduling2.s"
    % (gcc_path, gcc_path)
}
bwaves_path = "%s/benchspec/CPU/503.bwaves_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
bwaves = {
    1 : "%s/bwaves_1" % bwaves_path,
    2 : "%s/bwaves_2" % bwaves_path,
    3 : "%s/bwaves_3" % bwaves_path,
    4 : "%s bwaves_4" % bwaves_path
}
mcf_path = "%s/benchspec/CPU/505.mcf_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
mcf = {
    1 : "%s/inp.in" % mcf_path  
}
cactuBSSN_path = "%s/benchspec/CPU/507.cactuBSSN_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
cactuBSSN = {
    1 : "%s/spec_ref.par" % cactuBSSN_path
}
namd_path = "%s/benchspec/CPU/508.namd_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
namd = {
    1 : "--input %s/apoa1.input --output %s/apoa1.ref.output --iterations 65" % (namd_path, namd_path)
}
parest_path = "%s/benchspec/CPU/510.parest_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
parest = {
    1 : "%s/ref.prm" % parest_path
}
povray_path = "%s/benchspec/CPU/511.povray_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
povray = {
    1 : "%s/SPEC-benchmark-ref.ini" % povray_path
}
lbm_path = "%s/benchspec/CPU/519.lbm_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
lbm = {
    1 : "3000 %s/reference.dat 0 0 %s/100_100_130_ldc.of" % (lbm_path, lbm_path)
}
omnetpp = {
    1 : "-c General -r 0"
}
wrf = {
    1 : ""
}
xalanbmk_path = "%s/benchspec/CPU/523.xalanbmk_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
xalanbmk = {
    1 : "-v %s/t5.xml %s/xalanc.xsl" % (xalanbmk_path, xalanbmk_path)
}
x264_path = "%s/benchspec/CPU/525.x264_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
x264 = {
    1 : "--pass 1 --stats %s/x264_stats.log --bitrate 1000 --frames 1000 -o %s/BuckBunny_New.264 %s/BuckBunny.yuv 1280x720"
    % (x264_path, x264_path, x264_path),
    2 : "--pass 2 --stats %s/x264_stats.log --bitrate 1000 --dumpyuv 200 --frames 1000 -o %s/BuckBunny_New.264 %s/BuckBunny.yuv 1280x720"
    % (x264_path, x264_path, x264_path),
    3 : "--seek 500 --dumpyuv 200 --frames 1250 -o %s/BuckBunny_New.264 %s/BuckBunny.yuv 1280x720" % (x264_path, x264_path)
}
blender = {
    1 : "sh3_no_char.blend --render-output sh3_no_char_ --threads 1 -b -F RAWTGA -s 849 -e 849 -a"
}
cam4 = {
    1 : ""
}
deepsjeng_path = "%s/benchspec/CPU/531.deepsjeng_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
deepsjeng = {
    1 : "%s/ref.txt" % deepsjeng_path
}
imagick_path = "%s/benchspec/CPU/538.imagick_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
imagick = {
    #1 : "-limit disk 0 refrate_input.tga -edge 41 -resample 181% -emboss 31 -colorspace YUV -mean-shift 19x19+15% -resize 30% refrate_output.tga"
    1 : "-limit disk 0 %s/refrate_input.tga -mean-shift 19x19+15%% -edge 41 -resample 181%% -emboss 31 -colorspace YUV -resize 30%% %s/refrate_output.tga"
    % (imagick_path, imagick_path)
}
leela_path = "%s/benchspec/CPU/541.leela_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
leela = {
    1 : "%s/ref.sgf" % leela_path
}
nab_path = "%s/benchspec/CPU/544.nab_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
nab = {
    1 : "%s/1am0 1122214447 122" % nab_path
}
exchange2 = {
    1 : "6"
}
fotonik3d = {
    1 : ""
}
roms_path = "%s/benchspec/CPU/554.roms_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
roms = {
    1 : "< %s/ocean_benchmark2.in.x" % roms_path
}
xz_path = "%s/benchspec/CPU/557.xz_r/run/run_base_refrate_%s-m64.0000/" % (spec_path, config_name)
xz = {
    1 : "%s/cld.tar.xz 160 19cf30ae51eddcbefda78dd06014b4b96281456e078ca7c13e1c0c9e6aaea8dff3efb4ad6b0456697718cede6bd5454852652806a657bb56e07d61128434b474 59796407 61004416 6" % xz_path,
    2 : "%s/cpu2006docs.tar.xz 250 055ce243071129412e9dd0b3b69a21654033a9b723d874b2015c774fac1553d9713be561ca86f74e4f16f22e664fc17a79f30caa5ad2c04fbc447549c2810fae 23047774 23513385 6e" % xz_path,
    3 : "%s/input.combined.xz 250 a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf 40401484 41217675 7" % xz_path
}
specrand_f = {
    1 : "1255432124 234923"
}
specrand_i = {
    1 : "1255432124 234923"
}
launch_cmd_rate = {
    #"500.perlbench_r" : perlbench,
    "502.gcc_r" : gcc,
    "503.bwaves_r" : bwaves,
    "505.mcf_r" : mcf,
    "507.cactuBSSN_r" : cactuBSSN,
    "508.namd_r" : namd,
    #"510.parest_r" : parest,
    # povray does not call work_begin
    #"511.povray_r" : povray,
    "519.lbm_r" : lbm,
    "520.omnetpp_r" : omnetpp,
    #"521.wrf_r" : wrf,
    "523.xalancbmk_r" : xalanbmk,
    "525.x264_r" : x264, 
    "526.blender_r" : blender,
    "527.cam4_r" : cam4,
    "531.deepsjeng_r" : deepsjeng,
    "538.imagick_r" : imagick,
    "541.leela_r" : leela,
    "544.nab_r" : nab,
    "548.exchange2_r" : exchange2,
    "549.fotonik3d_r" : fotonik3d,
    "554.roms_r" : roms,
    "557.xz_r" : xz,
    #"997.specrand_fr" : specrand_f,
    #"999.specrand_ir" : specrand_i
}

abreviate_spec_name = {
    "perlbench" : "500.perlbench_r",
    "gcc" : "502.gcc_r",
    "bwaves" : "503.bwaves_r",
    "mcf" : "505.mcf_r",
    "cactuBSSN" : "507.cactuBSSN_r",
    "namd" : "508.namd_r",
    "parest" : "510.parest_r",
    "povray" : "511.povray_r",
    "lbm" : "519.lbm_r",
    "omnetpp" : "520.omnetpp_r",
    "wrf" : "521.wrf_r",
    "xalan" : "523.xalancbmk_r",
    "x264" : "525.x264_r", 
    "blender" : "526.blender_r",
    "cam4" : "527.cam4_r",
    "deepsjeng" : "531.deepsjeng_r",
    "imagick" : "538.imagick_r",
    "leela" : "541.leela_r",
    "nab" : "544.nab_r",
    "exchange2" : "548.exchange2_r",
    "fotonik3d" : "549.fotonik3d_r",
    "roms" : "554.roms_r",
    "xz" : "557.xz_r",
    "specrand_f" : "997.specrand_fr",
    "specrand_i" : "999.specrand_ir"
}

launch_cmd = {
    "rate" : launch_cmd_rate,
}
