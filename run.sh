#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo $DIR

cd $DIR

# ulimit -n 50000
/home/cjailab/anaconda3/envs/ppreader/bin/gunicorn --config=HelloWorld/gunicorn_conf.py HelloWorld.wsgi:application -D