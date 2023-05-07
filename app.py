import streamlit as st
import time
import pickle
import pandas as pd
import requests
import streamlit.components.v1 as components

# # Define the function to redirect to a new page
# def redirect_to_page(page_url):
#     js = f"window.location.href = '{page_url}'"
#     html = "<script>{}</script>".format(js)
#     return html

# # Define the settings page
# def settings():
#     st.title("Settings Page")
#     st.write("This is the settings page.")

# def load_html_file(file_path):
#     with open(file_path, 'r') as f:
#         page_html = f.read()
#     return page_html

# if st.button('Settings', key='btnSettings'):
#     st.markdown(load_html_file('profile.html'), unsafe_allow_html=True)

# Hide the iframe
iframe_css = """
<style>
iframe {
    display: none;
}
</style>
"""
st.markdown(iframe_css, unsafe_allow_html=True)

def load_html_file(file_path):
    with open(file_path, 'r') as f:
        page_html = f.read()
    return page_html

# Add buttons to the sidebar
sidebar_selection = st.sidebar.radio("Navigate to", ('Home', 'Profile'))

# Handle button clicks
if sidebar_selection == 'Profile':
    st.markdown(load_html_file('profile.html'), unsafe_allow_html=True)
elif sidebar_selection == 'Home':
    components.html('<meta content="URL=http://localhost:8502/">')



movies_dict = pickle.load(open('movie_dict.pkl', 'rb')) # rb = read binary mode
movies =pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Discover your next favorite movie...!')

movie_selected = st.selectbox('Get your personalized movie recommendations in seconds...', movies['title'].values)

API_KEY = "c3ed154bde1307169e62092fa886bb9c"
poster_path_base_url = "https://image.tmdb.org/t/p/original"

def get_movie_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c3ed154bde1307169e62092fa886bb9c&language=en-US'.format(movie_id))
    data = response.json()
    poster_url = poster_path_base_url + data['poster_path']
    return poster_url


def recommend_movies(movie_selected):
    movie_index = movies[movies['title'] == movie_selected].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x:x[1])[1:11]

    recommended_movies_list = []
    recommended_movies_poster_list = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_list.append(movies.iloc[i[0]].title)

        # fetch poster from API
        recommended_movies_poster_list.append(get_movie_poster(movie_id))
    return recommended_movies_list, recommended_movies_poster_list


# Define the main app page
def main():

    if st.button('Recommend', key='btnRecommend'):
        titles, posters = recommend_movies(movie_selected)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.text(titles[0])
            st.image(posters[0])

        with col2:
            st.text(titles[1])
            st.image(posters[1])

        with col3:
            st.text(titles[2])
            st.image(posters[2])

        col4, col5, col6 = st.columns(3)

        with col4:
            st.text(titles[3])
            st.image(posters[3])

        with col5:
            st.text(titles[4])
            st.image(posters[4])

        with col6:
            st.text(titles[5])
            st.image(posters[5])