def ternary_quicksort(sa, start, end, key):
    stack = [(start, end)]

    while stack:
        left, right = stack.pop()

        if right - left <= 1:
            continue

        pivot = key(sa[(left + right) // 2])

        low = left
        mid = left
        high = right

        while mid < high:
            value = key(sa[mid])

            if value < pivot:
                sa[low], sa[mid] = sa[mid], sa[low]
                low += 1
                mid += 1

            elif value > pivot:
                high -= 1
                sa[mid], sa[high] = sa[high], sa[mid]

            else:
                mid += 1

        if low - left > 1:
            stack.append((left, low))

        if right - high > 1:
            stack.append((high, right))


def suffix_array_larsson_sadakane(text):
    n = len(text)

    if n == 0:
        return []

    # Initially sort suffixes by their first character
    sa = sorted(range(n), key=lambda i: text[i])

    rank = [0] * n
    groups = 0
    start = 0

    # Assign ranks based on groups of equal characters
    while start < n:
        end = start + 1

        while end < n and text[sa[start]] == text[sa[end]]:
            end += 1

        for i in range(start, end):
            rank[sa[i]] = end - 1

        groups += 1
        start = end

    step = 1

    while groups < n and step < n:
        new_rank = [0] * n
        new_groups = 0
        start = 0

        def continuation(pos):
            if pos + step < n:
                return rank[pos + step]
            return -1

        while start < n:
            # Find the boundary of the current group
            end = rank[sa[start]] + 1

            # Sort groups containing multiple suffixes
            if end - start > 1:
                ternary_quicksort(
                    sa, start, end, continuation
                )

            # Split into smaller groups
            left = start

            while left < end:
                right = left + 1
                value = continuation(sa[left])

                while right < end:
                    if continuation(sa[right]) != value:
                        break
                    right += 1

                for i in range(left, right):
                    new_rank[sa[i]] = right - 1

                new_groups += 1
                left = right

            start = end

        rank = new_rank
        groups = new_groups
        step *= 2

    return sa

def main():
    text = "BANANA"

    sa = suffix_array_larsson_sadakane(text)

    print("Algorithm: Larsson-Sadakane")
    print("Input:", text)
    print("Suffix Array:", sa)


if __name__ == "__main__":
    main()