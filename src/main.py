"""
Command line runner for the Music Recommender Simulation.

Runs the recommender against multiple user profiles — including
adversarial / edge-case profiles — so you can stress-test the
scoring logic and observe unexpected behaviour.
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = [
    # --- Normal profiles ---
    {
        "label": "High-Energy Pop",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "tempo_bpm": 128,
        "valence": 0.85,
        "danceability": 0.88,
        "acousticness": 0.10,
    },
    {
        "label": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "tempo_bpm": 75,
        "valence": 0.58,
        "danceability": 0.55,
        "acousticness": 0.80,
    },
    {
        "label": "Deep Intense Rock",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "tempo_bpm": 150,
        "valence": 0.45,
        "danceability": 0.65,
        "acousticness": 0.08,
    },
    # --- Adversarial / edge-case profiles ---
    {
        "label": "EDGE: High Energy + Sad Mood (conflicting)",
        "genre": "ambient",
        "mood": "sad",          # no song in catalog has mood=sad
        "energy": 0.95,         # ambient songs are all low energy
        "tempo_bpm": 60,
        "valence": 0.20,
        "danceability": 0.30,
        "acousticness": 0.90,
    },
    {
        "label": "EDGE: Genre Miss — every feature matches pop but genre=jazz",
        "genre": "jazz",
        "mood": "happy",
        "energy": 0.82,
        "tempo_bpm": 118,
        "valence": 0.84,
        "danceability": 0.79,
        "acousticness": 0.18,
    },
    {
        "label": "EDGE: All-zeros numeric profile",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.0,
        "tempo_bpm": 0,
        "valence": 0.0,
        "danceability": 0.0,
        "acousticness": 0.0,
    },
]


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

def print_recommendations(label: str, user_prefs: dict, recommendations: list) -> None:
    width = 64
    print()
    print("=" * width)
    print(f" {label}".center(width))
    print("=" * width)
    print(f"  genre={user_prefs['genre']}  mood={user_prefs['mood']}  "
          f"energy={user_prefs['energy']}  tempo={user_prefs['tempo_bpm']}")
    print("-" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}  ({song['artist']})")
        print(f"       Score : {score:.2f}")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")
        print()
    print("=" * width)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        label = profile.pop("label")          # remove display key before scoring
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(label, profile, recommendations)
        profile["label"] = label              # restore so the list stays intact


if __name__ == "__main__":
    main()
