import os
from jinja2 import Environment, FileSystemLoader


def java_unpivot_command(csv_name):
    # get csv_file without extension
    name_core = os.path.splitext(csv_name)[0]
    selected_name = 'selected_' + name_core + '.txt'
    unpivoted_name = 'unpivoted_' + name_core + '.txt'
    java_cmd = ("java -jar /opt/MIPMapReduced.jar -unpivot /opt/source/{0}"
                " /opt/postgresdb.properties/mipmap-db.properties \"Attribute\""
                " /opt/map/{1} -u /opt/map/{2}").format(csv_name, selected_name, unpivoted_name)
    return java_cmd


def produce_run_sh_script(output_path, csvs):
    """Produce the run.sh script for preprocessing step.
    Arguments:
    :param csvs: list with csv file names
    :param output_path: the folder path where the run.sh will be saved
    """
    first_part = """\
#!/bin/sh
dockerize -template /opt/postgresdb.properties/mipmap-db.properties.tmpl:/opt/postgresdb.properties/mipmap-db.properties
dockerize -template /opt/postgresdb.properties/i2b2-db.properties.tmpl:/opt/postgresdb.properties/i2b2-db.properties

"""
    last_part = """\
# Encounter and Patient Mapping Section
echo "Generating patient_num and encounter_num"

java -jar /opt/MIPMapReduced.jar -generate_id /opt/map/patientmapping.properties

java -jar /opt/MIPMapReduced.jar -generate_id /opt/map/encountermapping.properties
"""
    middle_part = ''
    if len(csvs) != 0:
        for csv_name in csvs:
            middle_part = middle_part + java_unpivot_command(csv_name) +'\n'

    all_parts = first_part + middle_part + last_part
    file_path = os.path.join(output_path, 'run.sh')
    with open(file_path, 'w') as bashscript:
        bashscript.write(all_parts)

def produce_unpivot_files(output_path, csv_name, selected, unpivoted):
    """Creates the two config files for unpivoting the given csv file
    Arguments:
    :param csv_path: the csv file path to be unpivoted
    :param output_path: the output folder path where the config files will be saved
    :param selected: list or set with the column names to be preserved
    :param unpivoted: list or set with the column names to be unpivoted
    """
    # get csv_file without extension
    name_core = os.path.splitext(csv_name)[0]
    selected_name = 'selected_' + name_core + '.txt'
    unpivoted_name = 'unpivoted_' + name_core + '.txt'
    selected_filename = os.path.join(output_path, selected_name)
    unpivoted_filename = os.path.join(output_path, unpivoted_name)
    
    # write the columns to be unpivoted into the unpivot config file
    with open(unpivoted_filename, 'w') as unpiv:
        for column in unpivoted:
            unpiv.write(column + '\n')
    # write the columns that are going to be selected 
    with open(selected_filename, 'w') as selec:
        for column in selected:
            selec.write(column + '\n')



def produce_encounter_properties(output_path, csv_name, cvisit_id, cpatient_id, hospital_code):
    """Creates the encountermapping.properties config file.
    Arguments:
    :param output_path: the output folder path where encountermapping.properties will be stored
    :param csv_name: the csv name with all the patient visits
    :param cvisit_id: the column name that holds the visit id
    :param cpatient_id: the column name that holds the patient id
    :param hospital_code: string for hospital name/code
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    env_path = os.path.join(my_path, 'templates')
    env = Environment(loader=FileSystemLoader(env_path))
    template = env.get_template('encountermapping.j2')
    hospital_with_quotes = '\"' + hospital_code + '\"'
    vars = {'visits_csv': csv_name,
            'cvisit_id': cvisit_id,
            'cpatient_id': cpatient_id,
            'hospital_code': hospital_with_quotes}

    encounter_properties = os.path.abspath(os.path.join(output_path, 'encountermapping.properties'))
    template.stream(vars).dump(encounter_properties)


def produce_patient_properties(output_path, csv_name, cpatient_id, hospital_code):
    """Creates the patientmapping.properties config file.
    Arguments:
    :param output_path: the output folder path where encountermapping.properties will be stored
    :param csv_name: the csv name with all the patient visits
    :param cpatient_id: the column name that holds the patient id
    :param hospital_code: string for hospital name/code
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    env_path = os.path.join(my_path, 'templates')
    env = Environment(loader=FileSystemLoader(env_path))
    template = env.get_template('patientmapping.j2')
    hospital_with_quotes = '\"' + hospital_code + '\"'
    vars = {'patients_csv': csv_name,
            'cpatient_id': cpatient_id,
            'hospital_code': hospital_with_quotes}

    patient_properties = os.path.abspath(os.path.join(output_path, 'patientmapping.properties'))
    template.stream(vars).dump(patient_properties)