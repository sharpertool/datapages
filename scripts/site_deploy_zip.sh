#!/bin/bash

zipfile=$1
VERSION={$2:-''}
APPPATH=${APPPATH:-/var/www/datapages.io}
zipdir=~/zipdir

# Put site into maintenance mode
touch ${APPPATH}/maintenance.on

echo "unzip ${zipfile} to ${zipdir}"
rm -rf ${zipdir}
mkdir -p ${zipdir}
pushd ${zipdir}
unzip -uoq ~/deploy/${zipfile}
popd

cd ${APPPATH}

echo "use rsync to synchronize the two paths"
rsync -av ${zipdir}/ .

echo "Use rsync to remove old files in selected paths"
rsync -av --delete ${zipdir}/django_root/ django_root
rsync -av --delete ${zipdir}/collectedstatic/ collectedstatic
rsync -av --delete ${zipdir}/requirements/ requirements
rsync -av --delete ${zipdir}/scripts/ scripts

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

# Update app directory user and group values
sudo chown -R ec2-user:www ${APPPATH}

echo -e "\n Reloading uWSGI web service.."

# Note: forcing a full reload.
#touch reload.me
sudo /usr/local/bin/supervisorctl restart datapages.io

rm ${APPPATH}/maintenance.on

