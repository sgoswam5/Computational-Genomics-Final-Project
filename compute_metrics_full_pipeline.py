import numpy as np
from pydivsufsort import divsufsort, kasai


def get_inherent_metrics(sequence_string):
    # Convert string to numpy byte array (required by pydivsufsort)
    seq_bytes = np.frombuffer(sequence_string.encode('ascii'), dtype=np.uint8)
    
    # 1. Build Suffix Array instantly using the off-the-shelf library
    sa = divsufsort(seq_bytes)
    
    # 2. Build LCP Array using Kasai's algorithm
    lcp = kasai(seq_bytes, sa)
    
    # 3. Derive BWT (last characters of the sorted suffixes)
    # The SA gives the starting index of each sorted suffix; 
    # BWT is the character immediately preceding it.
    bwt = np.where(sa == 0, seq_bytes[-1], seq_bytes[sa - 1])
    
    # 4. Count BWT runs (r)
    # A run is a sequence of identical consecutive characters
    runs = 1 + np.count_nonzero(bwt[1:] != bwt[:-1])
    
    # 5. Extract inherent metrics
    return {
        "lcp_max": int(np.max(lcp)),
        "lcp_mean": float(np.mean(lcp)),
        "bwt_runs": int(runs),
        "r_over_n": float(runs) / len(sequence_string)
    }

