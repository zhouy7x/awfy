#!/bin/bash

function optional() {
    if [ -z "${!1}" ]; then
        echo -n "${1} not set (ok)"
        if [ -n "${2}" ]; then
            echo -n ", default is: ${2}"
            export ${1}="${2}"
        fi
        echo ""
    fi
}

machine=$1
cpu=$2
version=$3
optional version "release"
out_dir="out.gn/$machine/$cpu.$version"
echo "output directory is: $out_dir"
arguments="is_debug=false target_cpu=\"$cpu\""
if [ "$version" == "patch" ]; then
    arguments+=" v8_enable_pointer_compression=true"
fi
echo -e "gn gen $out_dir --args=\"$arguments\""
gn gen $out_dir --args="$arguments"
ninja -C $out_dir d8 -j40

