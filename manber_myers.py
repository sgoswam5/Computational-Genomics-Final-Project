def counting_sort(indices, keys, maximum):
    counts = [0] * (maximum + 1)

    for i in indices:
        counts[keys[i]] += 1

    total = 0

    for i in range(len(counts)):
        count = counts[i]
        counts[i] = total
        total += count

    result = [0] * len(indices)

    for i in indices:
        key = keys[i]
        result[counts[key]] = i
        counts[key] += 1

    return result


def suffix_array_manber_myers(text):
    n = len(text)

    if n == 0:
        return []

    # Assign initial ranks based on characters
    alphabet = sorted(set(text))
    char_rank = {}

    for i, char in enumerate(alphabet):
        char_rank[char] = i + 1

    rank = [char_rank[char] for char in text]
    sa = list(range(n))

    step = 1

    while step < n:
        second_rank = [0] * n

        for i in range(n):
            if i + step < n:
                second_rank[i] = rank[i + step]

        maximum = max(rank)

        # Radix sort by the second rank, then the first rank
        sa = counting_sort(sa, second_rank, maximum)
        sa = counting_sort(sa, rank, maximum)

        # Assign new ranks
        new_rank = [0] * n
        groups = 1

        new_rank[sa[0]] = groups

        for i in range(1, n):
            prev = sa[i - 1]
            curr = sa[i]

            prev_pair = (rank[prev], second_rank[prev])
            curr_pair = (rank[curr], second_rank[curr])

            if prev_pair != curr_pair:
                groups += 1

            new_rank[curr] = groups

        rank = new_rank

        if groups == n:
            break

        step *= 2

    return sa

def main():
    text = "BANANA"

    sa = suffix_array_manber_myers(text)

    print("Algorithm: Manber-Myers")
    print("Input:", text)
    print("Suffix Array:", sa)


if __name__ == "__main__":
    main()