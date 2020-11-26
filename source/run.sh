#!/bin/sh
dockerize -template /opt/postgresdb.properties/mipmap-db.properties.tmpl:/opt/postgresdb.properties/mipmap-db.properties
dockerize -template /opt/postgresdb.properties/i2b2-db.properties.tmpl:/opt/postgresdb.properties/i2b2-db.properties

java -jar /opt/MIPMapReduced.jar -unpivot /opt/source/DB_EHR_subset_cp2.csv /opt/postgresdb.properties/mipmap-db.properties "Attribute" /opt/map/selected_DB_EHR_subset_cp2.txt -u /opt/map/unpivoted_DB_EHR_subset_cp2.txt
java -jar /opt/MIPMapReduced.jar -unpivot /opt/source/volumes_new.csv /opt/postgresdb.properties/mipmap-db.properties "Attribute" /opt/map/selected_volumes_new.txt -u /opt/map/unpivoted_volumes_new.txt
# Encounter and Patient Mapping Section
echo "Generating patient_num and encounter_num"

java -jar /opt/MIPMapReduced.jar -generate_id /opt/map/patientmapping.properties

java -jar /opt/MIPMapReduced.jar -generate_id /opt/map/encountermapping.properties
