#!/bin/bash

# Save buffer as a ps file in emacs:
# C-u M-x ps-print-buffer

if [ $# -lt 1 ]; then
	echo "USAGE: ${0} file.ps [file.png]"
	exit 1
fi

psfile="${1}"
stem="${psfile%.ps}"
pdffile="${stem}.pdf"
pngfile="${stem}.png"

if [ ! -f "${psfile}" ]; then
	echo "${psfile} does not exist"
	exit 1
fi

ps2pdf "${psfile}" "${pdffile}" 
pdfcrop "${pdffile}" "${pdffile}"
gs -dSAFER -dBATCH -dNOPAUSE -dEPSCrop -r600 -sDEVICE=pngalpha -sOutputFile="${pngfile}" "${pdffile}"
