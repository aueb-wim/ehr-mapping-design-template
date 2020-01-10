# ehr-mapping-design-template

[![AUEB](https://img.shields.io/badge/AUEB-RC-red.svg)](http://rc.aueb.gr/el/static/home) [![HBP-SP8](https://img.shields.io/badge/HBP-SP8-magenta.svg)](https://www.humanbrainproject.eu/en/follow-hbp/news/category/sp8-medical-informatics-platform/)

This is a EHR mapping design template containing the folders and scripts needed to configure and run the EHR DataFactory pipeline on a machine.

## Requirements

- docker (v18)
- docker-compose (v1.22 - v1.8)

Datafactory User must be in the user group “docker”, so the scripts will run without the “sudo” command.
To do that, follow the below instructions:
Add the docker group if it doesn't already exist:

```shell
 sudo groupadd docker
 ```

Add the connected user "$USER" to the docker group. Change the user name to match your preferred user if you do not want to use your current user:

```shell
sudo gpasswd -a $USER docker
```

Either do a newgrp docker or log out/in to activate the changes to groups.
You can use `$ docker run hello-world`  to check if you can run docker without sudo.

## Instructions

1. We create a docker container with the name `demo_postgres` with the 3 databases which are needed by EHR DataFactory pipeline. These databases are:

- mipmap
- i2b2_capture
- i2b2_harmonized

To create this postgres container run:

```shell
sh build_postgres.sh
```

**Caution!** If `demo_postgres` container is already exist the script will drop the 3 databases and will create new ones.

2. Place the hospital csv files into the *source* folder and then launch MIPMap. Store the mapping xml file to the design root directory.

## Preprocess step configuration files

Update the following files located in the `preprocess_step` folder

- EncounterMapping.properties
- PatientMapping.properties
- run.sh

Create the txt files for unpivoting process (selected and unpivot txt files for each raw input csv)

The final configurations files which are located in the `preprocess_step` folder, will be the following:

- EncounterMapping.properties
- PatientMapping.properties
- run.sh
- selected<input_csv 1>.txt (columns that will **not** be unpivoted in the 1st input csv)
- unpivoted<input_csv 1>.txt (columns that will be unpivoted in the 1st input csv)
- ...
- selected<input_csv N>.txt
- upivoted<input_csv N>.txt

The total number of the configuration file will be **3 + 2N**, where **N** is the number of input csv files that needed to be unpivoted.

## Capture step configuration files

1. Update(or replace) the following csv files in `source` folder with metadata:
    - `hospital_metadata.csv` (metadata about hospital's raw input csv files)
    - `cde_metadata.csv` (metadata about the pathology data model)
2. For each hospitals's raw input csv file, we create a doublicate csv file in the `source` folder with the exact same name as the original. Each of those files must contain the original headers(column's name) and a small number of rows filled with data (actual or fictional). Those dublicate files must be in line with the metadata in the hospital_metadata.csv file.
3. Design the mapping task by using **MIPMAP** and save it in the main folder with the name `map.xml`
4. Then run:

```shell
  sh templator.sh capture
````

The last script creates a template xml `map.xml.tmpl` file in the folder `capture_step`.

The final configurations files are located in the `capture_step` folder and are the following:

- map.xml.tmpl  
- run.sh

## Harmonization step configuration files

1. Design the mapping task by using **MIPMAP** and save it in the main folder with the name `mapHarmonize.xml`
2. Then run:

```shell
  sh templator.sh harmonize
```

The last script creates a template xml `mapHarmonize.xml.tmpl` file in the folder `harmonize_step`.

The final configurations files are located in the `harmonize_step` folder and are the following:
  
- mapHarmonize.xml.tmpl
- run.sh

## Testing EHR pipeline

### Step_1 - preprocess step

In the main folder we run:

```shell
  sh ingestdata.sh preprocess
```

**Check** if the auxiliary files (EncounterMapping.csv, PatientMapping,csv and the unpivoted csv's) are created in the `source` folder

### Step_2 - capture step

Caution! Auxilary files must be created first by the preprocessing step.

In the main folder we run:

```shell
  sh ingestdata.sh capture
```

**Check** if the `i2b2_capture` database is populated with data in the postgres container.

### Step_3 - harmonization step

In the main folder we run:

```shell
  sh ingestdata.sh harmonize
```

**Check** if the `i2b2_harmonized` database is populated with data in the postgres container.

If every of the above step has run successfully in our local machine, we are ready to upload the EHR mapping configuration files into the actual DataFactory installation on Hospital node.
