#!/bin/bash

# On lance le truc

PROCESS_NUM=$(ps -ef | grep "ssh" | grep -v "grep" | wc -l)
if [ "$PROCESS_NUM" == "0" ];
then
ssh grdf -N -fn
fi
