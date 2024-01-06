import os
import json
import openpyxl
import requests
import pandas as pd
import urllib
import flask

def get_netflix_report():
    report_url = "https://assets.ctfassets.net/4cd45et68cgf/1HyknFM84ISQpeua6TjM7A/97a0a393098937a8f29c9d29c48dbfa8/What_We_Watched_A_Netflix_Engagement_Report_2023Jan-Jun.xlsx"
    response = requests.get(report_url) #download file
    if response.status_code == 200:
        cwd = os.getcwd()
        files = [x for x in os.listdir(cwd) if x.endswith('.xlsx')]
    assert files, 'there is no xlsx file here'
    return files

def generate_df(files):
    df = pd.read_excel(files[0]) # turn file into df
    df.drop([0,1,2,3], axis=0, inplace=True) # clean df removing unused rows and columns
    df.drop(df.columns[0], axis=1, inplace=True)
    teste = df.head(10) # taking only first 10s
    teste = df.index('Season')
    return df    

def search_movie(df):
    clean_movie_titles = []
    teste_dict = []
    movies_titles = list(df['Title'])
    test = df.head(10) # select only the first 10 movie titles, just to test
    movie_name_parsed = []
    movie_name_parsed = urllib.parse.quote_plus('The Night Agent') # to use in url for request
    for i in movies_titles:
          if 'Season' in i:
              position = i.index('Season')
              clean_movie_titles.append(i[0:position-2])
    for i in clean_movie_titles:
         movie_name_parsed = urllib.parse.quote_plus(i)
         url = "https://www.omdbapi.com/?t={}".format(movie_name_parsed)+"&apikey=de188342"
         response = requests.get(url)
         teste_dict[i]=response.json()
    return None

if __name__ == "__main__":
    movie_name = input("Enter the movie name: ")
    story_info = search_movie(movie_name)
    if story_info is not None:
        print("The story plot for the given movie '{}' is: {}".format(movie_name, story_info))
    else:
        print("Story plot not found for the movie '{}'".format(movie_name))