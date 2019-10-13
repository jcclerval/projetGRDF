#!/bin/bash

crontab -r
line_1='0 9-17/2 * * mon,tue,wed,thu,fri /home/debian/ProjetGRDF/sargas/scan_execution.sh >> /home/debian/ProjetGRDF/sargas/sauvegarde.log'
line_2='0 9-17/2 * * mon,tue,wed,thu,fri timeout 3600 autossh grdf -N >> /home/debian'
line_3='@reboot timeout 3600 /home/debian/ProjetGRDF/sargas/ssh_tunneling.sh'


(crontab -u debian -l; printf "$line_1 \n$line_2\n$line_3\n" ) | crontab -u debian -



