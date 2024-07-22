#!/bin/bash
BASEDIR=`dirname $0`
PROJECT_PATH=`cd $BASEDIR; pwd`

cd $PROJECT_PATH
source venv/bin/activate
python make_graph.py
deactivate
