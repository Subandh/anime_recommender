import os
from dotenv import load_dotenv

import streamlit as st
import pandas as pd
import requests
import requests_cache

# Load environment variables from .env (if present)
load_dotenv()

# Cache Jikan responses; TTL configurable via JIKAN_CACHE_TTL (seconds)
cache_ttl = int(os.getenv("JIKAN_CACHE_TTL", "86400"))
requests_cache.install_cache("jikan_cache", expire_after=cache_ttl)

# Jikan base URL configurable via JIKAN_BASE_URL
JIKAN_BASE_URL = os.getenv("JIKAN_BASE_URL", "https://api.jikan.moe/v4/anime/")

from recommender import recommend_anime
from database import (
    init_db,
    create_user,
    login_user,
    add_favorite,
    get_favorites,
    remove_favorite 
)
from database import (
    create_password_reset_token,
    reset_password,
    get_security_question,
    reset_password_with_security_answer
)


st.set_page_config(page_title="Anime Recommender", layout="wide")
init_db()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

anime = pd.read_csv("anime_with_id.csv")

def fetch_jikan_anime(anime_id):
    """Fetch anime metadata from Jikan (returns dict or None)."""
    try:
        url = f"{JIKAN_BASE_URL.rstrip('/')}/{anime_id}"
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json().get("data", {})

        title = data.get("title") or data.get("title_english") or ""
        genres = ", ".join([g.get("name", "") for g in data.get("genres", [])])
        synopsis = data.get("synopsis") or ""
        studios = ", ".join([s.get("name", "") for s in data.get("studios", [])]) if data.get("studios") else ""
        year = data.get("year") or ""
        rating = data.get("rating") or ""

        return {
            "Anime": title,
            "Genre": genres,
            "Description": synopsis,
            "Studio": studios,
            "Year": year,
            "Rating": rating,
        }
    except Exception:
        return None

# LOGIN / SIGNUP

if st.session_state.user_id is None:
    st.title("🎌 Anime Recommendation System")
    st.subheader("Login or Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    sec_question = st.text_input("Security question (for password recovery)")
    sec_answer = st.text_input("Answer to security question", type="password")

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
            if create_user(username, password, security_question=sec_question, security_answer=sec_answer):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")

    # Password reset request / security-question flow
    st.markdown("---")
    st.subheader("Forgot Password?")
    reset_username = st.text_input("Username for password reset", key="reset_username")
    use_sec = st.checkbox("Use security question to reset password", key="use_sec")

    if use_sec:
        if reset_username:
            question = get_security_question(reset_username)
            if question:
                st.markdown(f"**Security question:** {question}")
                sec_ans_attempt = st.text_input("Your answer", type="password", key="sec_ans_attempt")
                new_pw2 = st.text_input("New password", type="password", key="new_pw2")
                if st.button("Reset using security question"):
                    if not sec_ans_attempt or not new_pw2:
                        st.error("Provide answer and new password")
                    else:
                        ok = reset_password_with_security_answer(reset_username, sec_ans_attempt, new_pw2)
                        if ok:
                            st.success("Password reset successful. Please login.")
                        else:
                            st.error("Incorrect answer or reset failed")
            else:
                st.error("No security question set for this user")
        else:
            st.error("Enter a username to use security question")
    else:
        if st.button("Request password reset token"):
            if reset_username:
                token = create_password_reset_token(reset_username)
                if token:
                    st.success("Password reset token created. In production this would be emailed to the user.")
                    st.info(f"Reset token: {token}")
                else:
                    st.error("Username not found")
            else:
                st.error("Enter a username")

        st.markdown("---")
        st.subheader("Reset Password (have a token?)")
        provided_token = st.text_input("Reset token", key="provided_token")
        new_pw = st.text_input("New password", type="password", key="new_pw")
        if st.button("Reset password using token"):
            if provided_token and new_pw:
                ok = reset_password(provided_token, new_pw)
                if ok:
                    st.success("Password reset successful. Please login.")
                else:
                    st.error("Invalid or expired token")
            else:
                st.error("Provide token and new password")

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

    api_details = None
    if selected_anime_id is not None:
        api_details = fetch_jikan_anime(selected_anime_id)

    if api_details:
        st.markdown(f"**Genre:** {api_details.get('Genre','')}")
        st.markdown(f"**Studio:** {api_details.get('Studio','')}")
        st.markdown(f"**Year:** {api_details.get('Year','')}")
        st.markdown(f"**Rating:** {api_details.get('Rating','')}")
        st.markdown("**Description:**")
        st.write(api_details.get('Description',''))
    else:
        details = anime[anime["Anime"] == anime_name].iloc[0]

        st.markdown(f"**Genre:** {details['Genre']}")
        st.markdown(f"**Studio:** {details['Studio']}")
        st.markdown(f"**Year:** {details['Year']}")
        st.markdown(f"**Rating:** {details['Rating']}")
        st.markdown("**Description:**")
        st.write(details["Description"])
