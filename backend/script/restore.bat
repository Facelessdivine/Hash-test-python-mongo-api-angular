@echo off
mongodump --db apiRestorePython --out data/backup-%date:~-4,4%-%date:~-7,2%-%date:~-10,2%-%time:~3,2%-%time:~6,2%