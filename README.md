# 🎌 Anime Recommender System

A simple, user-friendly **Streamlit-based Anime Recommendation App** that helps users discover what to watch next using content-based filtering and live anime metadata from the **Jikan API (MyAnimeList)**.

---

## 📌 Project Overview

Finding a new anime to watch can be overwhelming due to the massive number of available titles. This project solves that problem by:

* Allowing users to search anime easily
* Letting users save their favourite anime
* Generating recommendations based on selected anime
* Persisting user data and favourites using a local database

The system is intentionally lightweight, beginner-friendly, and easy to extend.

---

## 🧠 Recommendation Logic

The recommender uses a **content-based filtering approach**.

### How it works:

1. The user selects an anime they like
2. The system compares it with other anime based on:

   * Genre
   * Studio
   * Rating
   * Release year
   * Description similarity (TF-IDF)
3. Anime with the highest similarity scores are recommended

### Why this approach works:

* No large user dataset required
* Instant recommendations
* Results feel relevant to the user’s taste

---

## ✨ Features

* User Login & Signup
* Search anime by name
* Content-based recommendations
* Add / Remove favourites
* Persistent storage using SQLite
* Scrollable recommendations table
* Live anime metadata via Jikan API
* Cached API responses to avoid rate limits

---

## 🛠 Tech Stack

* **Python**
* **Streamlit** (UI)
* **Pandas & NumPy** (data handling)
* **Scikit-learn (TF-IDF)** (similarity)
* **SQLite** (persistent database)
* **Jikan API** (MyAnimeList data)
* **requests-cache** (API caching)

---

## ⚙️ Setup Instructions

### 1. Create & activate a virtual environment (recommended)

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure environment variables

Copy the example file:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

#### Important environment variables:

* `DB_NAME` — SQLite database file (default: `anime_app.db`)
* `JIKAN_BASE_URL` — Jikan API base URL
  (default: `https://api.jikan.moe/v4/anime/`)
* `JIKAN_CACHE_TTL` — Cache duration in seconds
  (default: `86400` / 24 hours)

> ⚠️ Keep `.env` out of source control — it is ignored via `.gitignore`.

---

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📝 Notes

* The app uses **`requests-cache`** to cache Jikan API responses and reduce rate-limit issues
* User accounts and favourites are stored locally using SQLite
* The architecture allows easy replacement with a remote backend later

---

## 🚀 Future Enhancements

This project is designed to scale. Possible upgrades include:

### 🔥 New Releases Library

* Automatic fetching of newly released anime
* Trending & seasonal sections

### 🔗 Watch Links Integration

* Direct links to streaming platforms

### 🤖 Smarter Recommendations

* Popularity-based fallback
* Hybrid recommendation models

---

## ✅ Conclusion

The **Anime Recommender System** demonstrates how **simple logic + clean UI** can solve a real-world problem. It showcases core concepts of:

* Recommender systems
* User personalization
* API integration
* Database-backed applications

Perfect for beginners and practical enough for real use.
