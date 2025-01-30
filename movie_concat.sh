#!/bin/bash

if [ $# -lt 2 ]; then
	echo "USAGE: $(basename ${0}) movie_name movie1 [movie2 [movie3 [...]]]"
	echo "NOTE: this generates a movie with the same extension as movie1, so if the others have a different extension they will end up being transcoded."
	exit 1
fi

mov="${1}"
mext="${2##*.}"
shift
movies="${@}"

mfile="movie_files.${mov}.txt"

# echo ${@} | xargs -L 1 echo "file"

for movie in ${movies}; do
	echo "file ${movie}"
done | tee ${mfile}

# for i in lec5a.webm Kooha-2024-08-28-09-32-08.webm Kooha-2024-08-28-09-42-34.webm; do echo $i; done | xargs -L1 echo | xargs -L 1 echo file > lec5.txt

ffmpeg -f concat -i "${mfile}" -c copy "${mov}.${mext}"

echo "${mov}.${mext}"
