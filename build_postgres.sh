#! /bin/bash

getValueFromConfig() {
    VALUE=`grep ${1} config.sys | cut -d '=' -f 2`
    echo $VALUE
}

mipmap='mipmap'
db_capture=`getValueFromConfig "db_capture"`
db_harmonized=`getValueFromConfig "db_harmonized"`
dfcontainer_name='demo_postgres'
dfcontainer_port=`getValueFromConfig "container_port"`
df_db_user=`getValueFromConfig "db_user"`
df_db_pwd=`getValueFromConfig "db_pwd"`

export dfcontainer_name
export dfcontainer_port
export db_capture
export db_harmonized
export df_db_user
export df_db_pwd

docker run -p $dfcontainer_port:5432 --name $dfcontainer_name -e POSTGRES_PASSWORD="$df_db_pwd" -d postgres:9.6
sleep 10

# create mipmap database
echo "Creating $mipmap database"
docker exec -it $dfcontainer_name psql -U $df_db_user -d postgres -c "DROP DATABASE IF EXISTS $mipmap;"
docker exec -it $dfcontainer_name psql -U $df_db_user -d postgres -c "CREATE DATABASE $mipmap;"

# create and set up capture database
echo "Creating $db_capture database"
docker exec -it $dfcontainer_name psql -U $df_db_user -d postgres -c "DROP DATABASE IF EXISTS $db_capture;"
docker exec -it $dfcontainer_name psql -U $df_db_user -d postgres -c "CREATE DATABASE $db_capture;"



# create and set up harmonized database
echo "Creating $db_harmonized database"
docker exec -it $dfcontainer_name psql -U $df_db_user -d postgres -c "DROP DATABASE IF EXISTS $db_harmonized;"
docker exec -it $dfcontainer_name psql -U $df_db_user -d postgres -c "CREATE DATABASE $db_harmonized;"


echo "Setting up $db_capture database"
docker-compose run --rm i2b2_setup

echo "Setting up $db_harmonized database"
docker-compose run --rm i2b2_setup_harmonized

