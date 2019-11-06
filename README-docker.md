Components
==========

1. Database: MySQL database that stores statistics.
2. Collector: Hidden PHP script on the webserver, where stats get sent.
3. Driver: Python driver that runs on each benchmark computer, and submits stats.
4. Processor: Python aggregator that builds JSON data from the DB.
5. Website: Static HTML as the frontpage, that queries JSON via XHR.

Components (2), (3), and (5) must be on the same webserver, otherwise timestamps might not be computed correctly.

Keep in mind, most of this documentation is for posterity. AWFY was never intended to be a drag-and-drop all-in-one released product, so the procedures and scripts may be pretty rough.

Installation
============

Build awfy docker image
----------------------
```text
    mkdir -p /mnt/work/docker/
    cd /mnt/work/docker/
    git clone https://gitlab.devtools.intel.com/zhouy7x/awfy.git
    cd awfy/docker
    docker build -t test/awfy:18.04 .
```
Build mysql docker image
-----------------------
```text
    /etc/init.d/mysql stop
    cd /mnt/work/docker/awfy/database
    docker build -t test/mysql:5.7 .
```

Run docker container
-------------------
```text
    cd /mnt/work/docker/awfy/docker
    mkdir -p VOLUMES/repos
    mkdir -p VOLUMES/logs
    docker run -it -d \
            --network host \
            --name  awfy \
            -v /mnt/work/docker/awfy/docker/VOLUMES/repos:/repos \
            -v /mnt/work/docker/awfy/docker/VOLUMES/logs:/logs \
            test/awfy:18.04 \
            /bin/bash
    mkdir database/data
    docker run -it -d \
            -v /mnt/work/docker/awfy/database/data:/var/lib/mysql \
            -e MYSQL_ROOT_HOST="%" \
            -e MYSQL_ROOT_PASSWORD="mkk" \
            -p 3306:3306/tcp \
            test/mysql:5.7
```

Init DB
-------
```text
    mysql -uroot -pmkk -h `hostname -s` -P 3306
```
```sql
    CREATE DATABASE dvander CHARSET="UTF8";
    exit
```
```text
    cd /mnt/work/docker/awfy/database
    mysql -uroot -pmkk -h `hostname -s` -P 3306 dvander < dvander-base.sql
    mysql -uroot -pmkk -h `hostname -s` -P 3306
```
```sql
    use dvander;
    SELECT `value` FROM awfy_config WHERE `key` = 'version';  
```
Get result '3'.

Download submodule and repos, install dependence
-----------------------------------------------
```text
    docker exec -it awfy /bin/bash
    cd /home/user/work/awfy
    git submodule update --init --recursive
    cd /home/user/work/repos && mkdir -p v8/base
    cd v8/base && fetch v8 && cd v8 && git checkout master && sed -i -e 's/sudo//' build/install-build-deps.sh && ./build/install-build-deps.sh
    cd /home/user/work/repos/v8 && cp -r base 1800x && cp -r base bigcore && cp -r base cyan
    cd /home/user/work/repos && mkdir -p chrome/x64/chromium
    cd chrome/x64/chromium && fetch chromium && cd src && git checkout master && sed -i -e 's/sudo//' build/install-build-deps.sh && ./build/install-build-deps.sh
    cd /home/user/work/repos/chrome && cp -r x64 arm && cp -r x64 glm && cp -r x64 1800x && cp -r x64 cyan
```

Init and run
-----------
get the start commit id of each slave.
```text
cd /home/user/work/awfy/driver
ssh-keygen
./init.py
./all_run.py cyan x64  
```