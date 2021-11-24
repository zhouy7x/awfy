Components
==========

1. Database: MySQL database that stores statistics.
2. Collector: Hidden PHP script on the webserver, where stats get sent.
3. Driver: Python driver that runs on each benchmark computer, and submits stats.
4. Processor: Python aggregator that builds JSON data from the DB.
5. Website: Static HTML as the frontpage, that queries JSON via XHR.

Components (2), (3), and (5) must be on the same webserver, otherwise timestamps might not be computed correctly.

Keep in mind, most of this documentation is for posterity. AWFY was never intended to be a drag-and-drop all-in-one released product, 
so the procedures and scripts may be pretty rough.

Source repo: `git clone https://gitlab.devtools.intel.com/zhouy7x/awfy.git`

Official source repo: `git clone http://github.com/dvander/arewefastyet awfy`

Installation
============

Build awfy docker image
----------------------
* in localhost
```text
    /etc/init.d/apache2 stop
    mkdir -p /mnt/work/docker/
    cd /mnt/work/docker/   
    git clone https://gitlab.devtools.intel.com/zhouy7x/awfy.git
    cd awfy/docker 
    docker build -t awfy:18.04 .
```
Build mysql docker image
-----------------------
* in localhost
```text
    /etc/init.d/mysql stop
    cd /mnt/work/docker/awfy/database
    docker build -t awfy/mysql:5.7 .
```

Run docker container
-------------------
* in localhost
```text
    cd /mnt/work/docker/
    mkdir -p VOLUMES/repos
    mkdir -p VOLUMES/logs
    mkdir -p VOLUMES/data
    docker run -it -d \
            --network host \
            --name awfy \
            -v /mnt/work/docker/awfy:/awfy \
            -v /mnt/work/docker/VOLUMES/repos:/repos \
            -v /mnt/work/docker/VOLUMES/logs:/logs \
            awfy:18.04 \
            /bin/bash
    docker run -it -d \
            --name awfy-mysql \
            -v /mnt/work/docker/VOLUMES/data:/var/lib/mysql \
            -e MYSQL_ROOT_HOST="%" \
            -e MYSQL_ROOT_PASSWORD="mkk" \
            -p 3306:3306/tcp \
            awfy/mysql:5.7
```

Auto start docker container and run default devices after system start (IF NEEDED!)
-----------------------------------------------------------------------------------
```text
sudo chmod 755 start-docker.sh
sudo mv start-docker.sh /etc/init.d/
cd /etc/init.d/
sudo update-rc.d start-docker.sh defaults 90  # To remove, run `sudo update-rc.d -f start-docker.sh remove`
```

Init DB
-------
* enter to awfy docker
```text
    docker exec -it awfy /bin/bash
    cd /home/user/work/awfy/
    ssh-keygen
    cat ~/.ssh/id_rsa.pub >> docker/jsc/.ssh/authorized_keys
    mysql -uroot -pmkk -h `hostname -s` -P 3306
```
* in awfy-mysql
```sql
    CREATE DATABASE dvander CHARSET="UTF8";
    exit
```
* exit to awfy docker
```text
    cd /home/user/work/awfy/database
    mysql -uroot -pmkk -h `hostname -s` -P 3306 dvander < dvander-base.sql
    mysql -uroot -pmkk -h `hostname -s` -P 3306
```
* in awfy_mysql
```sql
    use dvander;
    SELECT `value` FROM awfy_config WHERE `key` = 'version';
    exit  
```
Get result '3'.

Build jsc build docker image
-----------------------
```text
    cd /mnt/work/docker/jsc
    docker build . -t awfy/jsc-build:20.04
```

Run jsc docker container
-------------------
* in localhost
```text
    cd /mnt/work/docker/
    docker run -it -d \
            --name awfy-jsc \
            -v /mnt/work/docker/awfy:/awfy \
            -v /mnt/work/docker/VOLUMES/repos:/repos \
            -v /mnt/work/docker/VOLUMES/logs:/logs \
            -p 2222:22/tcp \
            -p 8912:8912/tcp \
            awfy/jsc-build:20.04
            /bin/bash
```
* start jsc sshd server
```text
docker exec -it awfy-jsc /bin/bash
/usr/sbin/sshd
exit
```

Download submodule and repos, install dependence
-----------------------------------------------
* exit to awfy docker
```text
    cd /home/user/work/awfy
    git pull
    git submodule update --init --recursive
    python replace_host.py `hostname -s`  
    ./server/run-clean-and-update.sh  # load http://localhost:8000 in browser, you will see awfy report page.
    cd /home/user/work/repos && mkdir -p v8/base
    cd v8/base && fetch v8 && cd v8 && git checkout master && sed -i -e 's/sudo//' build/install-build-deps.sh && ./build/install-build-deps.sh && build/linux/sysroot_scripts/install-sysroot.py --arch=arm
    cd /home/user/work/repos/v8 && cp -r base 1800x && cp -r base bigcore && cp -r base cyan 
    cd /home/user/work/repos && mkdir -p chrome/x64/chromium
    cd chrome/x64/chromium && fetch chromium && cd src && git checkout master && sed -i -e 's/sudo //' build/install-build-deps.sh && ./build/install-build-deps.sh && build/linux/sysroot_scripts/install-sysroot.py --arch=arm64
    cd /home/user/work/repos/chrome && cp -r x64 arm && cp -r x64 glm && cp -r x64 1800x && cp -r x64 cyan
    cd /home/user/work/repos && mkdir -p jsc/base
    cd jsc/base && git clone https://github.com/WebKit/webkit.git && cd webkit && Tools/gtk/install-dependencies
```

