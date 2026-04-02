from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return (total_score, reasons) for one song judged against user_prefs."""
    score = 0.0
    reasons = []

    # --- Categorical features (fixed bonuses) ---
    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # --- Numerical features (closeness rewards) ---
    # Energy: full weight
    if "energy" in user_prefs:
        energy_score = 1.0 - abs(song["energy"] - float(user_prefs["energy"]))
        score += energy_score
        reasons.append(f"energy similarity ({energy_score:+.2f})")

    # Tempo: half weight, normalised over an 80 BPM window
    if "tempo_bpm" in user_prefs:
        tempo_score = max(0.0, 1.0 - abs(song["tempo_bpm"] - float(user_prefs["tempo_bpm"])) / 80)
        score += 0.5 * tempo_score
        reasons.append(f"tempo similarity ({0.5 * tempo_score:+.2f})")

    # Valence: half weight
    if "valence" in user_prefs:
        valence_score = 1.0 - abs(song["valence"] - float(user_prefs["valence"]))
        score += 0.5 * valence_score
        reasons.append(f"valence similarity ({0.5 * valence_score:+.2f})")

    # Danceability: half weight
    if "danceability" in user_prefs:
        dance_score = 1.0 - abs(song["danceability"] - float(user_prefs["danceability"]))
        score += 0.5 * dance_score
        reasons.append(f"danceability similarity ({0.5 * dance_score:+.2f})")

    # Acousticness: half weight
    if "acousticness" in user_prefs:
        acoustic_score = 1.0 - abs(song["acousticness"] - float(user_prefs["acousticness"]))
        score += 0.5 * acoustic_score
        reasons.append(f"acousticness similarity ({0.5 * acoustic_score:+.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest-to-lowest, and return the top k as (song, score, explanation)."""
    scored = [
        (song, *score_song(user_prefs, song))   # (song_dict, score, reasons_list)
        for song in songs
    ]

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return [(song, score, " | ".join(reasons)) for song, score, reasons in ranked[:k]]
