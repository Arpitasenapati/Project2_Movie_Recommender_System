
"""
Created on Tue Mar  5 23:23:45 2024

@author: arpit
"""

# app.py
import streamlit as st
import pickle
import pandas as pd
import requests

import time

def fetch_pos(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=d6171853dae04e4909e49d8f7c6fbc51".format(id)

    max_retries = 3
    current_retry = 0

    while current_retry < max_retries:
        try:
            data = requests.get(url)
            data.raise_for_status()  # Raise an HTTPError for bad responses
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            current_retry += 1
            time.sleep(3)  # Wait for 1 second before retrying

    print("Max retries reached. Unable to fetch data.")
    return None

def recommend(movie):
     movie_index=movies[movies['title']==movie].index[0]
     distances=similarity[movie_index]
     movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
     recommended_movies=[]
     recommended_pos=[]
     for i in movies_list[1:6]:
       id=movies.iloc[i[0]].id
       recommended_movies.append(movies.iloc[i[0]].title)
       recommended_pos.append(fetch_pos(id))
     return recommended_movies,recommended_pos
movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('MOVIE RECOMMENDER SYSTEM')
option=st.selectbox(
    "Type or select a movie from dropdown",
    movies['title'].values
)
if st.button('Recommend'):
    recommended_movies, recommended_pos = recommend(option)

    col1 , col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(recommended_movies[0])
        st.image(recommended_pos[0])
    with col2:
        st.header(recommended_movies[1])
        st.image(recommended_pos[1])
    with col3:
        st.header(recommended_movies[2])
        st.image(recommended_pos[2])
    with col4:
        st.header(recommended_movies[3])
        st.image(recommended_pos[3])
    
