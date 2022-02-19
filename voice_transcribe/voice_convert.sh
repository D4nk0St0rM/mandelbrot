#~!/bin/bash
#converts audio files to FLAC encoding for Voice to text conversion

set -x

echo "here we go then...."

VOICEBUCKET='gs://mmv1'
CONVERTBUCKET='gs://mmc1'
TEMPFILE='temp'

mkdir $TEMPFILE

gsutil ls -r $VOICEBUCKET > 'voicefiles.txt'
VOICEFILES='voicefiles.txt'

cat $VOICEFILES | while read vf
do
    gsutil cp $vf $TEMPFILE

done

ls -d -1 $TEMPFILE/*.* > 'convertfiles.txt'

CONVERTFILES='convertfiles.txt'


cat $CONVERTFILES | while read cf
do
	ffmpeg -i $cf -ar 16000 -c:a flac $cf'.flac' < /dev/null
	rm $cf
	echo 'Thats file '$cf' done....'
done

ls $TEMPFILE >'fileno.txt'
FILENO='fileno.txt'

echo 'All files converted'

sudo chmod -R $TEMPFILE

cat $FILENO | while read fn

do
	gsutil cp $TEMPFILE'/'$fn $CONVERTBUCKET'/'$fn
	rm $TEMPFILE'/'$fn
done

rm $FILENO
rm $VOICEFILES $CONVERTFILES
rm -R $TEMPFILE

