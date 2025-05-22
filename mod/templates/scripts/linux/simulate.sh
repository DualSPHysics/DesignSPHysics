{common}
dualsph=$bindir"/DualSPHysics5.4_linux64"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$bindir
args="{args}"
$dualsph $args
