import pandas as pd

# Load data
movies_info_df = pd.read_csv('./data/title.basics.tsv', sep='\t', dtype=str)
movies_rating_df = pd.read_csv('./data/title.ratings.tsv', sep='\t', dtype=str)

# Combine dataframes
full_movie_info_df = pd.merge(movies_info_df, movies_rating_df, on='tconst', how='left')
full_movie_info_df['genres'] = full_movie_info_df['genres'].str.replace(',', ';')

# Convert numeric columns
full_movie_info_df['averageRating'] = pd.to_numeric(full_movie_info_df['averageRating'], errors='coerce')
full_movie_info_df['numVotes'] = pd.to_numeric(full_movie_info_df['numVotes'], errors='coerce')

# Filter type for movies only
movies_only_df = full_movie_info_df[full_movie_info_df['titleType'] == 'movie'].copy()

#minimum vote requirement
min_votes = 40000
qualified_movies = movies_only_df[movies_only_df['numVotes'] >= min_votes]

# Sort and get top 250
top_250_movies = qualified_movies.sort_values(
    by=['averageRating', 'numVotes'], 
    ascending=[False, False]
).head(250)

# Before genre split
top_250_movies.to_csv('top_250_movies.csv', index=False)

# If you need genre-split version for analysis:
top_250_split_genres = top_250_movies.copy()
top_250_split_genres['genres'] = top_250_split_genres['genres'].str.split(';')
top_250_split_genres = top_250_split_genres.explode('genres')
top_250_split_genres.to_csv('top_250_movies_split_genres.csv', index=False)

print(top_250_movies.head())