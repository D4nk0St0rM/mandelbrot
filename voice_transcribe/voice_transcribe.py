
import csv
import datetime
import io
import json
import time
import traceback
import logging
import os
import requests

from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
from google.cloud import dlp
from google.cloud import language
from google.cloud import pubsub, pubsub_v1
from google.cloud import storage
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account

PROJECT_ID = 'mmvoice'
VOICEFILEBUCKET = 'gs://mmc1/'
#UPDATECRED = 'gs://mmvoice_creds/service-account2.json'
CREDFILE = 'mmkey.json'
FILELIST = 'py1_gspathfiles.txt'
FILES='py4_files.txt'


#Get Permissions needed for ML AI VOICE APIs
def gcs_credentials():
    scopes = [
        'https://www.googleapis.com/auth/devstorage.full_control',  # storage scope
        'https://www.googleapis.com/auth/pubsub',  # pub/sub scope
        'https://www.googleapis.com/auth/cloud-platform',  # speech-to-text scope
	'https://www.googleapis.com/auth/cloud-vision',
        'https://www.googleapis.com/auth/bigquery'  # BiqQuery
    ]
    service_account_file = 'mmkey.json'

    return service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)

gcs_credentials()


#convert the voice files into text files

def transcribe_gcs1(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print (u'Transcript: {}'.format(result.alternatives[0].transcript))
	string1 = str((u'Transcript: {}'.format(result.alternatives[0].transcript)))
        return string1 #(format(result.alternatives[0].transcript))


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
	#transcript = (u'Transcript{}'.format(result.alternatives[0].transript))
	
	print (u'Transcript: {}'.format(result.alternatives[0].transcript))
	string1 = str((u'Transcript: {}'.format(result.alternatives[0].transcript)))
	return string1 #(format(result.alternatives[0].transcript))
	print string1


def transcribe_gcs2(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-GB')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=1000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print (u'Transcript: {}'.format(result.alternatives[0].transcript))
	string1 = ((u'Transcript: {}'.format(result.alternatives[0].transcript)))
        print ('Confidence: {}'.format(result.alternatives[0].confidence))
	string2 = (('Confidence: {}'.format(result.alternatives[0].confidence)))
	return string1
	return string2











# define empty list
pyurl = []
pyfile = []

with open(FILELIST,'r') as filelisting:
	pyurl = [current_pyurl.rstrip() for current_pyurl in filelisting.readlines()]

with open(FILES,'r') as filename:
	pyfile = [current_pyfile.rstrip() for current_pyfile in filename.readlines()]

counti = 0

for pu in pyurl:
	url = pu
	print url
	string1 = transcribe_gcs2(url)
	str1 = string1
	fle = "%s.txt" %pyfile[counti]
	with open(fle,"w") as fle:
		fle.write(str1)
	#transcribe_gcs(url)
	#with open(("%s.txt" %fle),'w') as ftxt:
	#	ftxt.write()
	counti += 1
print("Bye")







