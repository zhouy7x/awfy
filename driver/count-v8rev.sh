count=0

list=`git rev-list origin/master ^master | tac`
if [ -z "$list" ]; then
  echo "chromium: no update"
else
  for i in $list
  do
    # Only check v8 changed chromium
    v8find=`git show $i | grep -P "^\+\s+.v8_revision."`
    if [[ -n $v8find ]]; then
      #echo $i
	  count=`expr $count + 1`
    fi
  done
fi
echo $count

