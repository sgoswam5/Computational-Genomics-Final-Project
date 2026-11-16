
import sys #needed to get cmd line arguments


def ternary_quicksort(sa, start, end, key):
    #create a stack containing the range of suffixes we want to sort
    #we use a stack instead of recursion to keep track of the groups
    stack = [(start, end)]

    #continue until all groups have been sorted
    while stack:
        left, right = stack.pop()

        #if the group only has one suffix, it is already sorted
        if right - left <= 1:
            continue

        #choose the middle suffix's rank as the pivot
        pivot = key(sa[(left + right) // 2])

        #use three pointers to divide suffixes into three groups
        #low: suffixes with ranks smaller than the pivot
        #mid: suffixes currently being examined
        #high: suffixes with ranks greater than the pivot
        low = left
        mid = left
        high = right

        #partition suffixes based on their ranks
        while mid < high:
            value = key(sa[mid])

            #if the rank is smaller than the pivot, move it left
            if value < pivot:
                sa[low], sa[mid] = sa[mid], sa[low]
                low += 1
                mid += 1

            #if the rank is greater than the pivot, move it right
            elif value > pivot:
                high -= 1
                sa[mid], sa[high] = sa[high], sa[mid]

            #if the rank equals the pivot, leave it in the middle
            else:
                mid += 1

        #sort the group containing smaller ranks
        if low - left > 1:
            stack.append((left, low))

        #sort the group containing larger ranks
        if right - high > 1:
            stack.append((high, right))


def suffix_array_larsson_sadakane(sequence):
    n = len(sequence)

    #return an empty array if the sequence is empty
    if n == 0:
        return []

    #initially sort suffixes based on their first character
    #each number represents the starting index of a suffix
    sa = sorted(range(n), key=lambda i: sequence[i])

    #create a list to store the rank of each suffix
    rank = [0] * n

    #keep track of the number of unique groups
    groups = 0
    start = 0

    #group suffixes that begin with the same character
    while start < n:
        end = start + 1

        #find where the current group of equal characters ends
        while end < n and sequence[sa[start]] == sequence[sa[end]]:
            end += 1

        #assign the same rank to all suffixes in this group
        #the rank is the last position of the group in the suffix array
        for i in range(start, end):
            rank[sa[i]] = end - 1

        #increase the number of groups and move to the next group
        groups += 1
        start = end

    #start with prefixes of length 1
    step = 1

    #keep refining groups until every suffix has a unique rank
    while groups < n and step < n:

        #create a new list for the updated ranks
        new_rank = [0] * n

        #count how many groups we have after refinement
        new_groups = 0
        start = 0

        #get the rank of the next block of characters
        #if the next block is past the end of the string, return -1
        def continuation(pos):
            if pos + step < n:
                return rank[pos + step]
            return -1

        #go through each existing group of suffixes
        while start < n:

            #find the ending position of the current group
            end = rank[sa[start]] + 1

            #only sort groups that contain multiple suffixes
            #groups with one suffix are already uniquely ranked
            if end - start > 1:
                ternary_quicksort(sa, start, end, continuation)

            #split the current group into smaller groups
            #based on the ranks of the next block of characters
            left = start

            while left < end:
                right = left + 1

                #get the rank of the next block for this suffix
                value = continuation(sa[left])

                #find all suffixes that have the same continuation rank
                while right < end:
                    if continuation(sa[right]) != value:
                        break
                    right += 1

                #assign the same new rank to suffixes that remain tied
                for i in range(left, right):
                    new_rank[sa[i]] = right - 1

                #increment the group count and move to the next group
                new_groups += 1
                left = right

            #move to the next original group
            start = end

        #replace the old ranks with the updated ranks
        rank = new_rank
        groups = new_groups

        #double the prefix length for the next iteration
        step *= 2

    #return the sorted suffix starting indices
    return sa


def main():
    #open and read the input file
    with open(sys.argv[1], "r") as f:
        sequence = f.read().strip()

    #construct the suffix array using larsson-sadakane
    sa = suffix_array_larsson_sadakane(sequence)

    #print the original sequence and the resulting suffix array
    print("Algorithm: Larsson-Sadakane")
    print("Input:", sequence)
    print("Suffix Array:", sa)


if __name__=="__main__":
    main()
