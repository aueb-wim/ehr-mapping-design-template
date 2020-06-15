#!/bin/bash

getValueFromConfig() {

    VALUE=`grep ${1} config.sys | cut -d '=' -f 2`
    echo $VALUE

}

db_capture=$(getValueFromConfig "db_capture")
db_harmonized=$(getValueFromConfig "db_harmonized")
db_user=$(getValueFromConfig "db_user")
db_pwd=$(getValueFromConfig "db_pwd")
container_name=$(getValueFromConfig "container_name")
container_port=$(getValueFromConfig "container_port")

capture_path=capture_step/map.xml.tmpl
harmonize_path=harmonize_step/mapHarmonize.xml.tmpl

if [ -z $1 ]; then
    echo "Please give capture or harmonize keywords."
    exit 1
elif [ $1 = "capture" ]; then
    target_path=capture_step/map.xml.tmpl
    cp map.xml $target_path
elif [ $1 = "harmonize" ]; then
    target_path=harmonize_step/mapHarmonize.xml.tmpl
    cp mapHarmonize.xml $target_path
else
   echo "Not a valid keyword. Please give capture or harmonize keywords"
   exit 1
fi


sed -i "s|<uri>jdbc:postgresql://localhost:${container_port}/${db_capture}</uri>|<uri>jdbc:postgresql://{{ .Env.i2b2_db_host }}:{{ default .Env.i2b2_db_port \"5432\" }}/{{ .Env.i2b2_db_name }}</uri>|g" $target_path
sed -i "s|<uri>jdbc:postgresql://localhost:${container_port}/${db_harmonized}</uri>|<uri>jdbc:postgresql://{{ .Env.i2b2_db_host }}:{{ default .Env.i2b2_db_port \"5432\" }}/{{ .Env.i2b2_db_harmonized_name }}</uri>|g" $target_path
sed -i "s|<login>${db_user}</login>|<login>{{ default .Env.i2b2_db_user \"postgres\" }}</login>|g" $target_path
sed -i "s|<password>${db_pwd}</password>|<password>{{ default .Env.i2b2_db_password \"postgres\" }}</password>|g" $target_path

sed -i "s|${db_capture}.|{{ .Env.i2b2_db_name }}.|g" $target_path
sed -i "s|${db_harmonized}.|{{ .Env.i2b2_db_harmonized_name }}.|g" $target_path