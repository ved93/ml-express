


# In this analysis, I will use an English word list from https://github.com/dwyl/english-words and pre-process the text by removing hashtags, usernames and non-alphanumeric symbols.

import pandas as pd
import re
# words = pd.read_table('https://raw.githubusercontent.com/dwyl/english-words/master/words.txt')
# words.columns=['word']
# words = words['word'].str.lower().values.tolist()
# data['clean_text'] = data.Tweet_Text.apply(lambda x: ' '.join([i for i in x.split(' ') if not (i.startswith('@') or i.startswith('#'))]))
# data['clean_text'] = data.clean_text.str.lower().str.replace('[^a-zA]', ' ')
# non_list = {}
# for sent in tqdm(data.clean_text.str.split().values):
#   for token in sent:
#     if token not in words:
#       non_list[token] = 1 if token not in non_list else non_list[token]+1
# pd.Series(non_list).sort_values(ascending=False).head(30)



def preprocess(reviewtext):
    reviewtext = reviewtext.str.replace("(<br/>)","")
    reviewtext = reviewtext.str.replace("\\w*\\d\\w*","") # Digits &amp; Word Containing digits
    reviewtext = reviewtext.str.replace("[%s]"%re.escape(string.punctuation),"") #Punctuations
    reviewtext = reviewtext.str.replace(" +","") #Extra Spaces
     
    return reviewtext
 
# data['reviews.text'] = preprocess(data['reviews.text'])


def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text
# train['text'] = train['text'].apply(lambda x:clean_text(x))