Format of config.json
-----------
```json
{
  "DEVICE_TYPE1": [
    {"name": "DEVICE_NAME1"},  
    {"name": "DEVICE_NAME2"},
    ... 
  ],
  "DEVICE_TYPE2": [
    {"name": "DEVICE_NAME3"},
    {"name": "DEVICE_NAME4"},
    ... 
  ],
  ...
}
```
* startup script starts by the settings of "DEVICE_TYPE" name. (e.g. "x64","win64","jsc"...)
* a "DEVICE_TYPE" has one or more devices(using "DEVICE_NAME" to show differences), (e.g. "jsc-hsw-nuc-jsc-x64", "chrome-amd-3900x", "v8-amd-3900x-x64"...)
* a example about "DEVICE_NAME" config json
```json
{
  "name": "chrome-amd-3900x",                                                   // device name
  "main": {                                                                     // main config, config enter point, 
      // including local repos path, local benchmarks path ,slave name(locate to remote test slave config), 
      // and mode names(different modes in a device means these modes all using the same build binary to run benchmark, but adding different running args)
    "slaves": "3900x",                                                          // slave name, locate to remote test slave's config
    "remote_build": true,                                                       // bool, if true, means a remote build config named "build" must be set
    "repos": "/home/user/work/repos/win64-chrome/x64",                          // local repo path
    "cpu": "x64",                                                               // cpu type, using when building binary
    "updateURL": "http://ssgs5-test.sh.intel.com:8000/UPDATE.php/",             // after slave test all benchmarks, using this url to update test data to AWFY DB 
    "machine": "0",                                                             // useless
    "host": "win-server.sh.intel.com",                                          // remote build host, default is localhost
    "port": "8781",                                                             // remote or local build port, default is 8799
    "benchmarks": "/home/user/work/awfy/benchmarks",                            // local benchmark path
    "target_os": "win64",                                                       // test slave's OS, default is "linux"
    "modes": "headless,headless-future,headless-sp",                            // all mode names
    "source": "chromium-win64"                                                  // to find deeper build and test remote path
  },
  "build": {                                                                    // remote build config
    "rsync": true,                                                              // bool, true means need sync local driver source to remote build driver source, default is true 
    "pull": true,                                                               // bool, true means need pull from remote build server repo path to local build repo path, default is true 
    "repos": "d:\\awfy",                                                        // remote build repo path
    "hostname": "awfy@win-server.sh.intel.com",                                 // remote build hostname, including username
    "driver": "c:\\work\\awfy\\driver",                                         // remote build driver path
    "name": "win-server"                                                        // mark of remote build log
  },
  "3900x": {                                                                    // remote test slave's config
    "remote": "1",                                                              // bool, true means this is a remote test(we do not have local test slave)
    "python": "python",                                                         // python name
    "repos": "c:\\work\\repos\\win64-chrome\\x64",                              // test slave's repo path
    "hostname": "test@3900x-win64.sh.intel.com",                                // test slave's hostname
    "driver": "c:\\work\\awfy\\driver",                                         // test slave's driver path
    "includes": "speedometer2,jetstream2,webxprt3",                             // all test benchmarks
    "machine": "22",                                                            // device id, using when save data to DB by "updateURL"
    "benchmarks": "c:\\work\\awfy\\benchmarks",                                 // test slave's benchmark path
    "cpu": "x64"                                                                // cpu type
  },
  "chromium-win64": {                                                           // deeper build and test remote path
    "source": "chromium\\src"
  },
  "headless": {},                                                               // args of mode1
  "headless-future": {                                                          // args of mode2
    "arg1": "--future"
  },
  "headless-sp": {                                                              // args of mode3
    "arg1": "--sparkplug"
  },
  "headless-a-sp": {                                                            // args of mode4
    "arg1": "--always_sparkplug"
  },
  "native": {                                                                   // maybe useless
    "cc": "gcc",
    "cxx": "g++",
    "options": "-O2",
    "mode": "gcc"
  }
}
```

Init and run
-----------
get the start commit id of each slave.
* in awfy docker
```text
cd /home/user/work/awfy/driver
# Set passwordless login to test slaves, you can get all test slaves' hostname by running ./init.py
./init.py  # you must run listed commands one by one by yourself!!!  TODO: auto run these commands.
# That's all, now you can auto run tests by all_run.py, 
./all_run.py x64 
```