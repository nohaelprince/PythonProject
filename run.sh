#! /bin/bash

export APP_HOME=`pwd`



# Database Configuration
export DBNAME=db1
export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PGPORT=${PGPORT:-5432}
export PGHOST=${PGHOST:-localhost}



# Initialize database
bash $APP_HOME/setup_database.sh
#SBT_OPTS="-Xmx4g" sbt "run -c $APP_HOME/application.conf"
python main.py