import heapq
import re
from nltk.tokenize import sent_tokenize


# Step 1: Text Preprocessing
def preprocess(text):
    # Tokenize into sentences using NLTK
    sentences = sent_tokenize(text)
    # Normalize sentences: convert to lowercase and remove punctuation from each sentence
    normalized_sentences = [re.sub(r'[^\w\s]', '', sentence.lower()) for sentence in sentences]
    return normalized_sentences


# Step 2: Levenshtein Distance Calculation
def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]

    for i in range(1, len_s1 + 1):
        dp[i][0] = i
    for j in range(1, len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No cost if characters match
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],  # Deletion
                                   dp[i][j - 1],  # Insertion
                                   dp[i - 1][j - 1])  # Substitution

    return dp[len_s1][len_s2]


# Step 3: A* Search Algorithm
def a_star_search(sentences1, sentences2):
    num_s1, num_s2 = len(sentences1), len(sentences2)

    open_set = []
    heapq.heappush(open_set, (0, 0, 0, []))  # (f_score, index1, index2, alignment)
    g_score = {(i, j): float('inf') for i in range(num_s1 + 1) for j in range(num_s2 + 1)}
    g_score[(0, 0)] = 0
    f_score = {(i, j): float('inf') for i in range(num_s1 + 1) for j in range(num_s2 + 1)}
    f_score[(0, 0)] = heuristic(0, 0, num_s1, num_s2)

    while open_set:
        _, i, j, alignment = heapq.heappop(open_set)

        # Goal reached, return the alignment
        if i == num_s1 and j == num_s2:
            return alignment

        # Align sentence i with sentence j
        if i < num_s1 and j < num_s2:
            cost = levenshtein_distance(sentences1[i], sentences2[j])
            new_alignment = alignment + [(i, j, cost)]
            tentative_g_score = g_score[(i, j)] + cost
            if tentative_g_score < g_score[(i + 1, j + 1)]:
                g_score[(i + 1, j + 1)] = tentative_g_score
                f_score[(i + 1, j + 1)] = tentative_g_score + heuristic(i + 1, j + 1, num_s1, num_s2)
                heapq.heappush(open_set, (f_score[(i + 1, j + 1)], i + 1, j + 1, new_alignment))

        # Skip a sentence in document 1
        if i < num_s1:
            tentative_g_score = g_score[(i, j)] + 1  # Increment cost for skipping
            if tentative_g_score < g_score[(i + 1, j)]:
                g_score[(i + 1, j)] = tentative_g_score
                f_score[(i + 1, j)] = tentative_g_score + heuristic(i + 1, j, num_s1, num_s2)
                heapq.heappush(open_set, (f_score[(i + 1, j)], i + 1, j, alignment + [(i, -1, 0)]))

        # Skip a sentence in document 2
        if j < num_s2:
            tentative_g_score = g_score[(i, j)] + 1  # Increment cost for skipping
            if tentative_g_score < g_score[(i, j + 1)]:
                g_score[(i, j + 1)] = tentative_g_score
                f_score[(i, j + 1)] = tentative_g_score + heuristic(i, j + 1, num_s1, num_s2)
                heapq.heappush(open_set, (f_score[(i, j + 1)], i, j + 1, alignment + [(-1, j, 0)]))


# Step 4: Heuristic Function
def heuristic(i, j, num_s1, num_s2):
    return abs((num_s1 - i) - (num_s2 - j))


# Step 5: Plagiarism Detection
def detect_plagiarism(alignment, sentences1, sentences2, threshold=1):
    plagiarized_pairs = []
    for pos1, pos2, cost in alignment:
        if cost <= threshold and pos1 != -1 and pos2 != -1:  # Ignore skipped sentences
            plagiarized_pairs.append((sentences1[pos1], sentences2[pos2], cost))
    return plagiarized_pairs


# Example Usage:
if __name__ == "__main__":
    # Input documents
    doc1 = "The quick brown fox jumps over the lazy dog."
    doc2 = "The quick brown fox jumps over the lazy dog."

    # Preprocess the documents
    sentences1 = preprocess(doc1)
    sentences2 = preprocess(doc2)

    # Perform sentence alignment using A* search
    alignment = a_star_search(sentences1, sentences2)

    # Detect plagiarism with a threshold for edit distance
    plagiarized_pairs = detect_plagiarism(alignment, sentences1, sentences2, threshold=1)

    # Output results
    print("Detected Plagiarized Sentences:")
    for s1, s2, cost in plagiarized_pairs:
        print(f"Sentence 1: {s1}")
        print(f"Sentence 2: {s2}")
        print(f"Edit Distance: {cost}\n")
