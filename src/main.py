"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs, TASTE_PROFILES


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    # Use a predefined taste profile
    # Options: "energetic_dancer", "chill_studier", "intense_rocker", "relaxed_listener"
    user_prefs = TASTE_PROFILES["energetic_dancer"]

    profile_name = "Energetic Dancer"
    print(f"\n{'='*70}")
    print(f"🎵 MUSIC RECOMMENDER SIMULATION")
    print(f"{'='*70}")
    print(f"\n👤 User Profile: {profile_name}")
    print(f"   Genre: {user_prefs['favorite_genre'].upper()}")
    print(f"   Mood: {user_prefs['favorite_mood'].upper()}")
    print(f"   Target Energy: {user_prefs['target_energy']}")
    print(f"   Likes Acoustic: {user_prefs['likes_acoustic']}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'='*70}")
    print(f"🎬 TOP 5 RECOMMENDATIONS")
    print(f"{'='*70}\n")
    
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        reasons = explanation.split(" | ")
        
        # Print rank and song info
        print(f"#{i}. {song['title'].upper()}")
        print(f"    Artist: {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"    ⭐ Score: {score:.2f}/6.0")
        print(f"\n    Why this match?")
        for reason in reasons:
            print(f"      ✓ {reason}")
        print()


if __name__ == "__main__":
    main()
