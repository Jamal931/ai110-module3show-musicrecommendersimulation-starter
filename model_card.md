# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

ScoreMatch 1.0

---

## 2. Intended Use

ScoreMatch 1.0 is a classroom simulation of how a music recommendation engine works. It takes a user's taste profile — things like their favorite genre, preferred mood, and how energetic or danceable they like their music — and returns a ranked list of songs from a small catalog.

The system is built for learning purposes only. It assumes every user can be described by a single, static set of preferences, and it only works with the 10 songs currently in the catalog. It is not intended for real users or production use.

---

## 3. How the Model Works

Imagine you walk into a record store and describe your taste to the clerk: "I like upbeat pop, something happy and danceable." The clerk mentally compares your description to every album on the shelves and picks the ones that seem closest to what you described. ScoreMatch 1.0 does exactly that, but with math instead of intuition.

For each song in the catalog, the system asks seven questions:

1. Does this song's **genre** match what the user said? If yes, +2 points.
2. Does this song's **mood** match what the user said? If yes, +1 point.
3. How close is the song's **energy level** to what the user wants? A perfect match adds up to 1 point; a complete mismatch adds nothing.
4. How close is the song's **tempo** (speed in beats per minute)? Up to 0.5 points.
5. How close is the song's **valence** (musical positivity) to the user's preference? Up to 0.5 points.
6. How close is the song's **danceability**? Up to 0.5 points.
7. How close is the song's **acousticness** (how "live" or instrumental it sounds)? Up to 0.5 points.

All those numbers are added together into a single score. The songs are then sorted from highest to lowest score, and the top five are returned as recommendations.

---

## 4. Data

The catalog contains **10 songs** across 7 genres: pop (2 songs), lofi (3), rock (1), ambient (1), jazz (1), synthwave (1), and indie pop (1). Moods include happy, chill, intense, relaxed, moody, and focused — but notably **no "sad" songs** exist in the catalog at all.

No songs were added or removed from the starter dataset. The catalog skews heavily toward mellow, low-energy styles: 6 of the 10 songs have an energy level below 0.80, and only 3 songs have a clearly danceable, high-energy character (Sunrise City, Gym Hero, Storm Runner). High-BPM or aggressive genres like EDM, hip-hop, country, and classical are entirely absent, meaning users who prefer those styles will always receive off-target recommendations.

---

## 5. Strengths

The system works best when the user's genre and mood are well-represented in the catalog and their numeric preferences are close to actual songs. For example:

- The **Chill Lofi** profile returns three genuine lofi tracks in the top three slots, and Library Rain achieves a near-perfect energy match (+1.00). The results feel correct and would likely satisfy that user.
- The **Deep Intense Rock** profile correctly places Storm Runner — the only rock song — at #1 with a score of 5.95, and its reasoning is completely transparent: you can read exactly why each point was awarded.
- The scoring is **fully explainable**. Every recommendation comes with a bullet-point breakdown of why each point was given, which is something real streaming apps almost never show you.

---

## 6. Limitations and Bias

**Filter bubble by genre label.** The +2.0 genre bonus is larger than the maximum score any song can earn from all five numeric features combined (which tops out at 3.0 points). This means a song that perfectly matches your energy, tempo, mood, and danceability can still lose to a song in the "right" genre that sounds nothing like what you want. In testing, a jazz song with mediocre numeric similarity nearly beat a pop song with a perfect numeric match just because the user typed `genre=jazz`.

**The catalog has no sad songs.** A user who wants sad music will never get a mood match bonus (+1.0). Their top results will be decided almost entirely by genre and numeric features, which means they will receive songs tagged "chill" or "relaxed" as their closest match — not because those songs are similar in emotional tone, but because they happen to score well on energy and acousticness. The system does not know the difference between sad and chill.

**Genre labels are exact-match only.** "Indie pop" does not match "pop." Rooftop Lights — which sounds like a pop song — never earns the genre bonus when a user asks for pop music. Real recommenders use embeddings or taxonomy trees to recognize that indie pop is a sub-genre of pop. This system treats them as completely unrelated.

**The catalog is too small to show diversity.** Rock has one song. Ambient has one song. A rock fan who wants variety gets Storm Runner at #1 and then a mix of unrelated songs filling positions 2–5. A real recommender would surface more variety; this one exhausts the genre in a single result.

**Energy gap punishes extreme preferences unfairly.** If a user sets `energy=0.0` (or any extreme value), the similarity formula `1.0 - abs(song_energy - 0.0)` simply scores songs in reverse order of their energy — it is no longer measuring closeness to a preference, it is measuring how low-energy the song is. A user who genuinely prefers very low energy music will get reasonable results, but the formula was not designed with that interpretation in mind. It works by accident, not by design.

