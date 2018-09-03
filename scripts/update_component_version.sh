#!/bin/bash

newversion=$1
file=$(find django_root -name 'common.py')
echo "File is ${file}"
version=$(grep 'COMPONENTS_VERSION' ${file} )

echo "Current version is ${version}"

exp="s/\(COMPONENTS_VERSION[[:space:]]*=[[:space:]]*\)'\(.*\)'/\1'${newversion}' #Old: \2/"
sed "${exp}" ${file}  | grep COMPONENTS_VERSION