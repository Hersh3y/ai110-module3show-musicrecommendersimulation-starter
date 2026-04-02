from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import os

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# Example taste profiles for different user types
TASTE_PROFILES = {
    "energetic_dancer": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
        "target_danceability": 0.80,
        "target_valence": 0.75,
        "min_tempo_bpm": 110
    },
    "chill_studier": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
        "target_danceability": 0.55,
        "target_valence": 0.60,
        "max_tempo_bpm": 85
    },
    "intense_rocker": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
        "target_danceability": 0.65,
        "target_valence": 0.50,
        "min_tempo_bpm": 130
    },
    "relaxed_listener": {
        "favorite_genre": "jazz",
        "favorite_mood": "relaxed",
        "target_energy": 0.45,
        "likes_acoustic": True,
        "target_danceability": 0.50,
        "target_valence": 0.70,
        "target_acousticness": 0.80
    }
}

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV file, converting numeric fields to appropriate types."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to appropriate types
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': int(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
        print(f"Successfully loaded {len(songs)} songs.")
    except FileNotFoundError:
        print(f"Error: File not found at {csv_path}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
    
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song using the Algorithm Recipe (genre, mood, energy, valence, danceability, acousticness)."""
    score = 0.0
    reasons = []
    
    # Genre match: +1.0 points (EXPERIMENTAL: halved from 2.0)
    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        score += 1.0
        reasons.append(f"genre match: {song['genre']} (+1.0)")
    
    # Mood match: +1.0 point
    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")
    
    # Energy similarity: 2.0 * (1.0 - |user_target - song_energy|) (EXPERIMENTAL: doubled from 1.0)
    target_energy = user_prefs.get('target_energy', 0.5)
    energy_diff = abs(target_energy - song['energy'])
    energy_similarity = 2.0 * (1.0 - energy_diff)
    score += energy_similarity
    reasons.append(f"energy similarity: {energy_similarity:.2f} (target {target_energy:.2f}, song {song['energy']:.2f})")
    
    # Valence similarity: 0.5 * (1.0 - |user_target - song_valence|)
    target_valence = user_prefs.get('target_valence', 0.5)
    valence_diff = abs(target_valence - song['valence'])
    valence_similarity = 0.5 * (1.0 - valence_diff)
    score += valence_similarity
    reasons.append(f"valence similarity: {valence_similarity:.2f}")
    
    # Danceability similarity: 0.5 * (1.0 - |user_target - song_danceability|)
    target_danceability = user_prefs.get('target_danceability', 0.5)
    danceability_diff = abs(target_danceability - song['danceability'])
    danceability_similarity = 0.5 * (1.0 - danceability_diff)
    score += danceability_similarity
    reasons.append(f"danceability similarity: {danceability_similarity:.2f}")
    
    # Acousticness bonus
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    if likes_acoustic and song['acousticness'] > 0.5:
        score += 0.3
        reasons.append(f"acousticness bonus: +0.3 (user likes acoustic, song is {song['acousticness']:.2f})")
    elif not likes_acoustic and song['acousticness'] > 0.5:
        score -= 0.2
        reasons.append(f"acousticness penalty: -0.2 (user dislikes acoustic, song is {song['acousticness']:.2f})")
    
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank by score, and return top K recommendations with explanations."""
    # Score each song using list comprehension
    scored_songs = [
        (song, score, " | ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # Sort by score descending and return top K
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
