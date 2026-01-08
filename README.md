# 🎌 Anime Recommender System

A simple, user-friendly anime recommendation app, especially for users who don’t know what to watch next.

---

# Project Overview

Finding a new anime to watch can be overwhelming due to the huge number of choices available. This project solves that problem by:

* Allowing users to **search anime easily**
* Letting users **save their favourite anime**
* Generating **recommendations based on selected anime**
* Keeping favourites **persistent per user** using a database

The system is designed to be **simple**, **lightweight**, and **easy to extend**.

---

# Recommendation Logic

The recommender works using a **content-based approach**:

1. The user selects an anime they like
2. The system compares this anime with others based on:

   * Genre
   * Studio
   * Rating
   * Year
   * Description similarity
3. Anime with the **most similar attributes** are recommended

This approach works well because:

* It does not require large user data
* Recommendations are immediate
* Results feel relevant to the user’s taste

---

# Why This Project Is Useful

* Helps users **discover new anime quickly**
* No need to browse hundreds of titles
* Saves favourites for later viewing
* Clean and minimal UI
* Works for both beginners and regular anime watchers

This project reduces the effort of *“searching endlessly”* and turns it into *“click, discover, watch”*.

---

# Features

* User Login & Signup
* Search anime by name
* Get recommendations
* Add / Remove favourites
* Persistent storage using SQLite
* Scrollable recommendation table

---

# Tech Stack

* Python
* Streamlit (UI)
* Pandas & NumPy (data handling)
* SQLite (persistent database)

---

# Future Enhancements

This project is intentionally simple, but it is designed to scale. 
Possible future upgrades include:

# New Releases Library

* Automatic fetching of newly released anime
* Separate section for trending & seasonal anime

# Watch Links Integration

* Add links to hosted/streaming platforms
* Redirect users directly to where the anime is available

# Smarter Recommendations

* Collaborative filtering (users with similar tastes)
* Recommendation based on favourites history
* Popularity-based fallback

---

# Conclusion

This Anime Recommender System shows how **simple logic + clean design** can solve a real-world problem. It is beginner-friendly, practical, and demonstrates core concepts of:

* Recommender systems
* User personalization
* Database-backed applications
--------------------------------------------------------------------------------------------------------
