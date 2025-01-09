import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import pandas as pd

# Configuración inicial de la API de Spotify
SPOTIFY_CLIENT_ID = "tu_client_id"
SPOTIFY_CLIENT_SECRET = "tu_client_secret"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Función para obtener canciones basadas en estado de ánimo y rango de años
def get_songs_by_mood(mood, start_year, end_year):
    # Diccionario de estados de ánimo con palabras clave para búsqueda
    mood_keywords = {
        "Viaje en auto energizante": "road trip upbeat",
        "Relax en casa": "chill acoustic",
        "Fiesta nocturna": "party dance",
        "Inspirador y motivacional": "inspirational pop",
    }

    if mood not in mood_keywords:
        return []

    query = f"{mood_keywords[mood]} year:{start_year}-{end_year}"
    results = sp.search(q=query, type="track", limit=20)

    songs = []
    for item in results['tracks']['items']:
        song = {
            "name": item['name'],
            "artist": item['artists'][0]['name'],
            "url": item['external_urls']['spotify']
        }
        songs.append(song)

    return songs

# Configuración de la app en Streamlit
st.title("Generador de Playlist por Estado de Ánimo")

st.sidebar.header("Elige tu estado de ánimo")
mood = st.sidebar.selectbox(
    "Selecciona un mood:",
    ["Viaje en auto energizante", "Relax en casa", "Fiesta nocturna", "Inspirador y motivacional"]
)

st.sidebar.header("Selecciona el rango de años")
start_year = st.sidebar.slider("Año de inicio", min_value=1950, max_value=2025, value=2000)
end_year = st.sidebar.slider("Año de fin", min_value=1950, max_value=2025, value=2025)

# Obtener canciones
if st.sidebar.button("Generar Playlist"):
    with st.spinner("Buscando canciones..."):
        songs = get_songs_by_mood(mood, start_year, end_year)

    if songs:
        st.success(f"¡Playlist generada para el mood '{mood}'!")
        for song in songs:
            st.write(f"[{song['name']} - {song['artist']}]({song['url']})")
    else:
        st.warning("No se encontraron canciones para los criterios seleccionados.")

# Funcionalidades futuras
# - Guardar la playlist generada directamente en la cuenta de Spotify del usuario
# - Agregar más estados de ánimo
# - Incluir filtros por género musical
# - Crear una playlist colaborativa
