#!/bin/bash

mkdir -p output
chmod 777 output

getValueFromConfig() {

    VALUE=`grep ${1} config.sys | cut -d '=' -f 2`
    echo $VALUE

}

# Postgres container info 
dfcontainer_name=$(getValueFromConfig "container_name") 
dfcontainer_name=$(getValueFromConfig "container_name") 
db_harmonized=$(getValueFromConfig "db_harmonized")
db_capture=$(getValueFromConfig "db_capture")
df_db_user=$(getValueFromConfig "db_user")
df_db_pwd=$(getValueFromConfig "db_pwd")

export dfcontainer_name
export db_capture
export db_harminized
export df_db_user
export df_db_pwd

# Mipmap paths 
mipmap_source="./source"
mipmap_pgproperties="./postgresdb.properties"
mipmap_output="./output"
mipmap_preprocess="./preprocess_step"
mipmap_capture="./capture_step"
mipmap_harmonize="./harmonize_step"
mipmap_export="./export_step"


# Settings for exporting
export_csv=harmonized_clinical_data.csv

if [ -z $1 ]; then
    echo "EHR DataFactory step not declared. Exiting..." 
    exit 1
elif [ $1 = "capture" ]; then
    mipmap_map=$mipmap_capture
    use_mipmap=true
elif [ $1 = "harmonize" ]; then
    mipmap_map=$mipmap_harmonize
    use_mipmap=true
elif [ $1 = "preprocess" ]; then
    mipmap_map=$mipmap_preprocess
    use_mipmap=true
elif [ $1 = "export" ]; then
    mipmap_map=$mipmap_export
    use_mipmap=false
    echo "not using mipmap"
else
    echo "Not a EHR DataFactory step. Exiting..."
    exit 1
fi

# setting mipmap paths as enviroment variables to the host
export mipmap_map
export mipmap_source
export mipmap_pgproperties

if [ "$use_mipmap" = true ]; then
    echo "Performing EHR DataFactory $1 step"
    echo "Using $mipmap_map folder"
    docker-compose up mipmap_etl
    echo "Removing mipmap container"
    docker rm mipmap
else
    if [ $1 = "export" ]; then
        echo "Performing EHR DataFactory $1 step"
        echo "Using $mipmap_map folder"
        # check if there is an existing flattened csv in postgres container and delete it
        if $(docker exec -i $dfcontainer_name bash -c "[ -f /tmp/${export_csv} ]"); then
            echo "Deleting previous created export csv file..."
            docker exec $dfcontainer_name rm -rf /tmp/${export_csv}
        fi
        # which flattening methon? 
        if [ $2 = 'mindate' ]; then
            pivoting_sql=pivot_i2b2_MaxDate.sql
        elif [ $2 = 'maxdate' ]; then
            pivoting_sql=pivot_i2b2_MaxDate.sql
        elif [ $2 = '6months' ]; then
            pivoting_sql=pivot_i2b2_6_months_MRI_Diag.sql
        elif [$2 = 'longitude' ]; then
            pivoting_sql=pivot_i2b2_longitudinal.sql
        else
            echo "Please give flatting method"
            exit 1

        # Copy the sql script to the postgres container
        docker exec -i $dfcontainer_name sh -c "cat > /tmp/pivot_i2b2.sql" < ${mipmap_export}/${pivoting_sql}
        # run the sql script
        docker exec -it $dfcontainer_name psql -q -U $df_db_user -d $db_harmonized -f /tmp/pivot_i2b2.sql
        # check if the flattened csv has been created
        if $(docker exec -i $dfcontainer_name bash -c "[ -f /tmp/${export_csv} ]"); then
            # copy the flatten csv to the Data Factory output folder
            docker cp ${dfcontainer_name}:/tmp/${export_csv} ${mipmap_output}/${export_csv}
            echo "Export csv created!"
        else
            echo "Error! The export csv was not created!"
            exit 1
        fi
    fi
fi
