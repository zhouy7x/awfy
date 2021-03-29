#!/bin/bash

docker start awfy awfy-mysql opengrok
pushd /mnt/work/docker/awfy/docker
/usr/bin/expect ./start-awfy >> start-awfy.log
popd

exit 0
