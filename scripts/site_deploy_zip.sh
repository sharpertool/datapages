#!/bin/bash

zipfile=$1
VERSION={$2:-''}
APPPATH=${APPPATH:-/home/ec2-user/datapages.io}
zipdir=${APPPATH}/zipdir

# Put site into maintenance mode
touch ${APPPATH}/maintenance.on

cd ${APPPATH}

echo "unzip ${zipfile} to ${zipdir}"
rm -rf ${zipdir}
mkdir -p ${zipdir}
pushd ${zipdir}
unzip -uoq ~/deploy/${zipfile}

echo "use rsync to synchronize the two paths"
rsync -av --delete zipdir/ django_root
popd

echo "Update requirements"
.venv3/bin/pip install -r requirements/prod.txt

echo -e "\n Collecting updated statics.."
./manage collectstatic --noinput

# Show any pending migrations
./manage showmigrations | grep "\[ \]\|^[a-z]" | grep "[ ]" -B 1

# Run migrations
./manage migrate --noinput

echo "Updating DATAPAGES_VERSION to match production version"
template_version=$(grep DATAPAGES_VERSION django_root/production.env.j2  | sed 's/DATAPAGES_VERSION=//')
version=${VERSION:-template_version}
sed -i -e "s/DATAPAGES_VERSION=.*/DATAPAGES_VERSION=${version}/" .env

echo -e "\n Reloading uWSGI web service.."

# Note: forcing a full reload.
#touch reload.me
sudo /usr/local/bin/supervisorctl restart datapages.io

rm ${APPPATH}/maintenance.on

