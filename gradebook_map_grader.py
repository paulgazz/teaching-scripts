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
import argparse

parser = argparse.ArgumentParser(description='Map students to grades in a gradebook csv given a grading script.')
parser.epilog = f'''EXAMPLE: {parser.prog} codegen2 "codegen2 project" bash cop3402_grader.sh codegen2 CodeGen < gradebook.csv > codegen2_grades.csv
'''
# \tcat 2025-03-13T1349_Grades-COP3402-25Spring_0002.csv | gradebook_slice_project.py "codegen3 project" | {parser.prog} "codegen3 project" bash cop3402_grader.sh codegen3 CodeGen | tee 2025-03-13T1349_Grades-COP3402-25Spring_0002_codegen3.csv

parser.add_argument('project', type=str,
                    help='the name of an assignment, which will be matched using startswith against a header column name')
parser.add_argument('grader', type=str, nargs='+',
                    help='a grading script; it is passed an nid as its last argument; the last line of output should have the grade, which will be converted to a floating point number')
parser.add_argument('--penalty', '--late-penalty', '-p', type=float,
                    default=0.0,
                    help='the amount of late penalty to deduct from the new grade; default to 0, no penalty')

args = parser.parse_args()

project = args.project
grader = args.grader
penalty = args.penalty

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

header_row = [ header[x] for x in required_cols ] + [ header[projectcol] ]
writer.writerow(header_row)


def grade(nid, old_grade, penalty=0.0):
  command = grader + [ nid ]
  logging.info(command)
  p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output, err = p.communicate()
  rc = p.returncode
  logging.info(output)
  outlines = output.decode('ascii', errors="ignore").splitlines()
  logging.info(outlines)
  # convert the student's current grade to float if possible
  try:
    old_grade = float(old_grade)
  except ValueError:
    old_grade = 0.0
  # convert the student's new grade to float.  the grader script is required to return a float
  new_grade = float(outlines[-1])
  # apply a late penalty (if not zero) and only update the grade if it's higher than the old grade
  grade_to_update = max(new_grade - penalty, old_grade)
  return grade_to_update

for row in reader:
  nid = row[required_cols[nidindex]]
  if len(nid) == 0:
    writer.writerow(row)
    continue
  logging.info(f"nid: {nid}")
  old_grade = row[projectcol]
  logging.info(f"old_grade: {old_grade}")
  new_grade = grade(nid, old_grade, penalty=penalty)
  logging.info(f"nid: {nid}")
  logging.info(f"new_grade: {new_grade}\n")
  updated_row = [ row[x] for x in required_cols ] + [ new_grade ]
  writer.writerow(updated_row)
