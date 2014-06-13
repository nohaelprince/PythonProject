#! /usr/bin/env bash
export DBNAME=db1
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export APP_HOME=`cd $(dirname $0)/; pwd`

dropdb $DBNAME
createdb $DBNAME

psql -d $DBNAME < $APP_HOME/schema.sql
#psql -d $DBNAME -c "copy mailing from STDIN CSV;" < $APP_HOME/data/emails.csv

