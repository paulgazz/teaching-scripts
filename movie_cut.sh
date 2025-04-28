#!/bin/bash

if [ $# -lt 2 ]; then
	echo "USAGE: $(basename ${0}) movie_name length [backup_movie_dir]"
	echo "NOTE: this cuts down a given movie_name to length, saving the original to backup_movie_dir/movie_name, which defaults to \"back/\".  ffmpeg will halt if the backup file exists already"
	exit 1
fi

mov="${1}"
length="${2}"
backupdir="${3-back}"
backup="${backupdir}/${mov}"

mkdir -p "${backupdir}"
mv -n "${mov}" "${backup}" && ffmpeg -i "${backup}" -t ${length} -c:v copy -c:a copy ${mov}
