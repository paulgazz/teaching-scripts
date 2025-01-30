#!/usr/bin/python3

import sys
import os
import subprocess
import csv
import logging
logging.basicConfig(level=logging.INFO)

name_colname = "Student"
nid_colname = "SIS Login ID"

if len(sys.argv) > 1:
  print(f"USAGE: {os.path.basename(sys.argv[0])} < 2024-11-07T0918_Grades-COP3402-24Fall_0001.csv > name_nid_roster.csv")
  exit(1)

reader = csv.reader(sys.stdin, delimiter=',')
writer = csv.writer(sys.stdout, delimiter=',')
header = next(reader)
# namecol = None
# nidcol = None
# for col in range(len(header)):
#     if name_colname == header[col]:
#         namecol = col
#     if nid_colname == header[col]:
#         nidcol = col
namecol = header.index(name_colname)
assert namecol != None
nidcol = header.index(nid_colname)
assert nidcol != None



logging.info(f"name column name: {header[namecol]}")
logging.info(f"name column: {namecol}")

logging.info(f"nid column name: {header[nidcol]}")
logging.info(f"nid column: {nidcol}")

# skip second header row
next(reader)

for row in reader:
    name = row[namecol]
    nid = row[nidcol]
    logging.info(f"name: {name}")
    logging.info(f"nid: {nid}")

    nameparts = name.split(',')
    newnamelist = [ x.strip() for x in nameparts[1:] + [nameparts[0]] ]
    newname = " ".join(newnamelist)

    email = f"{nid}@ucf.edu"
    
    logging.info(f"newname: {newname}")
    logging.info(f"email: {email}")
    roster_row = [ newname, email ]

    writer.writerow(roster_row)
