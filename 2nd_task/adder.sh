#!/bin/bash
IFS=:
file=$1
while read line
do
 RESULT="useradd"
 INFO=($line)
 NAME=${INFO[0]}
 PASS=${INFO[1]}
 GROUPID=${INFO[2]}
 GRUPS=${INFO[3]}
 HOME_DIR=${INFO[4]}

 if [ -n "$PASS" ]; then
	RESULT="$RESULT -p $(perl -e "print crypt('$PASS','xx')")"
 fi

 if [ -n "$GROUPID" ]; then
	RESULT="$RESULT -g $GROUPID"
 fi
 if [ -n "$GRUPS" ]; then
	IFS=','
	GROUP_LIST=($GRUPS)
	for GRP in "${GROUP_LIST[@]}"; do
		GR_EXIST=$(getent group $GRP | wc -l)
		if [ $GR_EXIST == 0 ]; then
			CREATE="groupadd $GRP"
			eval $CREATE
		fi
	done
	RESULT="$RESULT -G $GRUPS"
	IFS=:
 fi

 if [ -e "$HOME_DIR" ]; then
	echo "wrong home directory, user $NAME will be ignored"
	continue
 fi

 if [ -n "$HOME_DIR" ]; then
	RESULT="$RESULT -d $HOME_DIR"
 fi

 RESULT="$RESULT $NAME"
echo "RESULT = $RESULT"
eval $RESULT

done < $file