---

## 7. Evaluation

**Profiles tested:** Six profiles were run — High-Energy Pop, Chill Lofi, Deep Intense Rock, and three adversarial edge cases (conflicting preferences, genre miss, all-zeros numeric input).

**What was checked:** For each profile, the top-5 results were compared against musical intuition. Would a real person with these preferences be happy with these songs?

**What was surprising:**

- **Gym Hero keeps appearing for Happy Pop users.** Gym Hero is a pop song tagged as "intense," not "happy." Even though the user explicitly asked for happy music, Gym Hero scores well because it matches the genre (+2.0) and has similar energy and danceability. Without the mood check holding it back, it would rank #1. A non-programmer way to understand this: the system checks *what genre your music is* and *how it sounds physically* (tempo, energy), but it does not really understand what "happy" means emotionally. Gym Hero sounds like pop, moves like pop, and is energetic — so the system thinks it fits, even though a real person would hear it and say "this feels intense, not happy."

- **Halving the genre weight (Experiment A) made the jazz edge case more accurate** without changing any normal-profile rankings. The margin between the correct result (Sunrise City) and the wrong result (Coffee Shop Stories) grew from 0.17 points to 1.62 points, making numeric similarity more competitive.

- **Removing the mood check (Experiment B) made results worse**, not better. Rooftop Lights, which genuinely sounds happy, lost a full point and fell further down the list. Coffee Shop Stories — a jazz track — jumped to #1 for a user who asked for jazz/happy music, despite sounding nothing like upbeat pop. This showed that mood carries real information and should not be removed.

**Comparison between profile pairs:**

- **High-Energy Pop vs. Deep Intense Rock:** Both profiles want high-energy music, and both surfaces high-energy songs near the top. The difference is that pop gets Sunrise City (bright, danceable) while rock gets Storm Runner (distorted, aggressive). The genre label is doing most of the work here — without it, both profiles would return very similar songs because their energy and tempo targets overlap significantly.

- **Chill Lofi vs. EDGE All-Zeros:** Both profiles ask for lofi/chill music, but the all-zeros profile sets every numeric preference to 0. The ranking stays almost identical because the genre and mood bonuses dominate. This reveals that a user who fills in all preferences as 0 gets nearly the same results as a carefully considered lofi profile — the numeric inputs barely matter once the genre label locks in the top results.

- **Jazz/Happy (edge) vs. High-Energy Pop:** These two profiles have nearly identical numeric preferences but different genre tags. The pop profile gets Sunrise City at #1 with a score of 5.95. The jazz profile gets Sunrise City at #1 with a score of 4.00 — but Coffee Shop Stories follows very closely at 3.83. The 0.17-point margin shows how close a mediocre-matching song can get to a perfect match just because it has the right genre label.

---

## 8. Future Work

- **Add more songs.** Ten songs is not enough to show meaningful variety. A catalog of 100+ songs would let numeric similarity matter more, since there would be multiple strong genre matches and the numeric features would decide the final ranking.
- **Lower the genre bonus or make it relative.** Instead of a fixed +2.0, the genre bonus could be scaled based on how many songs in the catalog share that genre. A genre with only one song would get a smaller bonus so it does not automatically dominate.
- **Support sub-genre matching.** "Indie pop" should partially match "pop." A simple fix would be to check whether the user's genre string appears anywhere inside the song's genre tag, rather than requiring an exact match.
- **Add a mood taxonomy.** "Sad" and "chill" are emotionally related in some contexts but not others. A simple mood similarity table (e.g., chill is closer to sad than intense is) would help users who prefer moods the catalog does not directly represent.
- **Test with real users.** The best evaluation would be to ask actual people whether the recommendations matched their taste, rather than relying on the builder's intuition.

---

## 9. Personal Reflection

Building this simulation changed how I think about the recommendation buttons I see every day on Spotify and YouTube. I always assumed those systems were "smart" in some deep way — that they understood music. But this project showed me that a recommender does not need to understand anything. It just needs a scoring rule and a catalog. The results feel intelligent because the rule happens to line up with what humans care about most of the time.

The most surprising discovery was how much a single number — the +2.0 genre bonus — controls the entire output. A song can be wrong in every measurable way and still rank near the top simply because it has the right genre label. That is a bias that a user would never notice just by looking at their recommendations, because the output looks reasonable. It is only when you look at the math that the problem becomes visible. Real AI systems work the same way: the bias is often invisible until you deliberately test for it.

Human judgment still matters because the system has no way to know what a user means by "happy" or "chill." It knows how to measure energy and tempo, but those are physical properties of audio, not emotional ones. Two songs can have identical energy levels and sound completely different emotionally. The system treats them as equivalent. A human would not.
