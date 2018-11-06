#!/bin/bash

crontab -r
line='*/30 9-17 * * mon,tue,wed,thu,fri /home/debian/ProjetGRDF/sargas/scan_execution.sh >> /home/debian/ProjetGRDF/sargas/sauvegarde.log'
(crontab -u root -l; echo "$line" ) | crontab -u root -
