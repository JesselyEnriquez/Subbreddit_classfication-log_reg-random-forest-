

# general data analysis functions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
import pandas as pd
import requests
from datetime import datetime
import time
import random
import numpy as np
import re






########################## subreddit selftext & title extractor ##########################

# function to gather data from api and export a df
def get_df(subreddit):
    '''
    inputs:
    subreddit = 'subreddit name'

    This is a very customized function to gather the title and selftext from subreddits
    in reddit pushshift api.
    '''
    base_url =  'https://api.pushshift.io/reddit/search/submission?subreddit='

    #call function here
    url = base_url+subreddit

    # in second
    params = {'subreddit':subreddit, 'size':100 }

    cnt=0
    for i in range(1,30):
        res = requests.get(url,params)
        if res.status_code ==200:
            data = res.json()
            # getting the last date
            date = data['data'][-1]['created_utc']
            posts = data['data']
            # goes to the last post and gets the date stamp
            date = posts[-1]['created_utc']
            #print(date)
            # will update last date in each loop
            params['before'] = date
            # posts will update in each iteration
            if cnt==0:
                df=pd.DataFrame(posts)
                print(df.shape)
                cnt+=1
            df = df.append(pd.DataFrame(posts),ignore_index=True)
            #print(df.shape)
            sleep_duration = random.randint(2,6)
            #print(sleep_duration)
            time.sleep(sleep_duration)
            #print(df['title'])
        else:
            print('status code error')
            break
    df.drop_duplicates(subset=['title'],keep='first',inplace=True)
    print(df.shape)
    return df

####################################### preprocessing function ##########################
# to pass in a series using apply functions
def pre_process(sentences):
        '''
        inputs:
        sentences = text

        description:
        The function is utilized to remove emoticons, urls (https,eee,etc), special characters,
        and new line break stings('\n'). (Does NOT remove spaces).

        use cases:
        This was specifically created to pass in use df['new_column']=df['text_column'].apply(pre_preprocess)
        OR individual strings.
        '''
    # removing emoticons
    sentences = re.sub(':d', '', str(sentences)).strip()
    sentences = re.sub(':p', '', str(sentences)).strip()

    # removing urls
    sentences = re.sub('(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*','  ', sentences)

    # removing special characters (https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string)
    sentences = re.sub('[^A-Za-z0-9]+', ' ', str(sentences))

    sentences = re.sub('[^a-zA-Z\s]', '', str(sentences)).rstrip()

    # removing the '\n' new line breaks in sentences
    sentences = sentences.replace('\n',' ')

    return sentences
########################## word counter functions ##########################
def word_counter(paragraph):
    '''
    inputs:
    paragraph = group of text

    description:
    The function is utilized to count the words in a string.

    use cases:
    This was specifically created to pass in use df['new_column']=df['text_column'].apply(Lcase_counter)
    OR individual strings. Will temporarily strip out punctuation to get an accurate word count.
    '''
    # removing special characters (https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string)
    paragraph =     re.sub('[^A-Za-z0-9]+', '', str(paragraph))
    status_length = []
    for element in paragraph:
        if type(element) == str:
            #print(element)
            status_length.append(len(element))
    return len(status_length)

########################## case counter functions ##########################
def Lcase_counter(string):
    '''
    inputs:
    string = text

    description:
    The function is utilized to count the number of lower case letters in a string.

    use cases:
    This was specifically created to pass in use df['new_column']=df['text_column'].apply(Lcase_counter)
    OR individual strings.
    '''
    letter_list= []
    for charac in string:
        if charac.islower():
            letter_list.append(charac)
        else:
            pass
    return len(letter_list)

def Ucase_counter(string):
    '''
    inputs:
        string = text

    description:
    The function is utilized to count the number of upper case letters in a string.


    use cases:
        This was specifically created to pass in use df['new_column']=df['text_column'].apply(Ucase_counter)
        OR individual strings.
    '''
    letter_list= []
    for charac in string:
        if charac.isupper():
            letter_list.append(charac)
        else:
            pass
    return len(letter_list)



########################## punctuation character counter function ##########################
def punctuation_cntr(string):
    '''
    inputs:
    string = text

    description:
    The function is utilized to count the punctuation characters in a string.

    use cases:
    This was specifically created to pass in use df['new_column']=df['text_column'].apply(punctuation_cntr)
    OR individual strings.
    '''
    punctuations = ''' !()-[{]}};:'"\,<>./?@#$%^&*_~ '''
    count=0
    for charac in string:
        if charac in punctuations:
            count+=1
        else:
            pass
    return count
