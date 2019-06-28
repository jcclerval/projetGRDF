#!/bin/bash

crontab -r
##line='*/30 9-17 * * mon,tue,wed,thu,fri /home/debian/ProjetGRDF/sargas/scan_execution.sh >> /home/debian/ProjetGRDF/sargas/sauvegarde.log'
line_1='0 9-17/2 * * mon,tue,wed,thu,fri /home/debian/ProjetGRDF/sargas/scan_execution.sh >> /home/debian/ProjetGRDF/sargas/sauvegarde.log='
line_2='0 9-17/2 * * mon,tue,wed,thu,fri time timeout 3600 ssh grdf >> /home/debian'


(crontab -u debian -l; printf "$line_1 \n$line_2\n" ) | crontab -u debian -
