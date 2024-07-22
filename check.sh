#!/bin/bash
BASEDIR=`dirname $0`
PROJECT_PATH=`cd $BASEDIR; pwd`

cd $PROJECT_PATH
source env/bin/activate
python check.py
deactivate
