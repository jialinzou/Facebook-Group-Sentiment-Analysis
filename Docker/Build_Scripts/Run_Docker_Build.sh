# su as postgres and startup the postgres server
su - postgres -c '/usr/lib/postgresql/9.4/bin/postgres -D /var/lib/postgresql/9.4/main -c config_file=/etc/postgresql/9.4/main/postgresql.conf &' && 

# Startup the MongoDB Server in the background
(mongod --config /etc/mongod.conf &) && 

# Startup the Rabbitmq Server in the background
(rabbitmq-server &) && 

# cd to celery startup script, and force root to be run on celery, and start the
# celery worker
cd /application/Django_Application/workload_distribution/celery_startup_scripts && 
export C_FORCE_ROOT=true && 
(./celery_worker_start.sh &) && 

# Sleep for 1 minute until all services are ready
sleep 60 && 

# cd into the django application and start a sending constant messages to keep travis alive
cd /application/Django_Application && (../Build_Scripts/Constant_Message.sh &) && 

# Run Migration on Models on Django
python manage.py migrate && 

# Run tests, and send results to coveralls.io
# COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN TRAVIS_BRANCH=$TRAVIS_BRANCH BRANCH=$TRAVIS_BRANCH coveralls
coverage run --rcfile=../.coveragerc -m unit_tests.run_all_tests && 
COVERALLS_REPO_TOKEN=$1 TRAVIS_BRANCH=$2 BRANCH=$3 coveralls
