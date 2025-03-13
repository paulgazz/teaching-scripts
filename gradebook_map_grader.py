#!/usr/bin/python3

# this example first slices out the project column, then runs the grader script for each row
# example: gradebook_slice_project.py "git exercise" < 2025-01-30T0511_Grades-COP3402-25Spring_0002.csv | gradebook_map_grader.py "git exercise" bash git_grader.sh | tee 2025-01-30T0511_Grades-COP3402-25Spring_0002_git.csv 

# https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-grades-in-the-Gradebook/ta-p/807

# required_columns = [ "Student Name", "Student ID", "SIS User ID", "SIS Login ID", "Section" ]

required_columns = [ "Student", "ID", "SIS User ID", "SIS Login ID", "Section" ]
nidindex = required_columns.index("SIS Login ID")

import sys
import os
import subprocess
import csv
import logging
logging.basicConfig(level=logging.INFO)

if len(sys.argv) < 3:
  print(f"USAGE: {os.path.basename(sys.argv[0])} project grader [grader_arg] [...] < 2024-11-07T0918_Grades-COP3402-24Fall_0001.csv > project_slice.csv")
  print("  project is the name of an assignment, which will be matched using startswith against a header column name")
  print("  grader is the name of an assignment, which will be matched using startswith against a header column name.  grader takes nid and project name and the last line of output should have the grade, which will be converted to a floating point number.")
  exit(1)

project = sys.argv[1]
grader = sys.argv[2:]
  
reader = csv.reader(sys.stdin, delimiter=',')
writer = csv.writer(sys.stdout, delimiter=',')
header = next(reader)

required_cols = [ header.index(x) for x in required_columns ]

for col in required_cols:
  assert col != None

# projectcol = header.index(project)
projectcol = None
for col in range(len(header)):
    if header[col].startswith(project):
        projectcol = col
assert projectcol != None

logging.info(f"required columns: {required_columns}")
logging.info(f"required cols: {required_cols}")

logging.info(f"project column name: {header[projectcol]}")
logging.info(f"project column: {projectcol}")

# skip second header row
next(reader)

header_row = [ header[x] for x in required_cols ] + [ header[projectcol] ]
writer.writerow(header_row)

def grade(nid, old_grade):
  command = grader + [ nid ]
  logging.info(command)
  p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, err = p.communicate()
  rc = p.returncode
  logging.info(output)
  outlines = output.decode('ascii', errors="ignore").splitlines()
  logging.info(outlines)
  new_grade = float(outlines[-1])
  return new_grade

for row in reader:
  nid = row[required_cols[nidindex]]
  logging.info(f"nid: {nid}")
  old_grade = row[projectcol]
  logging.info(f"old_grade: {old_grade}")
  new_grade = grade(nid, old_grade)
  logging.info(f"nid: {nid}")
  logging.info(f"new_grade: {new_grade}\n")
  updated_row = [ row[x] for x in required_cols ] + [ new_grade ]
  writer.writerow(updated_row)
