sqlite3 db.sqlite3 < ./sqllite_dump.sql
mv backup.sql bkp/db.sqlite3@`date +%d-%m-%y-%H:%M`
