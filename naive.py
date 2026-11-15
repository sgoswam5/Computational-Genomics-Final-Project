def suffix_array_naive(text):
    n = len(text)
    sa = list(range(n))

    # Sort suffixes lexicographically
    sa.sort(key=lambda i: text[i:])

    return sa