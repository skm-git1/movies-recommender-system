import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bbe5c9e2a98ce833c6986e3a1eff57c8&language=en-US")
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, recommended_movies_posters

# Load the movie data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(    'Select a movie to get recommendations:',
    movies_list)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    st.write("Recommended Movies:")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:      
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])
