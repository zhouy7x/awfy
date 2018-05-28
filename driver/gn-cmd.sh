#!/bin/bash
machine=$1
cpu=$2
out_dir="out.gn/$machine/$cpu.release"
echo "output directory is: $out_dir"
arguments="is_debug=false target_cpu=\"$cpu\""
gn gen $out_dir --args="$arguments"
ninja -C $out_dir d8 -j40


