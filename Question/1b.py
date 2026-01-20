def segment_keywords(user_query, marketing_keywords_dictionary):
    word_set = set(marketing_keywords_dictionary)
    memo = {}  

    def dfs(start):
        if start in memo:
            return memo[start]

        results = []

        if start == len(user_query):
            return [""]

        for end in range(start + 1, len(user_query) + 1):
            word = user_query[start:end]
            if word in word_set:
                subsequences = dfs(end)
                for seq in subsequences:
                    if seq == "":
                        results.append(word)
                    else:
                        results.append(word + " " + seq)

        memo[start] = results
        return results

    return dfs(0)

user_query = "nepaltrekkingguide"
dictionary = ["nepal", "trekking", "guide", "nepaltrekking"]

print(segment_keywords(user_query, dictionary))
