def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.lower()
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    return text


def calculate_lcs_length(text1, text2):
    m = len(text1)
    n = len(text2)
    lcs_matrix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

    return lcs_matrix[m][n]


def detect_plagiarism(essays, threshold):
    num_essays = len(essays)
    plagiarism_cases = []

    for i in range(num_essays):
        for j in range(i + 1, num_essays):
            essay1 = preprocess_text(essays[i])
            essay2 = preprocess_text(essays[j])
            lcs_length = calculate_lcs_length(essay1, essay2)

            if lcs_length >= threshold:
                plagiarism_cases.append((i, j, lcs_length))

    return plagiarism_cases


# Example usage
essays = [
    "This is the first essay.",
    "This essay is very similar to the second essay.",
    "The third essay is different from the others.",
    "The fourth essay has some overlap with the second essay."
]

plagiarism_threshold = 10

plagiarism_cases = detect_plagiarism(essays, plagiarism_threshold)

# Print plagiarism cases
for case in plagiarism_cases:
    essay1_index, essay2_index, lcs_length = case
    print(f"Potential plagiarism detected between Essay {essay1_index + 1} and Essay {essay2_index + 1}.")
    print(f"LCS Length: {lcs_length}")
    print("---")
