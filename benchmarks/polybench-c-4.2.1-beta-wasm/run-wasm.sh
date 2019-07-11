#!/bin/sh
cd `dirname $0`; 
rootdir=`pwd`;

categories=('linear-algebra/blas' 'linear-algebra/kernels' 'linear-algebra/solvers' 'datamining' 'stencils' 'medley');
for cat in ${categories[@]}; do 
    for dir in `ls $cat`; do
        cd $cat/$dir
        kernel=$dir;
        echo $kernel
        sleep 1
        #sh $rootdir/utilities/time_benchmark_wasm.sh '/home/jingbao/Work/v8/out/x64.release/d8 --no-wasm-tier-up --no-liftoff ./'$kernel'.js';
       sh $rootdir/utilities/time_benchmark_wasm.sh $1 './'$kernel'.js';
        cd $rootdir
    done
done
