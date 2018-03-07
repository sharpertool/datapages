#!/bin/sh


pushd datapages
coverage run --rcfile='../.coveragerc' manage.py test --keepdb
coverage html
popd

