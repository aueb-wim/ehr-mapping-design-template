#!/bin/sh

dockerize -template /opt/postgresdb.properties/i2b2-db-harmonized.properties.tmpl:/opt/postgresdb.properties/i2b2-db-harmonized.properties


# Mapping Section
echo "Exporting the flatten csv...."
 
java -jar MIPMapReduced.jar -runsql /opt/map/pivot_i2b2_6_months_MRI_Diag.sql /opt/postgresdb.properties/i2b2-db-harmonized.properties

echo "done!"
