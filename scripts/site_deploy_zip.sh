#!/bin/bash

zipfile=$1
APPPATH=${APPPATH:-/home/ec2-user/datapages.io}

# Put site into maintenance mode
touch ${APPPATH}/maintenance.on

cd ${APPPATH}

echo "unzip ${zipfile}"
unzip -uoq ${zipfile}
rm ${zipfile}

echo "Update requirements"
.venv3/bin/pip install -r requirements/prod.txt

echo -e "\n Collecting updated statics.."
./manage collectstatic --noinput

# Show any pending migrations
./manage showmigrations | grep "\[ \]\|^[a-z]" | grep "[ ]" -B 1

# Run migrations
./manage migrate --noinput

echo "Updating DATAPAGES_VERSION to match production version"
version=$(grep DATAPAGES_VERSION django_root/production.env.j2  | sed 's/DATAPAGES_VERSION=//')
sed -i -e "s/DATAPAGES_VERSION=.*/DATAPAGES_VERSION=${version}/" .env

echo -e "\n Reloading uWSGI web service.."

# Note: forcing a full reload.
#touch reload.me
sudo /usr/local/bin/supervisorctl restart datapages.io

rm ${APPPATH}/maintenance.on

