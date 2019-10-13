#!/bin/bash

echo '*****************************************'
echo '*                                       *'
echo '*      Installation de la Raspberry     *'
echo '*                                       *'
echo '*****************************************'

#-----------------------------------------------
echo '	- Installation du script de démarrage'

#-----------------------------------------------
echo '	- Installation des modules necessaires'
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y mosquitto python-pip python-mysqldb libusb-dev wvdial

pip install paho-mqtt --index-url=https://pypi.python.org/simple/
echo 'Modules installés'

#-----------------------------------------------
#### A changer, remplacer par sargas
echo '	- Compilation du programme'
cd sargas
make clean
make
cd ../
echo 'Programme compilé'

#-----------------------------------------------
echo 'Copie des fichiers de configuration'

#-----------------------------------------------
# Installation du fichier ssh
sudo cp sargas/config_files/ssh_config /etc/ssh/ssh_config

#-----------------------------------------------
# Installation du Ip-Up
sudo cp sargas/config_files/ip-up /etc/ppp/ip-up

#-----------------------------------------------
# Installation du fichier de conf wvdial.com
sudo cp sargas/config_files/wvdial.conf.references /etc/wvdial.conf

#-----------------------------------------------
# Installation du crontab
./sargas/update_cron.sh

#-----------------------------------------------
# Installation du fichier de plaque
echo 'Creation du fichier de plaque'
echo 'Entrez la plaque du camion'
read plaque
echo 'Plaque ' $plaque
touch $HOME/get_camion.sh
echo 'echo ' $plaque >> $HOME/get_camion.sh
sudo chmod +x $HOME/get_camion.sh

echo '********** Installation terminée **********'

exit 0
