#!/bin/zsh
cd /home/ubuntu/GreenLife/greenlifecms
DB_FILE=db.sqlite3
BKP_FILE=bkp/db.sqlite3@`date +%d-%m-%y-%H:%M`.tgz
echo "tar zcvf $BKP_FILE $DB_FILE"
tar zcvf $BKP_FILE $DB_FILE
