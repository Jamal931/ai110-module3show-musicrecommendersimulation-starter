# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

ScoreMatch 1.0

---

## 2. Goal / Task

ScoreMatch 1.0 tries to predict which songs from a small catalog a user would enjoy most, given a description of their musical taste. It does not learn from listening history. Instead, it compares a user's stated preferences — genre, mood, energy, tempo, and a few other sound qualities — against every song in the catalog and returns the closest matches in ranked order.

The core task is: *given a taste profile and a list of songs, which songs are most likely to feel right to this person?*

---

## 3. Data Used

- **Catalog size:** 10 songs
- **Features per song:** id, title, artist, genre, mood, energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), acousticness (0–1)
- **Genres represented:** pop (2), lofi (3), rock (1), ambient (1), jazz (1), synthwave (1), indie pop (1)
- **Moods represented:** happy, chill, intense, relaxed, moody, focused — no "sad" songs exist
- **Key limits:** The catalog has no EDM, hip-hop, country, classical, or R&B songs. Only 3 of the 10 songs are high-energy and danceable. The dataset reflects a narrow slice of musical taste, skewed toward mellow and indie styles.

---

## 4. Algorithm Summary

For every song in the catalog, the system computes a compatibility score by asking seven questions and adding up the results:

1. **Genre match** — does the song's genre match what the user said they like? Yes = +2 points, no = +0.
2. **Mood match** — does the song's mood tag match the user's preferred mood? Yes = +1 point, no = +0.
3. **Energy closeness** — how close is the song's energy to the user's target? A perfect match = +1 point; the further away, the fewer points (down to 0).
4. **Tempo closeness** — how close is the song's speed (in BPM) to the user's preference? Up to +0.5 points.
5. **Valence closeness** — how close is the song's "musical positivity" to the user's preference? Up to +0.5 points.
6. **Danceability closeness** — up to +0.5 points.
7. **Acousticness closeness** — up to +0.5 points.

All seven values are added together to get a final score. The songs are then sorted from highest to lowest, and the top 5 are returned as recommendations. Each recommendation includes a bullet-point breakdown showing exactly how many points each component contributed.

---

## 5. Observed Behavior / Biases

**Genre dominates everything.**
The genre bonus (+2.0) is equal to the maximum score a song can earn from all five numeric features combined (3.0 total). In practice, the genre label almost always decides the winner before the numbers are even considered. A song that perfectly matches your energy, tempo, and mood can still lose to a song in the "right" genre that sounds nothing like what you want.

**No sad songs means sad users always get the wrong mood.**
The catalog contains zero songs tagged as "sad." A user who asks for sad music will never receive the +1.0 mood bonus. The system silently falls back to numeric similarity, so it recommends songs that are acoustically close — not emotionally close. It may recommend a "chill" song to a sad-music listener without any indication that the mood was unmatched.

**Exact genre matching excludes close relatives.**
"Indie pop" does not count as a match for "pop." Rooftop Lights — which sounds like a pop song — never earns the genre bonus for pop-preferring users. The system has no concept of genre similarity; genres are either identical or completely unrelated.

**The catalog is too small for real variety.**
Rock, ambient, and jazz each have only one song. A rock fan gets Storm Runner at #1 and then unrelated filler for positions 2–5. This is not a scoring problem — it is a data problem.

---

## 6. Evaluation Process

Six user profiles were tested against the full catalog:

| Profile | Purpose |
| --- | --- |
| High-Energy Pop | Normal case — well-represented genre and mood |
| Chill Lofi | Normal case — 3 lofi songs in catalog, should rank cleanly |
| Deep Intense Rock | Normal case — only 1 rock song, tests what happens after #1 |
| EDGE: Conflicting (ambient + sad + high energy) | Tests missing mood and mismatched numerics |
| EDGE: Genre miss (jazz label, pop numerics) | Tests genre bonus vs. perfect numeric similarity |
| EDGE: All-zeros numeric input | Tests whether numeric features matter when set to 0 |

For each profile, the top-5 results were compared to what a real person with those preferences would likely expect. Two weight experiments were also run:

