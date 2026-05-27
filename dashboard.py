import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# --- CONNEXION BDD ---
def get_data():
    try:
        engine = create_engine("mysql+mysqlconnector://root:root@localhost/vod_analysis")
        query = """
        SELECT m.title, m.release_year, m.platform, m.internal_score, m.global_rating, g.name as genre
        FROM movies m
        LEFT JOIN movie_genres mg ON m.id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        """
        df = pd.read_sql(query, engine)
        df['global_rating'] = df['global_rating'].fillna(df['internal_score'] / 10)
        return df
    except Exception as e:
        print(f"Erreur connexion BDD : {e}")
        return pd.DataFrame({
            'title': ['Breaking Bad', 'The 100', 'Sherlock', 'Stranger Things'],
            'genre': ['Drama', 'Sci-Fi', 'Crime', 'Sci-Fi'],
            'release_year': [2008, 2014, 2010, 2016],
            'platform': ['Netflix', 'CW', 'BBC', 'Netflix'],
            'internal_score': [95, 80, 92, 88],
            'global_rating': [9.5, 7.6, 9.1, 8.7]
        })

df = get_data()

# --- DASH APP ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Dashboard VOD Analysis (Dash & Plotly)", className="text-center my-4", style={'color': '#2c3e50'}),
    
    # Filtre
    dbc.Row([
        dbc.Col([
            html.Label("Filtrer par Plateforme :"),
            dcc.Dropdown(
                id='platform-filter',
                options=[{'label': p, 'value': p} for p in df['platform'].unique() if p],
                value=df['platform'].unique().tolist(),
                multi=True,
                className="mb-4"
            )
        ], width=6)
    ], justify="center"),
    
    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Séries", className="card-title text-center"),
                html.H2(id="kpi-total-movies", className="text-center text-primary")
            ])
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Note Moyenne", className="card-title text-center"),
                html.H2(id="kpi-avg-rating", className="text-center text-success")
            ])
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Genres", className="card-title text-center"),
                html.H2(id="kpi-total-genres", className="text-center text-info")
            ])
        ]), width=4),
    ], className="mb-4"),
    
    # Graphiques
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-top-shows'), width=6),
        dbc.Col(dcc.Graph(id='pie-genres'), width=6),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter-year-rating'), width=12),
    ])
], fluid=True)

@app.callback(
    [Output('kpi-total-movies', 'children'),
     Output('kpi-avg-rating', 'children'),
     Output('kpi-total-genres', 'children'),
     Output('bar-top-shows', 'figure'),
     Output('pie-genres', 'figure'),
     Output('scatter-year-rating', 'figure')],
    [Input('platform-filter', 'value')]
)
def update_dashboard(selected_platforms):
    filtered_df = df[df['platform'].isin(selected_platforms)]
    
    if filtered_df.empty:
        return "0", "0.0", "0", {}, {}, {}

    # Calcul KPIs
    total_movies = filtered_df.drop_duplicates('title').shape[0]
    avg_rating = round(filtered_df.drop_duplicates('title')['global_rating'].mean(), 2)
    total_genres = filtered_df['genre'].nunique()

    # 1. Top 10 des séries par Global Rating
    top_shows = filtered_df.drop_duplicates('title').sort_values('global_rating', ascending=False).head(10)
    fig_bar = px.bar(top_shows, x='title', y='global_rating', title="Top 10 des séries par Note Globale", color='title')
    
    # 2. Répartition des genres
    genre_dist = filtered_df['genre'].value_counts().reset_index()
    genre_dist.columns = ['genre', 'count']
    fig_pie = px.pie(genre_dist, names='genre', values='count', title="Distribution des Genres")
    
    # 3. Note vs Année de sortie
    fig_scatter = px.scatter(filtered_df, x='release_year', y='global_rating', color='platform', hover_name='title', size='internal_score', title="Note Globale vs Année de sortie")
    
    return str(total_movies), str(avg_rating), str(total_genres), fig_bar, fig_pie, fig_scatter

if __name__ == '__main__':
    app.run(debug=True)
