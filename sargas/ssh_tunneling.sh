#!/bin/bash

# On lance le truc

PROCESS_NUM=$(ps -ef | grep "autossh" | grep -v "grep" | wc -l)
if [ "$PROCESS_NUM" == "0" ];
then
autossh grdf -N -fn &
fi
