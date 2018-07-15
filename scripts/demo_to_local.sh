#!/usr/bin/env bash

server=synopticai-prod.cjizxr5h37hl.us-west-2.rds.amazonaws.com
dt=$(date '+%Y-%M-%d-%H_%M')
filename="demo_db_${dt}.sql"
echo "Dumping to filename ${filename}"

ssh bz.datapages.demo "pg_dump -h ${server} -U datasheet_user datapages_demo > ${filename}"
scp bz.datapages.demo:${filename} database/backups
ssh bz.datapages.demo "rm ${filename}"

