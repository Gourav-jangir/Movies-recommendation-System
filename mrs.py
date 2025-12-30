import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommendation(movie , similarity):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    sorted_movies = sorted(list(enumerate(distances)),reverse = True , key = lambda x:x[1])[1:6]
    recommended = []
    movies_poster = []
    for i in sorted_movies:
        movie_id = movies_list['id'][i[0]]
        recommended.append(movies_list['title'][i[0]])
        movies_poster.append(fetch_poster(movie_id))
    return recommended, movies_poster

def filter_by_genre(genre):
    titles = []
    posters = []

    for index, row in filter_movies.iterrows():
        if genre in row['genres']:
            titles.append(row['title'])
            posters.append(fetch_poster(row['id']))

            if len(titles) == 5:  # show only first 5
                break

    return titles, posters


movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
filter_movies = pickle.load(open('movie_list.pkl', 'rb'))


st.title("Movies Recommendation System")

genres = ['Drama', 'Horror', 'TVMovie', 'Comedy', 'Fantasy', 'Animation', 'Foreign', 'Documentary', 'Family', 'Music', 'History', 'ScienceFiction', 'Mystery', 'Adventure', 'Crime', 'Western', 'War', 'Action', 'Romance', 'Thriller']
tab1, tab2 = st.tabs(["🎯 Recommendation", "🎬 Genre Filter"])
with tab1:
    options = st.selectbox("Search for a movie", movies_list['title'].values)


    if st.button('recommend', key='recommend_button'):
        names , posters = recommendation(options , similarity)
    
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            st.image(posters[0])

        with col2:
            st.text(names[1])
            st.image(posters[1])
    
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])

        with col5:
            st.text(names[4])
            st.image(posters[4])
with tab2:
    genres_options = st.selectbox("Select Genre", genres)
    if st.button('Filter' , key='filter_button'):
        titles, posters = filter_by_genre(genres_options)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(titles[0])
            st.image(posters[0])

        with col2:
            st.text(titles[1])
            st.image(posters[1])

        with col3:
            st.text(titles[2])
            st.image(posters[2])

        with col4:
            st.text(titles[3])
            st.image(posters[3])

        with col5:
            st.text(titles[4])
            st.image(posters[4])
