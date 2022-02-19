import csv
import datetime
import io
import json
import logging
import os
import time
import traceback
from google.oauth2 import service_account
from dotenv import load_dotenv
import requests
from google.api_core.exceptions import NotFound
from google.cloud import dlp
from google.cloud import language
from google.cloud import pubsub, pubsub_v1
from google.cloud import storage
from google.cloud.language import enums
from google.cloud.language import types
from google.oauth2 import service_account



project_id = 'mmvoice'
textbuck = 'gs://mmvoice_files1/'
credfile = 'mmkey.json'


def gcs_credentials():
    scopes = [
        'https://www.googleapis.com/auth/devstorage.full_control',  # storage scope
       # 'https://www.googleapis.com/auth/pubsub',  # pub/sub scope
        'https://www.googleapis.com/auth/cloud-platform',  # speech-to-text scope
        'https://www.googleapis.com/auth/bigquery'  # BiqQuery
    ]
    service_account_file = credfile

    return service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)

gcs_credentials()


###Entities

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#gcs_uri = 'gs://mmvt/REC13b415bb.wav.flac.txt'
#gcs_uri = 'gs://mmvt/REC13b415bb.wav.flac.txt'
#gcs_uri = 'gs://mmvt/REC5495da0b.wav.flac.txt'
#gcs_uri = 'gs://mmvt/REC54ce9b72.wav.flac.txt'
gcs_uri  = 'gs://mmvt/REC70e8213b.wav.flac.txt'
#f5 = 'gs://mmvt/REC70ecb5ba.wav.flac.txt'



client = language.LanguageServiceClient()

# Instantiates a plain text document.
document = types.Document(
    gcs_content_uri=gcs_uri,
    type=enums.Document.Type.PLAIN_TEXT)

entities = client.analyze_entities(document).entities

for entity in entities:
	entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
               'EVENT', 'LETTER / COMMS', 'CONSUMER_GOOD', 'OTHER')
	for entity in entities:
    		print('=' * 20)
    		print(u'{:<16}: {}'.format('name', entity.name))
    		print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
    		#print(u'{:<16}: {}'.format('metadata', entity.metadata))
    		print(u'{:<16}: {}'.format('salience', entity.salience))
    		#print(u'{:<16}: {}'.format('wikipedia_url',
          		#entity.metadata.get('wikipedia_url', '-')))
	


client = language.LanguageServiceClient()

    # Instantiates a plain text document.
document = types.Document(
        gcs_content_uri=gcs_uri,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

for token in tokens:
	print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))


#syntax_file(gcs_uri)

