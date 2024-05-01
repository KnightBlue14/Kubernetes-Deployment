from bs4 import BeautifulSoup
import requests
import pandas as pd

ah = 'https://wh40k.lexicanum.com/wiki/Thought_for_the_day_(A_-_H)'
ip = 'https://wh40k.lexicanum.com/wiki/Thought_for_the_day_(I_-_P)'
qz = 'https://wh40k.lexicanum.com/wiki/Thought_for_the_day_(Q_-_Z)'
pages = [ah,ip,qz]
quotes = []
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept-Language':'en-US,en:q=0.5'})
for i in pages:
    webpage = requests.get(i,headers=HEADERS)

    soup = BeautifulSoup(webpage.content,'lxml')

    links = soup.find_all('i')

    for link in links:
        if 'Chapter Approved' in link.text.strip():
            pass
        elif 'last accessed' in link.text.strip():
            pass
        elif 'Source' in link.text.strip():
            pass
        elif 'Thought for the day' in link.text.strip():
            pass
        elif 'corrected spelling' in link.text.strip():
            pass
        elif 'Index Astartes' in link.text.strip():
            pass
        elif 'Biel-Tan Scorpion Super Heavy Tank, Description' in link.text.strip():
            pass
        elif 'The Betrayer' in link.text.strip():
            pass
        else:
            quotes.append(link.text.strip())

thoughts = []

for line in quotes:
    try:
        print(line)
    except Exception:
        pass
    finally:
        thoughts.append(line)

df = pd.DataFrame(thoughts)

df.to_csv('thought_for_the_day.csv',index=False)