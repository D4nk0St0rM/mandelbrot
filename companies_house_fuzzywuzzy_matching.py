# FUZZYWUZZY MATCHING

# Finding similar company name and auto matching them
# This program will use NLP and ML technique to match similar company names.

# Matching form common words like "LTD" and "COMPANY" will be discounted autometically in the algorithm.

# THIS CODE CURRENTLY USES THE COMPANY HOUSE ALL COMPANY DATABASE I HAVE IN BIG QUERY 

#INSTALL ALL THE LIBRARIES AND TOOLS NEEDED

from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from apiclient import discovery
import pandas as pd
import datetime
import gspread_dataframe as gd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

########## YOU CAN # OUT THE FOLLOWING !pip INSTALLS AFTER THE FIRST RUN - BUT NEED REINSTALLING IF YOU RESET THE RUNTIME ENVIORNMENT
!pip install fuzzywuzzy[speedup]
!pip install python-Levenshtein
!pip install fuzzywuzzy


#SET ENVIRON VARIABLES

project_id = '<ENTER_GCP_PROJECT>'
KEY_FILE_NAME ='/tmp/bqfuzzy.json'
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/bigquery']


# GO GET PERMISSIONS TO ACCESS API SERVICES
# SAVED SERVICE ACCOUNT JSON CREDENTIALS ARE IN CLOUD BUCKET

!gsutil cp gs://<BUCKET>/bqfuzzy.json /tmp/bqfuzzy.json
# Print the result to make sure the transfer worked.
#!cat /tmp/bqfuzzy.json
credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=KEY_FILE_NAME, scopes=SCOPES)
print("Acquiring credentials...")
print("Authorizing...")
http = credentials.authorize(httplib2.Http())
print("Acquiring service...")
service = discovery.build(serviceName="drive", version="v3", http=http) #, credentials=credentials) - Using both HTTP and credentials caused 'mutually exclusive error'
print("Service acquired!")
print("Acquiring service...")
service2 = discovery.build(serviceName="bigquery", version="v2", http=http) #, credentials=credentials) - Using both HTTP and credentials caused 'mutually exclusive error'
print("Service acquired!")
credentials2 = ServiceAccountCredentials.from_json_keyfile_name(filename=KEY_FILE_NAME, scopes=SCOPES)
gc = gspread.authorize(credentials2)


  
# QUERY BIG QUERY DATA CONTAINING DATASET [COMPANIES HOUSE ALL DATA]

pd.set_option('display.max_columns', 1000)
#THIS IS THE SQL QUERY - SHOWING ONLY A's AT THE MOMENT AND LIMITING 12000 RESULTS

query = "SELECT * FROM cohse.cseprep WHERE CompanyName LIKE 'A%' LIMIT 12000" # LIMIT 2000"
df = pd.io.gbq.read_gbq(query, project_id=project_id, private_key='/tmp/bqfuzzy.json', verbose=False, dialect='standard')

# OK - LETS SEE WHAT WE HAVE FROM THIS!!
df.head()
df.columns

# Frequency of words
# Since we have lots of companies, we will only use companies in LONDON as an example.
# Find the 30 most common words in all company names as we will be expecting them to be repeating a lot even in companies that is not the same, we cannot match company names using them. 
# The way we do it is we will deduct the matching score of a pair if any keywords is present in the names.
# It might be worth playing with the variable matching here of 30 to see if it effects the matching algorithm

df['RegAddress_PostTown'].value_counts().head(30)
from collections import Counter
all_names = df['CompanyName'][df['RegAddress_PostTown']=='LONDON'].unique()
names_freq = Counter()
for name in all_names:
    names_freq.update(str(name).split(" "))
key_words = [word for (word,_) in names_freq.most_common(30)]
print(key_words)

# Matching by Grouping
# Group the names by their 1st character. As the list is too long, it will take forever to match them all at once (F'LOADS x F'ING LOADS pairs to consider). 
# The work around is to match them by groups, assuming if the names are not matched at the 1st character, it is unlikely that they are the same name. 
# Match by Grouping
all_main_name = pd.DataFrame(columns=['sort_gp','names','alias','score'])
all_names.sort()
all_main_name['names'] = all_names
all_main_name['sort_gp'] = all_main_name['names'].apply(lambda x: x[0])

print("Grouping Completed")

