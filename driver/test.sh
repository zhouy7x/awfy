#!/bin/bash


count=0
while :
do
    #part 1
    list=`ls`
    for id in $list
    do
        echo $id
        echo $count
        sleep 1
        count=`expr $count + 1`
        if [ "$count" = "5" ]
        then
            count=0
            break

        fi
    done

    # part 2
    list=`ls ..`
    for id in $list
    do
        echo $id
        echo $count
        sleep 1
        count=`expr $count + 1`
        if [ "$count" = "5" ]
        then
            count=0
            break

        fi
    done
done
