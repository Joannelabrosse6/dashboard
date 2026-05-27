import pandas as pd
import requests
import mysql.connector
from mysql.connector import Error

# ==========================================
# CONFIGURATION
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Mot de passe MySQL
    'database': 'vod_analysis'
}

# ==========================================
# FONCTIONS
# ==========================================
def fetch_tvmaze_data(show_title):
    """
    Appelle l'API publique TVMaze pour récupérer les informations d'une série.
    Retourne la note globale (rating) et la liste des genres.
    """
    url = f"https://api.tvmaze.com/singlesearch/shows?q={show_title}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rating = data.get('rating', {}).get('average', None)
            genres = data.get('genres', [])
            return rating, genres
    except Exception as e:
        print(f"Erreur API pour {show_title}: {e}")
    return None, []

def calculate_marketing_score(internal_score, global_rating):
    """
    Algorithme Marketing : Calcul d'un score de segmentation.
    Pondération : 60% score interne (plateforme), 40% rating global (API).
    Permet de classer les séries pour des campagnes publicitaires.
    """
    if pd.isna(global_rating) or global_rating is None:
        # Si pas de note API, on se base uniquement sur le score interne
        return round(internal_score, 2)
    
    # Le global_rating de TVMaze est sur 10, on le ramène sur 100 pour l'échelle
    normalized_global = global_rating * 10
    marketing_score = (internal_score * 0.6) + (normalized_global * 0.4)
    return round(marketing_score, 2)

# ==========================================
# PIPELINE PRINCIPAL
# ==========================================
def main():
    print("--- Démarrage du Pipeline Python ---")
    
    # 1. Lecture des données avec Pandas
    print("1. Lecture du fichier CSV...")
    try:
        df = pd.read_csv("tv_shows.csv")
    except FileNotFoundError:
        print("Erreur : le fichier tv_shows.csv est introuvable.")
        return
        
    df['global_rating'] = None
    df['marketing_score'] = None
    df['genres'] = None
    
    # 2. Enrichissement via l'API TVMaze
    print("2. Appel à l'API TVMaze pour enrichissement...")
    for index, row in df.iterrows():
        title = row['title']
        rating, genres = fetch_tvmaze_data(title)
        
        df.at[index, 'global_rating'] = rating
        df.at[index, 'genres'] = genres
        
        # 3. Application de l'Algorithme Marketing
        score = calculate_marketing_score(row['internal_popularity_score'], rating)
        df.at[index, 'marketing_score'] = score
        
    print("\nAperçu des données enrichies :")
    print(df[['title', 'global_rating', 'marketing_score']].head())
    
    # 4. Insertion dans MySQL
    print("\n3. Connexion et insertion dans MySQL...")
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            
            for _, row in df.iterrows():
                # On utilise marketing_score comme internal_score mis à jour pour la BDD
                insert_movie_query = """
                INSERT INTO movies (title, release_year, platform, internal_score, global_rating)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                internal_score = VALUES(internal_score), global_rating = VALUES(global_rating);
                """
                cursor.execute(insert_movie_query, (
                    row['title'], 
                    row['release_year'], 
                    row['platform'], 
                    float(row['marketing_score']), 
                    float(row['global_rating']) if row['global_rating'] else None
                ))
                
                # Récupération de l'ID du film
                cursor.execute("SELECT id FROM movies WHERE title = %s", (row['title'],))
                movie_id = cursor.fetchone()[0]
                
                # Insertion des genres
                if row['genres']:
                    for genre_name in row['genres']:
                        cursor.execute("""
                            INSERT INTO genres (name) VALUES (%s)
                            ON DUPLICATE KEY UPDATE name=name
                        """, (genre_name,))
                        
                        cursor.execute("SELECT id FROM genres WHERE name = %s", (genre_name,))
                        genre_id = cursor.fetchone()[0]
                        
                        # Insertion relation
                        cursor.execute("""
                            INSERT IGNORE INTO movie_genres (movie_id, genre_id)
                            VALUES (%s, %s)
                        """, (movie_id, genre_id))
            
            connection.commit()
            print("[OK] Succes : Les donnees enrichies ont ete inserees dans MySQL !")
            
    except Error as e:
        print(f"[ERREUR] Erreur lors de la connexion a MySQL: {e}")
        print("Verifiez que MySQL tourne, que la BDD 'vod_analysis' est creee, et que le mot de passe est correct.")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
