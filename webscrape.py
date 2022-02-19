# pip install tldextract

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
  
# to search 
query = "IT support company hampshire"
  
for j in search(query, tld="co.uk", num=30, stop=1, pause=2): 
    print(j)


import nltk
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os, os.path, csv
import tldextract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

my_path = "/home/WebScrape/"
my_file = "domainslist.txt"

url_list = open(my_path+my_file).read().splitlines()
#print(url_list)


for url in url_list:
    try:
        ext = tldextract.extract(url)
        filename = ext.domain
        import os, ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
            req = Request(url,headers=hdr)
            html = urlopen(req).read()
            soup = BeautifulSoup(html)
            for script in soup(["script", "style"]):
                script.extract()
                text = soup.get_text()

# break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        words = word_tokenize(text)


# removes punctuation and numbers
        wordsFiltered = [word.lower() for word in words if word.isalpha()]

        filtered_words = [word for word in wordsFiltered if word not in stopwords.words('english')]
        print(filename)
  
        wc = WordCloud(max_words=10000, margin=10, background_color='white',
                    scale=3, relative_scaling = 0.5, width=500, height=400,
                    random_state=1).generate(' '.join(filtered_words))

        plt.figure(figsize=(20,10))
        plt.imshow(wc)
        plt.axis("off")
  #plt.show()
        wc.to_file(filename+".png")
    except:
        pass

    
