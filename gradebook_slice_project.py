#!/usr/bin/python3

# https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-grades-in-the-Gradebook/ta-p/807

# required_columns = [ "Student Name", "Student ID", "SIS User ID", "SIS Login ID", "Section" ]

required_columns = [ "Student", "ID", "SIS User ID", "SIS Login ID", "Section" ]

import sys
import os
import subprocess
import csv
import logging
logging.basicConfig(level=logging.INFO)

if len(sys.argv) < 2:
  print(f"USAGE: {os.path.basename(sys.argv[0])} project < 2024-11-07T0918_Grades-COP3402-24Fall_0001.csv > project_slice.csv")
  print("  project is the name of an assignment, which will be matched using startswith against a header column name")
  exit(1)

project_colname = sys.argv[1]
  
reader = csv.reader(sys.stdin, delimiter=',')
writer = csv.writer(sys.stdout, delimiter=',')
header = next(reader)

required_cols = [ header.index(x) for x in required_columns ]

for col in required_cols:
  assert col != None

# projectcol = header.index(project_colname)
projectcol = None
for col in range(len(header)):
    if header[col].startswith(project_colname):
        projectcol = col
assert projectcol != None

logging.info(f"required columns: {required_columns}")
logging.info(f"required cols: {required_cols}")

logging.info(f"project column name: {header[projectcol]}")
logging.info(f"project column: {projectcol}")

header_row = [ header[x] for x in required_cols ] + [ header[projectcol] ]
writer.writerow(header_row)

for row in reader:
  sliced_row = [ row[x] for x in required_cols ] + [ row[projectcol] ]
  writer.writerow(sliced_row)
