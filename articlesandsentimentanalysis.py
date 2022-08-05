"""
@author: Aditi
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

data = pd.read_excel('articles.xlsx')

#summary of data
data.describe()

#summary of columns
data.info()

#count of articles form each source
data.groupby(['source_id'])['article_id'].count()

#number of reactions per publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping engagement_comment_plugin_count column
data = data.drop('engagement_comment_plugin_count', axis=1)

#function to flag keywords
def keyword_flag(keyword):
    keywordflag = []
    for x in range(len(data)):
        try:
            title = data['title'][x]
            if keyword in title:
                flag = 1
            else:
                flag = 0
        except:
            flag = 0
        keywordflag.append(flag)
    return keywordflag
Key_Word = input()
data['keyword_flag'] = pd.Series(keyword_flag(Key_Word))

#SentimentIntensityAnalyser
#lists for negative, positive and neutral sentiment
title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

#loop for extracting sentiment
for x in range(0,len(data)):
    sent_int = SentimentIntensityAnalyzer()  #initializing the class
    try:
        text = data['title'][x]
        sent = sent_int.polarity_scores(text)  #this gives a dictionary contaning pos, neg and compound scores
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0

    title_neg_sentiment.append(neg)
    title_pos_sentiment.append(pos)
    title_neu_sentiment.append(neu)
    
#converting into pandas series and adding as a new column
data['title_negative_sentiment'] = pd.Series(title_neg_sentiment)
data['title_positive_sentiment'] = pd.Series(title_pos_sentiment)
data['title_neutral_sentiment'] = pd.Series(title_neu_sentiment)
    
    
#writing the final data to xlsx file
data.to_excel('articles_clean.xlsx', sheet_name='articles data', index = False)
