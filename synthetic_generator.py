#Data Generation
#Hyperparameters --> .fa (FASTA)

import os

import numpy as np


def write_fasta(filepath, header, sequence, line_length=80):
    """Writes a DNA sequence to a standard FASTA file format."""
    with open(filepath, 'w') as f:
        f.write(f">{header}\n")
        # Chunk sequence into fixed-width lines (standard FASTA format)
        f.writelines(sequence[i:i+line_length] + '\n' for i in range(0, len(sequence), line_length))

# part 1: numpy.random to generate the uniform random ATGC sequences

def generate_control_sequence(length, seed=42):
    """
    Control 1: Generates a randomized uniform ATGC sequence.
    """
    np.random.seed(seed)
    bases = np.array(['A', 'C', 'G', 'T'])
    
    # Generate random indices and map to bases
    indices = np.random.randint(0, 4, size=length)
    return ''.join(bases[indices])

#part 2: generator function for the Synthetic Repeats to build custom FASTA files.

def generate_synthetic_repeats(unit_length, copy_number, divergence_rate, seed=42):
    """
    Synthetic Repeats: Generates a tandem repeat sequence based on a unit length, 
    duplicates it, and introduces uniformly distributed mutations (divergence).
    """
    np.random.seed(seed)
    bases = np.array(['A', 'C', 'G', 'T'])
    
    # 1. Generate the foundational repeating unit
    unit_indices = np.random.randint(0, 4, size=unit_length)
    base_unit = bases[unit_indices]
    
    # 2. Duplicate the unit to achieve the target copy number
    full_sequence = np.tile(base_unit, copy_number)
    
    # 3. Introduce divergence (point mutations)
    total_bases = unit_length * copy_number
    num_mutations = int(total_bases * divergence_rate)
    
    if num_mutations > 0:
        # Select random distinct positions across the entire sequence to mutate
        mutation_indices = np.random.choice(total_bases, num_mutations, replace=False)
        
        # Apply mutations ensuring the new base is strictly different from the old base
        for idx in mutation_indices:
            current_base = full_sequence[idx]
            possible_mutations = np.setdiff1d(bases, current_base)
            full_sequence[idx] = np.random.choice(possible_mutations)
            
    return ''.join(full_sequence)

# main 

def main():
    # Setup output directory
    output_dir = "data/synthetic"
    os.makedirs(output_dir, exist_ok=True)
    
    # Define target sizes (1 Mb, 2 Mb, 4 Mb)
    MB = 1_000_000
    target_sizes = [1 * MB, 2 * MB, 4 * MB]
    
    print("Generating Control Datasets (Randomized Uniform ATGC)...")
    for size in target_sizes:
        seq = generate_control_sequence(size)
        filepath = os.path.join(output_dir, f"control_uniform_{size // MB}Mb.fa")
        write_fasta(filepath, f"Control_Uniform_{size // MB}Mb", seq)
        print(f"  -> Saved {filepath}")

    print("\nGenerating Synthetic Repeat Sweeps...")
    
    # Sweep 1: Varying Divergence (fixed length 1Mb, fixed unit 10kb, 100 copies)
    unit_len = 10_000
    copies = 100
    divergences = [0.0, 0.01, 0.05, 0.10] # 0%, 1%, 5%, 10% divergence
    
    for div in divergences:
        seq = generate_synthetic_repeats(unit_len, copies, div)
        filename = f"synthetic_unit10k_copies100_div{int(div*100)}pct.fa"
        filepath = os.path.join(output_dir, filename)
        write_fasta(filepath, f"Synthetic_div{div}", seq)
        print(f"  -> Saved {filepath}")
        
    # Sweep 2: Varying Unit Length (fixed length 1Mb, 0% divergence)
    # 100bp * 10000 copies = 1Mb | 1kb * 1000 copies = 1Mb | 100kb * 10 copies = 1Mb
    unit_lengths = [100, 1_000, 100_000] 
    
    for length in unit_lengths:
        c_num = (1 * MB) // length
        seq = generate_synthetic_repeats(length, c_num, divergence_rate=0.0)
        filename = f"synthetic_unit{length}_copies{c_num}_div0pct.fa"
        filepath = os.path.join(output_dir, filename)
        write_fasta(filepath, f"Synthetic_unit{length}", seq)
        print(f"  -> Saved {filepath}")

    print("\nDone! Synthetic sequence generation complete.")

if __name__ == "__main__":
    main()

