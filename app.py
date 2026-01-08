import streamlit as st
import pandas as pd

from recommender import recommend_anime
from database import (
    init_db,
    create_user,
    login_user,
    add_favorite,
    get_favorites,
    remove_favorite 
)


st.set_page_config(page_title="Anime Recommender", layout="wide")
init_db()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

anime = pd.read_csv("anime_with_id.csv")

# LOGIN / SIGNUP

if st.session_state.user_id is None:
    st.title("🎌 Anime Recommendation System")
    st.subheader("Login or Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            user_id = login_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        if st.button("Signup"):
            if create_user(username, password):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# MAIN APPLICATION
st.title("🎌 Anime Recommendation System")

if st.sidebar.button("Logout"):
    st.session_state.user_id = None
    st.rerun()

# SIDEBAR
st.sidebar.subheader("⭐ My Favorites")

favorites = get_favorites(st.session_state.user_id)

if not favorites:
    st.sidebar.write("No favorites yet, Start Binging Now!!")
else:
    fav_names = [name for _, name in favorites]

    selected_fav = st.sidebar.selectbox(
        "Your favourite anime:",
        fav_names
    )

    if st.sidebar.button("❌ Remove from favorites"):
        anime_id_to_remove = next(
            aid for aid, name in favorites if name == selected_fav
        )
        remove_favorite(st.session_state.user_id, anime_id_to_remove)
        st.sidebar.success("Removed from favorites")
        st.rerun()

# ANIME SELECTION
search_term = st.text_input("Type anime name (partial or full):")

if search_term:
    filtered_anime = anime[
        anime["Anime"].str.contains(search_term, case=False, na=False)
    ]
else:
    filtered_anime = anime

if filtered_anime.empty:
    st.warning("No anime found. Try another one!")
    anime_name = None
    selected_anime_id = None
else:
    anime_name = st.selectbox(
        "Pick an anime from the list:",
        filtered_anime["Anime"].values
    )

    selected_anime_id = anime.loc[
        anime["Anime"] == anime_name, "anime_id"
    ].values[0]


# ACTION BUTTONS
col1, col2 = st.columns(2)

with col1:
    if st.button("Recommend") and anime_name:
        recommendations = recommend_anime(anime_name)
        st.subheader("Recommended Anime")
        st.dataframe(recommendations, use_container_width=True)

with col2:
    if st.button("Add to Favorites") and anime_name:
        add_favorite(
            st.session_state.user_id,
            selected_anime_id,
            anime_name
        )
        st.success("Added to favorites!")
        st.rerun()

# ANIME DETAILS
if anime_name:
    st.subheader("Anime Details")
    details = anime[anime["Anime"] == anime_name].iloc[0]

    st.markdown(f"**Genre:** {details['Genre']}")
    st.markdown(f"**Studio:** {details['Studio']}")
    st.markdown(f"**Year:** {details['Year']}")
    st.markdown(f"**Rating:** {details['Rating']}")
    st.markdown("**Description:**")
    st.write(details["Description"])
