# Creating a utils file for functions specific to the MSD
import collections
import numpy as np
from scipy.stats import entropy  # new requirement; we should track these when we publish ;)

# Explanation: the pitches_segments field of the MSD tracks a numeric value [0, 1] for each of the 12 conventional
# semitones (A->G#) over each segment. The result is an array (variable length) of arrays (length 12)

# Naturally, we want to map these variable length arrays to something finite, so we can do math
# So I put together two methods to take in this field value and spit back a 256-length feature vectors,
# and a second method to call those methods for a final vector output of length 512

# I'm borrowing some style here from Berlin & Saxe, "Deep Neural Nets for Malware Detection", but I'll write up
# those details once we do the paper

# We also don't have to focus on this particular field, but I figure it's a start. Gives us some song metadata
# that maps directly from the music, which I think is cool

# So the workflow is: pull the dataset, grab the segments_pitches field, generate a feature vector per song using
# that field (skipping those w/out that field, since can't really do cleaning on seriously empty series data), then
# start to use metrics from Metrics.py to see how things map out

# Feel free to delete these comments whenever you've read them. For explanation of the functions themselves
# (and why I'm doing the weird things I'm doing) we should set up a call - much easier to explain by talking

def vectorize_segments_pitches_distribution(pitches_vector):
    """
    Constructs a 32 by 8 histogram; the 32 represents 32 pitch bins between 0 and 1, the 8 represents each tone (A->G#)
    Goal is to create a single vector which captures pitch range and variety
    """
    # Space out the range [0,1] to 32 equally separated values
    bin_values = np.linspace(0, 1, 32)
    tone_bins = {}
    for tone in range(12):
        tone_bins[tone] = collections.defaultdict(float)

    # Iterate through segments_pitches field and generate 2-D pitches frequency histogram
    for entry in pitches_vector:  # vector of 12 semitones (A->G#)
        for i in range(12):  # for each tone
            pitch_idx = 0
            while entry[i] >= bin_values[pitch_idx]:  # find the bin for that tone's value,
                if pitch_idx == 31:
                    break
                pitch_idx += 1
            tone_bins[i][pitch_idx] += 1  # then save it to tone_bins

    # Now, collapse the 2-D histogram into a 256-length feature vector
    return_vector = []
    for i in range(12):
        for j in range(32):
            return_vector.append(tone_bins[i][j])
    return return_vector


def vectorize_segments_pitches_entropy(pitches_vector):
    """
    For each pitch value, generate a sliding window of length 64. Then over those grouped values,
    compute entropy;
    """
    # Iterate over sliding windows of length 64
    num_windows = len(pitches_vector) // 64
    tone_entropies = collections.defaultdict(list)
    for window_index in range(num_windows + 1):
        i = window_index * 64
        j = (window_index + 1) * 64
        if j > len(pitches_vector):
            j = len(pitches_vector)

        # For each window, collect and group tone values
        tones_vector = collections.defaultdict(list)
        while i < j:
            for tone_idx in range(12):
                tones_vector[tone_idx].append(pitches_vector[i][tone_idx])
            i += 1

        # Compute entropy of tone value over each window for each tone
        for tone in tones_vector.keys():
            window_entropy = entropy(tones_vector[tone])  # is entropy what we want to measure here?
            tone_entropies[tone].append(window_entropy)

    # Separate entropy values per tone into percentiles
    tone_percentiles = collections.defaultdict(list)
    percentiles = np.linspace(0, 1, 21)
    for tone in tone_entropies.keys():
        for p in percentiles:
            p = p * 100
            val = np.percentile(tone_entropies[tone], p)
            tone_percentiles[tone].append(val)

    # Now, collapse the 2-D histogram into a 256-length feature vector
    return_vector = [0, 0, 0, 0, ]  # four empty values; use for other metadata?
    for i in range(12):
        for j in range(21):
            return_vector.append(tone_percentiles[i][j])
    for i in range(len(return_vector)):
        if not isinstance(return_vector[i], float) or np.isnan(return_vector[i]):
            return_vector[i] = 0.
    return return_vector


def vectorize_segments_pitches(pitches_vector):
    pitch_distribution = vectorize_segments_pitches_distribution(pitches_vector)
    pitch_entropy = vectorize_segments_pitches_entropy(pitches_vector)

    return_vector = pitch_distribution + pitch_entropy
    return return_vector
