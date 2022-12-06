#!/bin/bash

ALL_FILES=$(find runs/detect/exp2/labels -type f -name "*.txt")

OIFS="$IFS"
IFS=$'\n'
for FILE in $ALL_FILES; do

	# if file has more than 1 line or 0 line print
	NO_OF_LINES=$(wc -l $FILE | awk '{print $1}')

	if [[ $NO_OF_LINES -gt 1 ]] || [[ $NO_OF_LINES -eq 0 ]]; then
		echo "$FILE"
		cp $FILE runs/detect/exp2/defects/
		cp /home/pj/Downloads/unlabeled/"$($FILE | cut -d'/' -f 5)".jpg runs/detect/exp2/defects/
	fi
done

# DEFECT_FILES=$(find runs/detect/exp2/defects -type f -name "*.txt")
# for FILE in $DEFECT_FILES; do
# 	cp /home/pj/Downloads/unlabeled/"$($FILE | cut -d'/' -f 5)".jpg runs/detect/exp2/defects/
# done
IFS="$OIFS"
