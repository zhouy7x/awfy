pushd /home/user/work/awfy/repos/chromium/src
#  git fetch
  current=`git rev-parse HEAD`
  echo $current
  list=`git rev-list 5c04f2b782b5a2a0dc4d61a22bcc67930802771b^..HEAD | tac`
  if [ -z "$list" ]; then
    echo "chromium: no source updated"
  else
    for i in $list
    do
      v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
      if [[ -n $v8find ]]; then
        echo $i
      fi
      #git reset --hard $i
      #pushd /home/user/work/awfy/driver
      #python dostuff.py -f -n --config=awfy-x64.config
      #python dostuff.py -f -n --config=awfy-x86.config

      #count=`expr $count + 1`
      #count=`expr $count % 5`
      #if [ "$count" = "1" ]
      #then
      #  python dostuff.py -f -n --config=awfy-arm.config
      #fi
    done
  fi
popd
