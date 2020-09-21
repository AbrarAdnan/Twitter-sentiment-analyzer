**Importing the libraries and keys**
"""

# Import the libraries
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
pd.set_option('display.max_colwidth',500)

log = pd.read_csv("Login.csv")
# Twitter Api Credentials
consumerKey = log["key"][0]
consumerSecret = log["key"][1]
accessToken = log["key"][2]
accessTokenSecret = log["key"][3]

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)

"""**Enter the name of the people to compare their tweets**"""

FirstPerson = "BillGates" 
SecondPerson = "realDonaldTrump"
tweetAmount = 200

# Extract 100 tweets from the first twitter user
FirstPosts = api.user_timeline(screen_name=FirstPerson, count = tweetAmount, lang ="en", tweet_mode="extended")

#  Print the last 5 tweets
print("Showing the 3 recent tweets from %s:\n"%FirstPerson)
i=1
for tweet in FirstPosts[:3]:
    print(str(i) +') '+ tweet.full_text + '\n')
    i= i+1

# Extract 100 tweets from the second twitter user
SecondPosts = api.user_timeline(screen_name=SecondPerson, count = tweetAmount, lang ="en", tweet_mode="extended")

#  Print the last 5 tweets
print("Showing the 3 recent tweets from %s:\n"%SecondPerson)
i=1
for tweet in SecondPosts[:3]:
    print(str(i) +') '+ tweet.full_text + '\n')
    i= i+1

# Create a dataframe with a column called Tweets for First Person
df1 = pd.DataFrame([tweet.full_text for tweet in FirstPosts], columns=['Tweets'])
# Show the first 5 rows of data
df1.head()

# Create a dataframe with a column called Tweets for Second Person
df2 = pd.DataFrame([tweet.full_text for tweet in SecondPosts], columns=['Tweets'])
# Show the first 5 rows of data
df2.head()

# Create a function to clean the tweets
def cleanTxt(text):
 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
 text = re.sub('#', '', text) # Removing '#' hash tag
 text = re.sub('RT[\s]+', '', text) # Removing RT
 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
 
 return text

# Clean the tweets
df1['Tweets'] = df1['Tweets'].apply(cleanTxt)

# Show the cleaned tweets
df1

# Clean the tweets
df2['Tweets'] = df2['Tweets'].apply(cleanTxt)

# Show the cleaned tweets
df2

# Create a function to get the subjectivity
def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
   return  TextBlob(text).sentiment.polarity

# Create two new columns 'Subjectivity' & 'Polarity'
df1['Subjectivity'] = df1['Tweets'].apply(getSubjectivity)
df1['Polarity'] = df1['Tweets'].apply(getPolarity)

# Show the new dataframe with columns 'Subjectivity' & 'Polarity'
df1

# Create two new columns 'Subjectivity' & 'Polarity'
df2['Subjectivity'] = df2['Tweets'].apply(getSubjectivity)
df2['Polarity'] = df2['Tweets'].apply(getPolarity)

# Show the new dataframe with columns 'Subjectivity' & 'Polarity'
df2

# word cloud visualization of First Person
allWords = ' '.join([twts for twts in df1['Tweets']])
FirstPersonWordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)

plt.title('WordCloud of %s'%FirstPerson)
plt.imshow(FirstPersonWordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()


# word cloud visualization of Second Person
allWords = ' '.join([twts for twts in df2['Tweets']])
SecondPersonWordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)

plt.title('WordCloud of %s'%SecondPerson)
plt.imshow(SecondPersonWordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

df1['Analysis'] = df1['Polarity'].apply(getAnalysis)# Show the dataframe
df1

df2['Analysis'] = df2['Polarity'].apply(getAnalysis)# Show the dataframe
df2

# Printing positive tweets of first person
print('Printing positive tweets of %s:\n' %FirstPerson)
j=1
sortedDF1 = df1.sort_values(by=['Polarity']) #Sort the tweets
for i in range(0, sortedDF1.shape[0] ):
  if( sortedDF1['Analysis'][i] == 'Positive'):
    print(str(j) + ') '+ sortedDF1['Tweets'][i])
    print()
    j= j+1

# Printing positive tweets of second person
print('Printing positive tweets of %s:\n' %SecondPerson)
j=1
sortedDF2 = df2.sort_values(by=['Polarity']) #Sort the tweets
for i in range(0, sortedDF2.shape[0] ):
  if( sortedDF2['Analysis'][i] == 'Positive'):
    print(str(j) + ') '+ sortedDF2['Tweets'][i])
    print()
    j= j+1

# Printing negative tweets of first person
print('Printing negative tweets of %s:\n' %FirstPerson)
j=1
sortedDF1 = df1.sort_values(by=['Polarity'],ascending=False) #Sort the tweets
for i in range(0, sortedDF1.shape[0] ):
  if( sortedDF1['Analysis'][i] == 'Negative'):
    print(str(j) + ') '+sortedDF1['Tweets'][i])
    print()
    j=j+1
# Printing positive tweets of second person
print('Printing negative tweets of %s:\n' %SecondPerson)
j=1
sortedDF2 = df2.sort_values(by=['Polarity'],ascending=False) #Sort the tweets
for i in range(0, sortedDF2.shape[0] ):
  if( sortedDF2['Analysis'][i] == 'Negative'):
    print(str(j) + ') '+sortedDF2['Tweets'][i])
    print()
    j=j+1

# Plotting point of first person
plt.figure(figsize=(8,6)) 
for i in range(0, df1.shape[0]):
  plt.scatter(df1["Polarity"][i], df1["Subjectivity"][i], color='Blue') # plt.scatter(x,y,color)
for i in range(0, df2.shape[0]):
  plt.scatter(df2["Polarity"][i], df2["Subjectivity"][i], color='Red') # plt.scatter(x,y,color)
plt.title('Sentiment comparison of '+FirstPerson+' in Blue \n and '+SecondPerson+' in Red') 
plt.xlabel('Polarity') 
plt.ylabel('Subjectivity') 
plt.show()

# Print the percentage of positive tweets of first person
ptweets = df1[df1.Analysis == 'Positive']
ptweets = ptweets['Tweets']
ptweets

FirstPersonPositivity = round( (ptweets.shape[0] / df1.shape[0]) * 100 , 1)

# Print the percentage of positive tweets of second person
ptweets = df2[df2.Analysis == 'Positive']
ptweets = ptweets['Tweets']
ptweets

SecondPersonPositivity = round( (ptweets.shape[0] / df2.shape[0]) * 100 , 1)
print("Percentage of positive tweets of %s is "%FirstPerson , FirstPersonPositivity)
print("Percentage of positive tweets of %s is "%SecondPerson , SecondPersonPositivity)

# Print the percentage of negative tweets of first person
ptweets = df1[df1.Analysis == 'Negative']
ptweets = ptweets['Tweets']
ptweets

FirstPersonNegativity = round( (ptweets.shape[0] / df1.shape[0]) * 100 , 1)

# Print the percentage of positive tweets of second person
ptweets = df2[df2.Analysis == 'Negative']
ptweets = ptweets['Tweets']
ptweets

SecondPersonNegativity = round( (ptweets.shape[0] / df2.shape[0]) * 100 , 1)
print("Percentage of negative tweets of %s is "%FirstPerson , FirstPersonNegativity)
print("Percentage of negative tweets of %s is "%SecondPerson , SecondPersonNegativity)

# Show the value counts
print("Value count of "+FirstPerson)
df1['Analysis'].value_counts()

print("Value count of "+SecondPerson)
df2['Analysis'].value_counts()

# Plotting and visualizing the tweets of first person
plt.title('Sentiment Analysis of %s'%FirstPerson)
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df1['Analysis'].value_counts().plot(kind = 'bar')
plt.show()

# Plotting and visualizing the tweets of second person
plt.title('Sentiment Analysis of %s'%SecondPerson)
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df2['Analysis'].value_counts().plot(kind = 'bar')
plt.show()