# Reflection: User Profile Testing & Recommendation Behavior

## Profile Pair Comparisons

### 1. Energetic Dancer vs. Chill Studier

**What changed**: Energetic Dancer gets fast pop songs (Sunrise City at 4.89, energy 0.82). Chill Studier gets slow lofi tracks (Library Rain at 5.285, energy 0.35). The score difference is small, but the *actual songs* are completely opposite.

**Why it makes sense**: The energy preference is now weighted 2x as heavily as before, so a 0.35 energy target pulls toward acoustic, slow songs while a 0.85 target pulls toward upbeat, bouncy tracks. Even though the Chill Studier's #1 song (Library Rain) isn't "energetic" by any definition, the energy similarity calculation (1.0 - |0.35-0.35| = 2.0) becomes a powerhouse component of their score.

**Non-programmer explanation**: Imagine you're recommending coffee backgrounds: someone studying wants the sound of a quiet library (low energy), someone at a gym wants heavy metal (high energy). Energy is now the strongest signal—if you nail the energy level, everything else is secondary.

---

### 2. Energetic Dancer vs. Intense Rocker

**What changed**: Both want high-energy songs (0.85 vs 0.90), but the Energetic Dancer prefers happy moods while the Intense Rocker wants aggressive/intense. Despite similar energy, they get almost completely different top 5 lists.

**Why it makes sense**: The Energetic Dancer's #1 is Sunrise City (pop, happy) but the Intense Rocker's #1 is Storm Runner (rock, intense). The 2x energy multiplier helps pull matching songs, but the exact genre and mood matches (now worth +1.0 and +1.0 respectively) are strong enough to override energy. But here's the trap: **both users get "Gym Hero" in their top 5** (ranks #2 and #2). This is because Gym Hero is pop+intense+high energy (0.93), which partially matches both profiles even though it shouldn't be ideal for either.

**Non-programmer explanation**: Think of it like streaming services recommending the same "top energy" song to both a happy-pop lover and an angry-rocker. The system sees "high energy = high energy" and forgets that a 0.93 energy intense pop song is tiring for a pop fan (who wants happy) AND wrong genre for a rocker. The binary mood/genre matching creates blind spots.

---

### 3. Chill Studier vs. Relaxed Listener  

**What changed**: Both users love acoustic music and want low energy (0.35 vs 0.45). But Chill Studier dominates within lofi (scores 5.285, 5.105) while Relaxed Listener struggles to find jazz matches and settles for lofi (scores 3.110, 3.095).

**Why it makes sense**: Chill Studier's favorite genre (lofi) has 3 songs in the dataset. Relaxed Listener's favorite genre (jazz) has only 1 song. Without the exact genre match, Relaxed Listener loses +1.0 points and has to compete on energy and acoustic bonuses alone. The Chill Studier's #1 song scores 5.285 while Relaxed Listener's best non-jazz options score ~3.1. This is the filter bubble in action: users whose taste exists in the dataset get inflated scores; users whose taste is rare get penalized.

**Non-programmer explanation**: If Spotify has 10 lofi songs but only 1 jazz song, lofi lovers will always see higher match scores. The system isn't being unfair—it's just revealing that the *dataset* doesn't represent all music tastes equally. A jazz fan will feel like the system is pushing them toward lofi, when really it's just that lofi is overrepresented.

---

### 4. Intense Rocker vs. Randomized Non-Match User  

**What changed (hypothetical test)**: When matching a user who wants "metal" against a dataset that only has "heavy metal", the user gets 0/2 bonus points from genre+mood and must rely entirely on energy similarity.

**Why it makes sense**: The Intense Rocker is "lucky"—rock exists in the dataset (1 song). But if you tested a "Synth Pop Enthusiast" (wants synth-pop, which doesn't exist as a genre) they'd get zero genre points from synthwave or pop individually and would fall back to pure energy matching. The system has no mechanism for fuzzy/partial matching or genre hierarchies.

**Non-programmer explanation**: It's like asking about books in a library. If you ask for "science fiction", you get all sci-fi books. But if you ask for "soft science fiction", the system can't help—it's an all-or-nothing text match. Users have to match exactly what the dataset calls things, or they get nothing.

---

## Key Insight: Energy is Now the "Common Currency"

Before the 2x weight change, genre (37.7%) and energy (18.9%) were balanced. Now energy (37.7%) dominates, and it's the only continuous feature that bridges across genre/mood boundaries. This explains why Gym Hero shows up for both the Energetic Dancer and the Intense Rocker—they both want high energy, and that's what the algorithm optimizes for.

**This is actually a problem**: High energy should make a song *more appealing*, not a *replacement* for getting the genre wrong. But with the weights as they are, a mediocre-but-high-energy song can outrank a perfect-but-medium-energy song.
