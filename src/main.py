"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120,
        "valence": 0.85,
        "danceability": 0.80,
        "acousticness": 0.20,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # --- Header ---
    width = 60
    print()
    print("=" * width)
    print(" MUSIC RECOMMENDER — Top Picks For You".center(width))
    print("=" * width)
    print(f"  Profile: genre={user_prefs['genre']}  mood={user_prefs['mood']}  "
          f"energy={user_prefs['energy']}")
    print("-" * width)

    # --- Results ---
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}  ({song['artist']})")
        print(f"       Score : {score:.2f}")
        # Print each reason on its own indented line
        for reason in explanation.split(" | "):
            print(f"         • {reason}")
        print()

    print("=" * width)


if __name__ == "__main__":
    main()
