#list=`ssh ssgs3@10.239.61.100 powershell "cd d:/src/chromium/src/ ; git rev-list origin/master...master" | tac`
##echo $list
#
#if [ -z "$list" ]; then
#    echo "chromium: no update"
#else
#    for i in $list
#    do
#      echo $i
#    done
#fi
#
#i=244613d0e9774fd8768a2249110c90b4605b6733
#
#v8find=`ssh ssgs3@10.239.61.100 powershell "cd d:/src/chromium/src/ ; git show $i "| grep -P "^\+\s+.v8_revision."`
#echo 123213
#echo $v8find
#a=$1
#b=1
#echo $a
#c=`expr $a*$b`
#c=$[$a*$b]
#echo $c
#echo $2
#if [ -z $1 ] ; then
#  echo 1
#else
#  echo 2
#fi
[ -z $1 ] && d=1 || d=$1
echo $d
echo $[$d/1]
