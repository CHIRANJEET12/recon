import pickle
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def recon(selected):
    index = mov_list[mov_list['Title']==selected].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    recon_mv=[]
    recon_mv_p=[]
    self_title = mov_list.iloc[index].Title
    self_poster = mov_list.iloc[index].Poster_Url
    for i in distance[1:6]:
        recon_mv.append(mov_list.iloc[i[0]].Title)
        recon_mv_p.append(mov_list.iloc[i[0]].Poster_Url)
    return self_title,self_poster,recon_mv,recon_mv_p

def movie_analysis_graphs(title):
    row = mov_list[mov_list['Title']==title].iloc[0]

    popularity = float(row.Popularity)
    vote_count = float(row.Vote_Count)

    avg_pop = mov_list['Popularity'].mean()
    avg_count = mov_list['Vote_Count'].mean()

    fig1, ax1 = plt.subplots(figsize=(5,4))
    ax1.bar(['Selected Movie', 'Average'], [popularity, avg_pop], color=['skyblue','orange'])
    ax1.set_ylabel('Popularity')
    ax1.set_title(f"{title} - Popularity vs Average")
    for i, v in enumerate([popularity, avg_pop]):
        ax1.text(i, v + 0.1, str(round(v,2)), ha='center', fontweight='bold')

    fig2, ax2 = plt.subplots(figsize=(5,4))
    ax2.bar(['Selected Movie', 'Average'], [vote_count, avg_count], color=['green','purple'])
    ax2.set_ylabel('Vote Count')
    ax2.set_title(f"{title} - Vote Count vs Average")
    for i, v in enumerate([vote_count, avg_count]):
        ax2.text(i, v + 0.1, str(round(v,2)), ha='center', fontweight='bold')

    return fig1, fig2



mov_list = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_titles = mov_list['Title'].values

st.header("Movie Recon Sys")
selected = st.selectbox(
   "Type or select a movie from the dropdown",
    movie_titles
)

if st.button("Show Recom"):
    self_title,self_poster,rec_mov,recon_mv_p = recon(selected)
    
    st.subheader("Movie Selected:")
    st.text(self_title)
    st.image(self_poster, width=250)
    
    st.subheader("Movie Stats Graphs:")
    fig1, fig2 = movie_analysis_graphs(self_title)
    st.pyplot(fig1)
    st.pyplot(fig2)

    st.subheader("Recommended Movies:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(rec_mov[0])
        st.image(recon_mv_p[0], width=150)
    with col2:
        st.text(rec_mov[1])
        st.image(recon_mv_p[1], width=150)
    with col3:
        st.text(rec_mov[2])
        st.image(recon_mv_p[2], width=150)
    with col4:
        st.text(rec_mov[3])
        st.image(recon_mv_p[3], width=150)
    with col5:
        st.text(rec_mov[4])
        st.image(recon_mv_p[4], width=150)
