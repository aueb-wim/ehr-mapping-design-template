#!/bin/sh

# copy those 3 lines as many times as the csv files that are going to unpivot and rename the variable names accordingly
# and then go to the Unpivotig Section and do the same.
unpivot_csv_1=DB_EHR_subset_cp2.csv
selected_columns_1=selected_DB_EHR_subset_cp2.txt
unpivot_columns_1=unpivoted_DB_EHR_subset_cp2.txt
unpivot_csv_2=volumes_new.csv
selected_columns_2=selected_volumes_new.txt
unpivot_columns_2=unpivoted_volumes_new.txt



dockerize -template /opt/postgresdb.properties/mipmap-db.properties.tmpl:/opt/postgresdb.properties/mipmap-db.properties
dockerize -template /opt/postgresdb.properties/i2b2-db.properties.tmpl:/opt/postgresdb.properties/i2b2-db.properties



# Unpivoting Section
echo "Unpivoting $unpivot_csv_1"

java -jar /opt/MIPMapReduced.jar -unpivot /opt/source/${unpivot_csv_1} /opt/postgresdb.properties/mipmap-db.properties "Attribute" /opt/map/${selected_columns_1} -u /opt/map/${unpivot_columns_1}

echo "Unpivoting $unpivot_csv_2"

java -jar /opt/MIPMapReduced.jar -unpivot /opt/source/${unpivot_csv_2} /opt/postgresdb.properties/mipmap-db.properties "Attribute" /opt/map/${selected_columns_2} -u /opt/map/${unpivot_columns_2}

# Encounter and Patient Mapping Section
#echo "Generating patient_num and encounter_num"

#java -jar /opt/MIPMapReduced.jar -generate_id /opt/map/patientmapping.properties

#java -jar /opt/MIPMapReduced.jar -generate_id /opt/map/encountermapping.properties

