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
    string='-long-time'
    tmp=0
else
    string=''
    tmp=$[tmp+1];
fi
echo $tmp > tmp/v8-count;

#echo --config=client/machine_config/electro-x64$string.config

bash tmp/1$string.sh
