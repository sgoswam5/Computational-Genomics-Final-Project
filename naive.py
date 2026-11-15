def suffix_array_naive(text):
    n = len(text)
    sa = list(range(n))

    # Sort suffixes lexicographically
    sa.sort(key=lambda i: text[i:])

    return sa

def main():
    text = "BANANA"

    sa = suffix_array_naive(text)

    print("Algorithm: Naive")
    print("Input:", text)
    print("Suffix Array:", sa)


if __name__ == "__main__":
    main()