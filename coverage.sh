#!/bin/sh


pushd datasheet_ai
coverage run --rcfile='../.coveragerc' manage.py test --keepdb
coverage html
popd

