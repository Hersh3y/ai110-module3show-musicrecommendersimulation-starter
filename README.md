# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world apps like Spotify use both user history (what others clicked) and song details to make suggestions. Because this is a simple simulation, my version focuses only on the song's details. It tries to find songs that closely match the user's preferred vibes and numbers. The Song objects store genre, mood, energy, valence, etc. The UserProfile object stores favorite_genre, favorite_mood, target_energy, and likes_valence.

**Algorithm Recipe: Point-Weighting Scoring System**

Each song in the catalog is scored using the following formula:

Exact Matches (Discrete):
- Genre match: +2.0 points
- Mood match: +1.0 point

Similarity Scoring (Continuous):
- Energy similarity: 1.0 − |user_target_energy − song_energy| (max: 1.0 pts)
- Valence similarity: 0.5 × (1.0 − |user_target_valence − song_valence|) (max: 0.5 pts)
- Danceability similarity: 0.5 × (1.0 − |user_target_danceability − song_danceability|) (max: 0.5 pts)
- Acousticness bonus: +0.3 if user likes acoustic AND song acousticness > 0.5; −0.2 if user dislikes acoustic AND song acousticness > 0.5

Total Score Range: 0 to 6.0 points (higher is better)

The algorithm loops through all 16 songs in the CSV, calculates a score for each, then returns the top K recommendations sorted by score descending.

Why These Weights? Genre is the strongest signal (2.0) because it captures the core taste preference. Mood adds nuance (1.0). Energy is the primary numeric factor because it prevents recommending songs with the wrong intensity level. Valence and danceability refine the recommendation with secondary information. Acousticness is conditional and weighted lower because it's a more specialized preference.

**Expected Biases**

- Genre over-prioritization: High genre weight (2.0) may cause the system to ignore fantastic mood matches in other genres. For example, a user who loves "pop" + "happy" might miss a great "indie pop" song with perfect energy but different genre label.
- Middle-road bias: The numeric similarity scoring favors songs close to the user's target values, potentially missing high-quality "outlier" songs that might be unexpectedly enjoyable.
- Limited catalog: With only 16 songs, the system cannot demonstrate diversity or serendipity—it will often run out of good matches.
- Energy dominance: Energy's 1.0 point weight matches genre (2.0 vs 1.0 for mood), creating a potential over-emphasis on intensity level at the expense of other emotional qualities.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Example Output

Below are screenshots showing the recommender system output (scrolled in two parts):

### Screenshot 1: Top Half of Output
![Output Part 1](terminal1.png)

### Screenshot 2: Bottom Half of Output
![Output Part 2](terminal2.png)

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

