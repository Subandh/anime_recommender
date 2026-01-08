import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

anime = pd.read_csv("anime_with_id.csv")

anime['content'] = (
    anime['Genre'].fillna('') + ' ' +
    anime['Description'].fillna('')
)

tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=5000
)

tfidf_matrix = tfidf.fit_transform(anime['content'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

anime_index = pd.Series(anime.index, index=anime['Anime']).drop_duplicates()

def recommend_anime(anime_name, top_n=5):
    """
    Returns top_n anime similar to the given anime_name
    """

    if anime_name not in anime_index:
        return pd.DataFrame(columns=['Anime', 'Genre', 'Similarity Score'])

    idx = anime_index[anime_name]

    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_matches = similarity_scores[1:top_n + 1]

    recommendations = []
    for i, score in top_matches:
        recommendations.append({
            'Anime': anime.iloc[i]['Anime'],
            'Genre': anime.iloc[i]['Genre'],
            'Similarity Score': round(score, 3)
        })

    return pd.DataFrame(recommendations)
