#!/bin/bash

START=$(date +%s)

rm *.txt
rm *.mp4
rm *.wav
rm background_cropped.jpg

python3 image_generator.py
python3 random_citation.py
python3 tts.py
python3 video_generator_1.py

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Время выполнения скрипта: $DIFF секунд"

mpv output_video_with_text.mp4
