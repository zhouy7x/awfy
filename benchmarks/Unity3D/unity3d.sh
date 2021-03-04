#!/bin/bash
echo "***************************"  
echo "Auto collect unity3d datas!"  
echo "eg: ./unity3d.sh CHROME_PATH URL"  
echo "***************************"  


if [ $# != 2 ]
then
	echo "usage: $0  CHROME_PATH  URL  JSFLAG"
	exit 
fi 

# Get chrome_path and url 
CHROME_PATH=$1
URL=$2
JSFLAG=$3
# delete log file and score file

CHROME_DEBUG_LOG="$HOME/.config/chromium/chrome_debug.log"
SCORE_INFO_FILE="$HOME/unity3d.txt"
if [ -f $CHROME_DEBUG_LOG ]
then
	rm -rf $CHROME_DEBUG_LOG
fi

if [ -f $SCORE_INFO_FILE ]
then
	rm -rf $SCORE_INFO_FILE
fi

# lanuch chrome
if [ "$(cat /proc/cpuinfo  | grep N3350)" != "" ] ;then
	export DISPLAY=":1"
#elif [ "$(cat /proc/cpuinfo  | grep 1800X)" != "" ] ;then
#	export DISPLAY=":1"
elif [ "$(cat /proc/cpuinfo  | grep N3450)" != "" ] ;then
	export DISPLAY=":0"
else
	export DISPLAY=":0"

fi
if [ -z $JSFLAG ] ; then
  $CHROME_PATH --no-sandbox $URL --enable-logging --v=1 &
else
  $CHROME_PATH --no-sandbox $URL --enable-logging --js-flags=$JSFLAG --v=1 &
fi


# start to monitor chrome exit 
keyword="Overall:"
while true
do
	grep -wnrq $keyword $CHROME_DEBUG_LOG
	if [ $? -eq 0 ]
	then
		echo "find keyword $keyword ..."
		#grep -o $keyword | wc -l
		cat $CHROME_DEBUG_LOG | grep -B 12 $keyword | cut -d '"' -f 2 > $SCORE_INFO_FILE
		cat $SCORE_INFO_FILE

		# kill chrome process
		#ps -ef | grep chrome | grep -v grep | awk '{print $2}' | xargs kill -9
		ps -ef | grep $CHROME_PATH | grep -v grep | awk '{print $2}' | xargs kill -9
		break
	else
		echo "No data found. wait chrome exit!!!"
	fi 

	sleep 3
done 


