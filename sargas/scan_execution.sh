#!/bin/bash

sleep 3
# Date
dt=$(date '+%d/%m/%Y %H:%M:%S');
# Path
path0=`get_path.sh`
idcamion=`get_camion.sh`

echo ""
echo "--- Date $dt ---"
echo "--- Lancement d'un scan ---"
#
i="0"
max_count="10"
echo "--- Lancement de Wvdial ---"
wvdial &
sleep 10
echo "--- Test de connection ---"
while [ $i -le $max_count ]
	do
	echo "Tentative $i"
	# Test de la connection internet
	wget -q --tries=10 --timeout=20 --spider http://google.com
	if [[ $? -eq 0 ]]; then
			echo "Online"
			echo "proceed with programm"
			python $path0'sargas/script.py -f '$path0' -c '$idcamion
			killall wvdial
			break
	else
			echo "Offline"
			sleep 2
	fi
	i=$[$i+1]
done
#
echo "Fin du code"
sleep 2
