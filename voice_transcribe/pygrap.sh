
#~!/bin/bash
#converts audio files to FLAC encoding for Voice to text conversion

set -x

echo "here we go then...."

CONVERTBUCKET='gs://mmc1'


gsutil ls -r $CONVERTBUCKET > 'py1_gspathfiles.txt'
VOICEFILES='py1_gspathfiles.txt'


echo 'URLS in file.... ready for python'

cat $VOICEFILES | while read fn
do
    basename $fn >> 'py4_files.txt'
done



python voice_transcribe.py
