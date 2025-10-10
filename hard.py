def are_anagrams(firstString, secondString):
    print(sorted(firstString), sorted(secondString))
    return sorted(firstString) == sorted(secondString)

# Test cases
print(are_anagrams("listen", "silent"))  # Output: True
print(are_anagrams("hello", "world"))    # Output: False