#!/bin/bash


if [ ! -e tmp/v8-count ];
then
    touch tmp/v8-count
fi
tmp=`cat tmp/v8-count`;
if [ -z "$tmp" ];
then
    tmp=0;
fi

echo $tmp;
if [ $tmp == 5 ];
then
    echo "succeed!"
    tmp=0
else
    tmp=$[tmp+1];
fi
echo $tmp > tmp/v8-count;

