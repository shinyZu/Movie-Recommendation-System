import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import webbrowser
# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     with app.app_context():
#         # Get the current URL
#         # current_url = request.url
#         # print(current_url)
#         # Open the current URL in the system's default browser
#         # webbrowser.open(current_url)
#     return "Hello, World!"


with open( "assets/css/main.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Load the HTML file as a string
def load_html_file(file_path):
    with open(file_path, 'r') as f:
        page_html = f.read()
    return page_html

# Load the Profile CSS file as a string
with open('assets/css/profile.css', 'r') as f:
    profile_css = f'<style>{f.read()}</style>'

# Load the Profile JS file as a string
with open('assets/js/profile.js', 'r') as f:
    profile_js = f'<style>{f.read()}</style>'

# Load the JS code from file
# with open('assets/js/profile.js', 'r') as f:
#     profile_js_code = f.read()

# Hide the iframe
iframe_css = """
    <style>
        iframe {
            display: none;
        }
    </style>
"""
st.markdown(iframe_css, unsafe_allow_html=True)

login_page_url = "http://127.0.0.1:5000/"
main_app_url = "http://localhost:8501/"


st.title('Discover your next favorite movie...!')
st.title("")

movies_dict = pickle.load(open('pickle/movie_dict.pkl', 'rb')) # rb = read binary mode
movies =pd.DataFrame(movies_dict)
similarity = pickle.load(open('pickle/similarity.pkl', 'rb'))

movie_selected = st.selectbox('Get your personalized movie recommendations in seconds...', movies['title'].values)

API_KEY = "c3ed154bde1307169e62092fa886bb9c"
poster_path_base_url = "https://image.tmdb.org/t/p/original"


def get_movie_poster(movie_id):
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c3ed154bde1307169e62092fa886bb9c&language=en-US'.format(movie_id))
        data = response.json()
        # print(data)
        # st.text(data)
        poster_url = poster_path_base_url + data['poster_path']
        # st.text(poster_url)
        return poster_url


def recommend_movies(movie_selected):
    movie_index = movies[movies['title'] == movie_selected].index[0]
    # st.text(movie_index)
    distances = similarity[movie_index]
    # st.text(distances)
    movies_list = sorted(list(enumerate(distances)), reverse = True, key=lambda x:x[1])[1:21]
    # st.text(movies_list)

    recommended_movies_list = []
    recommended_movies_poster_list = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # st.text(movie_id)
        recommended_movies_list.append(movies.iloc[i[0]].title)
        # st.text(recommended_movies_list)

        # fetch poster from API
        recommended_movies_poster_list.append(get_movie_poster(movie_id))
        # st.text(len(recommended_movies_list))
    return recommended_movies_list, recommended_movies_poster_list

def main():
    if st.button('Recommend'):
        titles,posters = recommend_movies(movie_selected)
        st.header('\n')
        st.header('\n')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(posters[0])
            st.caption(titles[0])

        with col2:
            st.image(posters[1])
            st.caption(titles[1])

        with col3:
            st.image(posters[2])
            st.caption(titles[2])

        st.header('\n')
        # st.header('\n')

        col4, col5, col6 = st.columns(3)

        with col4:
            st.image(posters[3])
            st.caption(titles[3])

        with col5:
            st.image(posters[4])
            st.caption(titles[4])

        with col6:
            st.image(posters[5])
            st.caption(titles[5])

        st.header('\n')

        col7, col8, col9 = st.columns(3)

        with col7:
            st.image(posters[6])
            st.caption(titles[6])

        with col8:
            st.image(posters[7])
            st.caption(titles[7])

        with col9:
            st.image(posters[8])
            st.caption(titles[8])


    else :
        titles,posters = recommend_movies("Avatar")
        st.header('\n')
        st.header('\n')

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(posters[0])
            st.caption(titles[0])

        with col2:
            st.image(posters[1])
            st.caption(titles[1])

        with col3:
            st.image(posters[2])
            st.caption(titles[2])

        st.header('\n')
        # st.header('\n')

        col4, col5, col6 = st.columns(3)

        with col4:
            st.image(posters[3])
            st.caption(titles[3])

        with col5:
            st.image(posters[4])
            st.caption(titles[4])

        with col6:
            st.image(posters[5])
            st.caption(titles[5])

        st.header('\n')

        col7, col8, col9 = st.columns(3)

        with col7:
            st.image(posters[6])
            st.caption(titles[6])

        with col8:
            st.image(posters[7])
            st.caption(titles[7])

        with col9:
            st.image(posters[8])
            st.caption(titles[8])

# Add buttons to the sidebar
sidebar_selection = st.sidebar.radio("Navigate to", ('Home', 'Profile'))

# Add a Logout button to the sidebar and redirect to login page
if st.sidebar.button('Logout'):
    # st.markdown('<a target="_self" href="http://127.0.0.1:5500/">sas</a>', unsafe_allow_html=True)
    webbrowser.open(login_page_url, new=2)

# Handle button clicks
if sidebar_selection == 'Profile':
    # Redirect to an HTML page when the user clicks the button
    #  webbrowser.open('http://127.0.0.1:5000/profile.html')
    #  webbrowser.open('profile.html')
    # render_template('http://127.0.0.1:8501/profile.html')

    st.markdown(load_html_file('profile.html'), unsafe_allow_html=True)

elif sidebar_selection == 'Home':
    main()

# else:
#     webbrowser.o

# if __name__ == "__main__":
#    app.run(debug=True)