# Fuzzy Matching
# Here for each group, we use fuzzywuzzy.token_sort_ratio to matching the names. 
# Different form the basic fuzzywuzzy.ratio which use Levenshtein Distance to calculate the differences, it allow the token (words) in a name to swap order and still give a 'perfect' match. 
# (ref: https://github.com/seatgeek/fuzzywuzzy)

from fuzzywuzzy import fuzz

all_sort_gp = all_main_name['sort_gp'].unique()

def no_key_word(name):
    """check if the name contain the keywords in travel company"""
    output = True
    for key in key_words:
        if key in name:
            output = False
    return output

for sortgp in all_sort_gp:
    this_gp = all_main_name.groupby(['sort_gp']).get_group(sortgp)
    gp_start = this_gp.index.min()
    gp_end = this_gp.index.max()
    for i in range(gp_start,gp_end+1):
    
        # if self has not got alias, asign to be alias of itself
        if pd.isna(all_main_name['alias'].iloc[i]):
            all_main_name['alias'].iloc[i] = all_main_name['names'].iloc[i]
            all_main_name['score'].iloc[i] = 100
        
        # if the following has not got alias and fuzzy match, asign to be alias of this one
        for j in range(i+1,gp_end+1):
            if pd.isna(all_main_name['alias'].iloc[j]):
                fuzz_socre = fuzz.token_sort_ratio(all_main_name['names'].iloc[i],all_main_name['names'].iloc[j])
                if not no_key_word(all_main_name['names'].iloc[j]):
                    fuzz_socre -= 10
                if (fuzz_socre > 85):
                    all_main_name['alias'].iloc[j] = all_main_name['alias'].iloc[i]
                    all_main_name['score'].iloc[j] = fuzz_socre
                    
        if i % (len(all_names)//10) == 0:
            print("progress: %.2f" % (100*i/len(all_names)) + "%")
            
all_main_name[(all_main_name['names']!=all_main_name['alias']) & (all_main_name['alias'].notna())]

#LETS SEE WHAT THIS MEANS IN DATA SIZES
len(all_main_name['alias'].unique())
all_main_name.head()
all_main_name.info()
all_main_name[(all_main_name['names']!=all_main_name['alias']) & (all_main_name['alias'].notna())].shape[0]


# Groups Normally Found:
# they are usually differ in spelling by 1 character: missing an 'L' or 'I' or 'S' highly similar names: 'No.3' instead of 'No.2' or 'EB' instread of 'EH' fairly similar names: 'CATS AND HAMMERS PRODUCTIONS LIMITED' and TATS AND AMMERS PRODUCTIONS LIMITED' For type 1 and 2 matches it could be the same company, the diffeernce in names could be an intentional alteration or simply a typo. But it is not likely the same company for type 3 matched, it seems more like a coincidence.
# To further confirm, manual work need to be done.

# NOW PUSHING INTO A SPREADSHEET

#THIS IS JUST THE ID FROM THE URL OF THE GOOGLE SHEET
worksht = gc.open_by_key('1T_WNf1AMB11fzTag23DWGGxoNIMwCyT_Xw8076vCYCo')

#DEFINE A CONVERSION FOR SPREADSHEET ROW | COL REF FROM DATA TO PUSH RESULTS

def numberToLetters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result;
        q = q//26 - 1
    return result

#SET DATAFRAME TO USE AS DATA
df2 = all_main_name[(all_main_name['names']!=all_main_name['alias']) & (all_main_name['alias'].notna())]
df2.head()
dataframe2 = df2
df3=all_main_name
df3.head()
dataframe3 = df3


#taking dataframe count rows and columns 
pd.set_option('display.max_columns', 1000)
num_lines, num_columns = df2.shape
num_lines2, num_columns2 = df3.shape


#add worksheet with timestamp as name and populate
ws = worksht.add_worksheet(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), (num_lines+1), (num_columns))
cell_list = ws.range('A2:'+numberToLetters(num_columns)+str(num_lines+1))
set_with_dataframe(ws, dataframe2, row=1, col=1, include_index=False, include_column_header=True, resize=False, allow_formulas=True)
df2.head()

ws2 = worksht.add_worksheet(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), (num_lines+1), (num_columns))
cell_list = ws2.range('A2:'+numberToLetters(num_columns2)+str(num_lines2+1))
set_with_dataframe(ws2, dataframe3, row=1, col=1, include_index=False, include_column_header=True, resize=False, allow_formulas=True)
df3.head()


#end routine
print("Requested operations complete")

