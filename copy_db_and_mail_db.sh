#!/bin/zsh
PWD=/home/ubuntu/GreenLife/greenlifecms
cd $PWD
DB_FILE=db.sqlite3
BKP_FILE=bkp/db.sqlite3@`date +%d-%m-%y-%H:%M`.tgz
echo "tar zcvf $BKP_FILE $DB_FILE"
tar zcvf $BKP_FILE $DB_FILE

SUBJECT="GL DB backup $BKP_FILE"

mail -s $SUBJECT yannvr@gmail.com -A $BKP_FILE < ./mail_bkp_body.txt
