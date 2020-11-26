#!/usr/bin/env-python3

import sys
import csv

#Need to separate Subject ID's from MRI IDs and also put Visit ID's in the volumes rows. Lets just pick the first one... And if there is another MRI for the same patient take the second one... and so on and so on... until all MRIs of the 933 Patients are connected with one Visit (of the correct Patient...).
print('Argument list:', str(sys.argv))


def separateSubjID_MRIID(in_file, out_file, visitsDict):
  c_rows=0;
  
  with open(out_file, 'w') as volumes_new:
    with open(in_file, 'r') as volumes:
      reader=csv.reader(volumes)
       #intervention putting Visit-ID after Subject-ID... <------ 
      headers=next(reader)
      new_headers=headers
      new_headers.insert(1, 'VISIT_ID')
      #print(new_headers)
      writer=csv.writer(volumes_new)
      writer.writerow(new_headers)
      for row in reader:
          patient_id = row[0].split('_')[0]
          visit_id = visitsDict[patient_id].pop()
          new_row = row[1:]
          new_row = [patient_id, visit_id] + new_row
          writer.writerow(new_row)


#read the DB_EHR_subset and return a Dictionary with SubjectID->first VisitID
def loadVisitIDs(ehr_file):
  ehrFile=csv.DictReader(open(ehr_file))
  visitIDsDict = dict()
  for row in ehrFile:
    if row["SUBJECT_CODE"] in visitIDsDict:
      visitIDsDict[row["SUBJECT_CODE"]].append(row["VISIT_ID"])
    else:
      visitIDsDict[row["SUBJECT_CODE"]] = [row["VISIT_ID"]]
  print("Total of %d Patients with at least one visit" % len(visitIDsDict))
  return visitIDsDict

#rewrite a CSV... we do not want the unneeded quotes!..
def rewriteCSV(quotedCSV):
  newCSV=quotedCSV.split('.')[0]+'2.csv'
  with open(newCSV, 'w') as new_csv:
    with open(quotedCSV, 'r') as old_csv:
      reader=csv.reader(old_csv)
      writer=csv.writer(new_csv)
      for row in reader:
        writer.writerow(row)

rewriteCSV('DB_EHR_subset_cp.csv')
visitIDs = loadVisitIDs('DB_EHR_subset_cp2.csv')#returns Dictionary
separateSubjID_MRIID(sys.argv[1], sys.argv[2], visitIDs)

