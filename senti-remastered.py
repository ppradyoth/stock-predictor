#pip install snscrape
import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt


query="tesla"
tweets=[]
limit=2000


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets)==limit:
        break
    else:
        tweets.append(tweet.content)
        
#create a dataframe with column called tweets
df1=df=pd.DataFrame(tweets,columns=['tweet'])
print(df)


#function to clean the tweets
def cleanTxt(text):
    text=re.sub(r'@[A-Za-z0-9]+','',text)#remove s@mentions
    text=re.sub(r'#','',text) #removes #
    text=re.sub(r'RT[\s]+','',text) #removes RT
    text=re.sub(r'https?:\/\/\S+','',text) #removes hyperlinks
    return text
#cleaning the text
df['tweet']=df['tweet'].apply(cleanTxt)
print(df)


#function to get subjectivity and polarity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

#create two new columns related to subjectivity and polarity
df['Subjectivity']=df['tweet'].apply(getSubjectivity)
df['Polarity']=df['tweet'].apply(getPolarity)
print(df)

#function to compute positive,negative,neutral analysis
def getAnalysis(score):
    if score<0:
        return 'Negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'
df['Analysis']=df['Polarity'].apply(getAnalysis)
print(df)

#Print all the positive tweets
j=1
sortedDF=df.sort_values(by=['Polarity'])
for i in range(0,sortedDF.shape[0]):
    if (sortedDF['Analysis'][i]=='Positive'):
        print(str(j)+')'+sortedDF['tweet'][i])
        print()
        j=j+1


#print the negative tweets
j=1
sortedDF=df.sort_values(by=['Polarity'],ascending=False)
for i in range(0,sortedDF.shape[0]):
    if (sortedDF['Analysis'][i]=='Negative'):
        print(str(j)+')'+sortedDF['tweet'][i])
        print()
        j=j+1

#Plot the polarity and subjectivity
plt.figure(figsize=(8,6))
for i in range(0,df.shape[0]):
    plt.scatter(df['Polarity'][i],df['Subjectivity'][i],color='Blue')
plt.title("Sentiment Analysis")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity")
plt.show()


#Get the percentage of positive tweets
ptweets=df[df.Analysis=='Positive']
ptweets=ptweets['tweet']
pos=round((ptweets.shape[0]/df.shape[0]*100),11)
print(pos)


#Get the percentage of NEGATIVE tweets
ptweets=df[df.Analysis=='Negative']
ptweets=ptweets['tweet']
neg=round((ptweets.shape[0]/df.shape[0]*100),11)
print(neg)


#Get the percentage of neutral tweets
ptweets=df[df.Analysis=='Neutral']
ptweets=ptweets['tweet']
neu=round((ptweets.shape[0]/df.shape[0]*100),11)
print(neu)


#show the value count
df['Analysis'].value_counts()

#plot and visualize the count
plt.title("Sentiment Analysis")
plt.xlabel('Sentiment')
plt.ylabel('Count')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()



if(neu<pos or (neu>pos and pos<neg) ):
    print("Dont buy the stock!!")
    print("Here are some negative tweets about the stock that may help you consider not to buy!!")
    j=1
    sortedDF=df.sort_values(by=['Polarity'],ascending=False)
    for i in range(0,sortedDF.shape[0]):
        if (sortedDF['Analysis'][i]=='Negative') and j<=10:
            print(str(j)+')'+df1['tweet'][i])
            j+=1

elif(neu>pos and pos>neg):
    print("Buy the stock!!")
    print("Here are some positive tweets about the stock that may help you  consider buying!!")
    j=1
    sortedDF=df.sort_values(by=['Polarity'])
    
    for i in range(0,sortedDF.shape[0]):
        if (sortedDF['Analysis'][i]=='Positive') and j<=10:
            print(str(j)+')'+df1['tweet'][i])
            j+=1

    
#elif(neu>pos and pos<neg):
    #print("Dont buy the stock!!")


