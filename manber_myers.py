import sys #needed to get cmd line arguments

def counting_sort(indices, keys, maximum):
    #create a list to count how many times each rank appears
    counts = [0] * (maximum + 1)

    #count the number of occurrences of each rank
    for i in indices:
        counts[keys[i]] += 1

    #convert the counts into starting positions for each rank
    #this tells us where each rank should start in the sorted array
    total = 0

    for i in range(len(counts)):
        count = counts[i]
        counts[i] = total
        total += count

    #create a new list to store the sorted suffix indices
    result = [0] * len(indices)

    #place each suffix index into its correct sorted position
    for i in indices:
        key = keys[i]
        result[counts[key]] = i
        counts[key] += 1

    #return the indices sorted by their ranks
    return result


def suffix_array_manber_myers(sequence):
    n = len(sequence)

    #return an empty array if the input sequence is empty
    if n == 0:
        return []

    #get all unique characters and sort them alphabetically
    alphabet = sorted(set(sequence))

    #create a dictionary to assign a numerical rank to each character
    #start at 1 so that rank 0 can represent positions past the end
    char_rank = {}

    for i, char in enumerate(alphabet):
        char_rank[char] = i + 1

    #assign initial ranks to each position based on its first character
    rank = []

    for char in sequence:
        rank.append(char_rank[char])

    #create a list containing the starting index of every suffix
    sa = list(range(n))

    #start by comparing prefixes of length 1
    step = 1

    #keep doubling the prefix length until all suffixes are sorted
    while step < n:

        #store the rank of the next block of characters for each suffix
        #the first rank is already stored in rank
        second_rank = [0] * n

        for i in range(n):
            if i + step < n:
                second_rank[i] = rank[i + step]

        #find the largest rank for counting sort
        maximum = max(rank)

        #sort suffixes using pairs of ranks
        #first sort by the second half, then by the first half
        #this is equivalent to sorting by both halves together
        sa = counting_sort(sa, second_rank, maximum)
        sa = counting_sort(sa, rank, maximum)

        #create a list to store the updated ranks
        new_rank = [0] * n

        #keep track of how many unique rank groups we have
        groups = 1

        #the first suffix in sorted order gets rank 1
        new_rank[sa[0]] = groups

        #compare adjacent suffixes in the sorted array
        for i in range(1, n):
            prev = sa[i - 1]
            curr = sa[i]

            #get the rank pairs for the previous and current suffix
            #each pair represents two blocks of length step
            prev_pair = (rank[prev], second_rank[prev])
            curr_pair = (rank[curr], second_rank[curr])

            #if the rank pairs are different, assign a new rank
            #otherwise the suffixes stay in the same rank group
            if prev_pair != curr_pair:
                groups += 1

            new_rank[curr] = groups

        #update the ranks for the next iteration
        rank = new_rank

        #if every suffix has a unique rank, the sorting is complete
        if groups == n:
            break

        #double the prefix length for the next iteration
        step *= 2

    #return the sorted starting indices of all suffixes
    return sa


def main():
    #open and read the input file
    with open(sys.argv[1], "r") as f:
        sequence = f.read().strip()

    #construct the suffix array using manber-myers
    sa = suffix_array_manber_myers(sequence)

    #print the input sequence and resulting suffix array
    print("Algorithm: Manber-Myers")
    print("Input:", sequence)
    print("Suffix Array:", sa)


if __name__=="__main__":
    main()