#!/bin/bash

if [ $# -lt 1 ]; then
	echo "USAGE: $(basename ${0}) lecture_date [extension]"
	echo "EXAMPLE: $(basename ${0}) 2025-01-13"
  echo "NOTE: the extension defaults to webm"
	exit 1
fi

date=${1}
ext=${2-webm}

movie_concat.sh ${date} *${date}*.${ext}
