import sys #needed to get cmd line arguments

def suffix_array_naive(sequence):
    n = len(sequence)

    #create a list containing the starting index of every suffix
    sa = list(range(n))

    #sort the suffixes alphabetically based on the substring starting at each index
    #the sort function compares these suffixes lexicographically
    sa.sort(key=lambda i: sequence[i:])

    #return the sorted starting indices of the suffixes
    return sa


def main():
    #open and read the input file
    with open(sys.argv[1], "r") as f:
        sequence = f.read().strip()

    #construct the suffix array using the naive algorithm
    sa = suffix_array_naive(sequence)

    #print the original sequence and the resulting suffix array
    print("Algorithm: Naive")
    print("Input:", sequence)
    print("Suffix Array:", sa)


if __name__=="__main__":
    main()