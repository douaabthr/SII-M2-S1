def levenshtein_distance(s1, s2):
    n,m = len(s1), len(s2)

    # matrix creation
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize first row and column
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 2

            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )
    for row in dp:
        print(row)
    return dp[m][n]


# === Read input strings ===
s1 = input("Enter the first string: ")
s2 = input("Enter the second string: ")

# === Compute and display distance ===
distance = levenshtein_distance(s1, s2)
print(f"Levenshtein distance between '{s1}' and '{s2}' is {distance}")
