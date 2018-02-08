#!/bin/bash

echo '*****************************************'
echo '*                                       *'
echo '*      Installation de la Raspberry     *'
echo '*                                       *'
echo '*****************************************'

#-----------------------------------------------
echo '	- Copie des fichiers'
mkdir $HOME/raspberry
cp Raspberry/script.py $HOME/raspberry/script.py
sudo cp skyetek/Examples/linux/85-skyemodule.rules /etc/udev/rules.d
echo 'Fichiers copiés'

#-----------------------------------------------
echo '	- Installation du script de démarrage'


# Lanceur de clé 3g
sudo sed -i -e "s/exit 0/wvdial \&\nsleep 10 \nexit 0/g" /etc/rc.local
sudo sed -i -e "s/exit 0/cd \/home\/pi\/raspberry\/\npython \/home\/pi\/raspberry\/script.py \& \nexit 0/g" /etc/rc.local
sudo chmod +x /etc/rc.local
echo 'Script de démarrage configuré'

#-----------------------------------------------
echo '	- Installation des modules necessaires'
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y mosquitto python-pip python-mysqldb libusb-dev wvdial

pip install paho-mqtt --index-url=https://pypi.python.org/simple/
echo 'Modules installés'

#-----------------------------------------------
#### A changer, remplacer par sargas
echo '	- Compilation du programme'
cd skyetek/Examples/linux/
make
cp example $HOME/raspberry/example
echo 'Programme compilé'

echo '********** Installation terminée **********'

exit 0
