"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs, TASTE_PROFILES


# Adversarial/Edge Case Profiles - Test profiles designed to reveal potential issues
ADVERSARIAL_PROFILES = {
    "conflicting_energy_mood": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",  # Conflicting: sad mood usually pairs with low energy
        "target_energy": 0.9,     # But user wants very high energy!
        "likes_acoustic": False,
        "target_danceability": 0.85,
        "target_valence": 0.2,    # Very low valence (sad)
        "min_tempo_bpm": 140
    },
    "contradictory_acoustic": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,   # Says they like acoustic
        "target_danceability": 0.30,
        "target_valence": 0.65,
        "target_acousticness": 0.2  # But wants LOW acousticness - contradiction!
    },
    "extreme_highs": {
        "favorite_genre": "rock",  # Genre might not match "high" everything
        "favorite_mood": "intense",
        "target_energy": 0.95,     # Extreme high
        "likes_acoustic": False,
        "target_danceability": 0.95,    # Everything at max
        "target_valence": 0.95,
        "min_tempo_bpm": 160
    },
    "extreme_lows": {
        "favorite_genre": "ambient",
        "favorite_mood": "relaxed",
        "target_energy": 0.05,     # Extreme low
        "likes_acoustic": True,
        "target_danceability": 0.05,    # Everything at min
        "target_valence": 0.05,
        "max_tempo_bpm": 50
    },
    "intense_but_lazy": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",  # Intense usually needs high energy
        "target_energy": 0.15,       # But wants very low energy - mismatch!
        "likes_acoustic": False,
        "target_danceability": 0.65,
        "target_valence": 0.3,
        "max_tempo_bpm": 70
    },
    "paradox_energy_tempo": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,       # Wants high energy
        "likes_acoustic": False,
        "target_danceability": 0.8,
        "target_valence": 0.75,
        "max_tempo_bpm": 60  # But wants VERY slow tempo - usually conflict!
    }
}


def run_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Helper function to run recommender for a given profile."""
    print(f"\n{'='*70}")
    print(f"🎵 MUSIC RECOMMENDER SIMULATION")
    print(f"{'='*70}")
    print(f"\n👤 User Profile: {profile_name}")
    print(f"   Genre: {user_prefs['favorite_genre'].upper()}")
    print(f"   Mood: {user_prefs['favorite_mood'].upper()}")
    print(f"   Target Energy: {user_prefs['target_energy']}")
    print(f"   Likes Acoustic: {user_prefs['likes_acoustic']}")
    print(f"   Target Danceability: {user_prefs.get('target_danceability', 'N/A')}")
    print(f"   Target Valence: {user_prefs.get('target_valence', 'N/A')}")
    if 'min_tempo_bpm' in user_prefs:
        print(f"   Min Tempo: {user_prefs['min_tempo_bpm']} BPM")
    if 'max_tempo_bpm' in user_prefs:
        print(f"   Max Tempo: {user_prefs['max_tempo_bpm']} BPM")

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


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Test with standard profile
    run_profile("Energetic Dancer", TASTE_PROFILES["energetic_dancer"], songs)

    # Now test adversarial/edge case profiles
    print(f"\n\n{'#'*70}")
    print(f"# ADVERSARIAL TEST SUITE - Edge Cases & Contradictory Preferences")
    print(f"{'#'*70}")

    for profile_key, profile_prefs in ADVERSARIAL_PROFILES.items():
        # Convert snake_case to readable name
        readable_name = profile_key.replace("_", " ").title()
        run_profile(f"[ADVERSARIAL] {readable_name}", profile_prefs, songs)


if __name__ == "__main__":
    main()