- **Experiment A (genre ÷2, energy ×2):** Reduced genre bonus from 2.0 → 1.0, doubled energy weight. Normal-profile rankings were unchanged. The jazz edge case improved significantly — Coffee Shop Stories dropped from #2 to #5, and the correct result (Sunrise City) opened a 1.62-point lead instead of a 0.17-point lead.
- **Experiment B (mood removed):** Commented out the mood check entirely. Results got worse: Gym Hero overtook Sunrise City for Happy Pop, and Coffee Shop Stories jumped to #1 for jazz/happy. Mood carries real signal and should not be removed.

**Biggest surprise:** Gym Hero keeps appearing near the top for happy pop users even though it is tagged as "intense." It scores well because it matches the genre (+2.0) and has similar energy and danceability. The system checks whether a song *sounds like* pop (tempo, energy, danceability), but it cannot tell whether a song *feels* happy vs. intense — those two things can co-exist in the same audio features.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
This system is designed for classroom exploration of how scoring-based recommenders work. It is suitable for testing how different weights and features change output rankings, and for practicing reasoning about algorithmic bias with a small, transparent dataset.

**Not intended for:**

- Real music discovery. The 10-song catalog is too small and too narrow to reflect any real user's taste.
- Users who listen to genres not in the dataset (EDM, hip-hop, country, classical, R&B, metal, etc.). Those users will always receive poor recommendations.
- Any context where fairness across diverse musical tastes matters. The catalog systematically underrepresents high-energy, urban, and non-Western music.
- Production deployment of any kind. There is no user authentication, no listening history, no feedback loop, and no error handling for missing preferences.

---

## 8. Ideas for Improvement

1. **Expand the catalog to 100+ songs.** With 10 songs, the genre bonus almost always decides the winner. With 100 songs per genre, the numeric features would actually determine which song within the genre is the best match — which is where the interesting differentiation happens.

2. **Make the genre bonus proportional, not fixed.** Instead of always adding +2.0 for a genre match, scale the bonus based on how many songs in the catalog share that genre. A genre with 20 songs would get a smaller bonus per match than a genre with only 1 song, because the numbers can do more work when there is more variety.

3. **Use partial genre matching.** Check whether the user's genre string appears as a substring of the song's genre tag (so "pop" matches "indie pop," "synth pop," "dream pop"). This one change would fix the Rooftop Lights problem without any math changes.

---

## 9. Personal Reflection

**What was my biggest learning moment?**
The moment I ran the numbers and discovered that `genre + mood = 3.0` — equal to the entire numeric ceiling — was the most clarifying point of the project. I had designed what felt like a balanced scoring system, but the math showed it was dominated by two categorical labels. The numbers (energy, tempo, valence, danceability, acousticness) looked important but were often just tiebreakers. Building the system from scratch made that invisible imbalance visible in a way that just reading about recommenders never would have.

**How did using AI tools help, and when did I need to double-check them?**
AI tools (Claude Code, in this case) were most useful for writing boilerplate quickly — the CSV loader, the loop structure, the output formatter — and for explaining *why* a specific sorting approach (like `sorted()` vs `.sort()`) was the right choice. The moments that required double-checking were when I accepted a suggestion without verifying the math. For example, the energy similarity formula `1.0 - abs(a - b)` is correct for values between 0 and 1, but it can return a negative number if the values are more than 1 apart. I had to check the data to confirm all values were in the 0–1 range before trusting the formula. AI tools write plausible-looking code; the programmer still needs to verify the assumptions.

**What surprised me about how a simple algorithm can still "feel" like a real recommendation?**
The output surprised me every time I changed a profile and got a result that felt genuinely right — like the Chill Lofi profile returning Library Rain at #1 with a perfect energy score. It felt smart. But nothing smart was happening: the formula found the song with the closest numbers. The "feeling" of intelligence came from the fact that the song's audio features happen to correlate with what humans call "chill." The algorithm did not understand chill — it just found the nearest point in a seven-dimensional space. That gap between "feels intelligent" and "is actually intelligent" is probably the most important thing I will carry forward from this project.

**What would I try next if I extended this project?**
I would replace the fixed genre bonus with a learned weight — let the system try different genre bonus values (0.5, 1.0, 1.5, 2.0) against a small set of labeled test cases and pick the one that produces the most accurate rankings. That would turn this from a hand-tuned scoring system into a simple optimization problem, which is conceptually how real recommendation engines begin before they add neural networks. I would also add a feedback button to the CLI ("Was this recommendation good? y/n") so the system could collect signal and adjust weights over time.
