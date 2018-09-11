#!/bin/bash

sleep 3
echo "Lancement d'un scan"
#
i="0"

wvdial &
while [ $i -lt 10 ]
	do
	# Test de la connection internet
	wget -q --tries=10 --timeout=20 --spider http://google.com
	if [[ $? -eq 0 ]]; then
			echo "Online"
			echo "proceed with programm"
	else
			echo "Offline"
			sleep 2
	fi
	i=$[$i+1]
done
#
echo "Fin du code"
sleep 2
