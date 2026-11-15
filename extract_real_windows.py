#Data Manipulation
#.bed + .fa.gz --> .fa

import os

import pybedtools
import pysam


def get_chromosome_length(fasta_path, chrom="chr13"):
    """Uses pysam to quickly check the exact length of the chromosome."""
    with pysam.FastaFile(fasta_path) as fasta:
        # pysam automatically reads the .fai index file
        return fasta.get_reference_length(chrom)

def find_densest_window(bed_path, chrom, chrom_len, window_size):
    """
    Creates overlapping sliding windows across the chromosome and finds the one 
    that contains the maximum number of base pairs overlapping the BED features.
    """
    # Create sliding windows (step size is half the window size for better coverage)
    step_size = window_size // 2
    windows = pybedtools.BedTool().window_maker(
        genome={chrom: (0, chrom_len)}, 
        w=window_size, 
        s=step_size
    )
    
    # Load the BED file containing the repeat coordinates
    features = pybedtools.BedTool(bed_path)
    
    # Calculate coverage of the repeats within sliding windows
    # Output columns: chrom, start, end, count, overlap_bp, window_len, fraction
    coverage = windows.coverage(features)
    
    max_overlap = -1
    best_window = None
    
    for interval in coverage:
        # Field [4] in bedtools coverage output is the total overlapping base pairs
        overlap_bp = int(interval.fields[4])
        
        if overlap_bp > max_overlap:
            max_overlap = overlap_bp
            best_window = (interval.chrom, interval.start, interval.end)
            
    return best_window, max_overlap

def extract_and_save_fasta(fasta_path, window, output_path, header_name):
    """Slices the exact DNA string from the reference FASTA and saves it."""
    chrom, start, end = window
    
    with pysam.FastaFile(fasta_path) as fasta:
        # pysam is 0-indexed, extracting [start, end)
        sequence = fasta.fetch(chrom, start, end)
        
    # Write to a standard 80-character wrapped FASTA format
    with open(output_path, 'w') as f:
        f.write(f">{header_name} {chrom}:{start}-{end}\n")
        f.writelines(sequence[i:i+80] + '\n' for i in range(0, len(sequence), 80))

def main():
    # Setup directories
    data_dir = "data/raw"
    out_dir = "data/extracted_windows"
    os.makedirs(out_dir, exist_ok=True)
    
    # Placeholder paths
    reference_fasta = os.path.join(data_dir, "chm13v2.0_chr13.fa.gz")
    
    # Dictionary of BED files 
    repeat_beds = {
        "Alu_SINE": os.path.join(data_dir, "alu.bed"),
        "L1_LINE": os.path.join(data_dir, "l1.bed"),
        "CenSat": os.path.join(data_dir, "censat_v2.1.bed"),
        "SegDups": os.path.join(data_dir, "sd.bed")
    }
    
    MB = 1_000_000
    window_sizes = [1 * MB, 2 * MB, 4 * MB]
    target_chrom = "chr13"
    
    # Skips execution without files, but validates logic
    if not os.path.exists(reference_fasta):
        print(f"Waiting for {reference_fasta} from data team. Pipeline ready.")
        return

    chrom_length = get_chromosome_length(reference_fasta, target_chrom)
    print(f"Loaded {target_chrom} ({chrom_length // MB} Mb total).")

    for repeat_name, bed_file in repeat_beds.items():
        if not os.path.exists(bed_file):
            print(f"  -> Missing {bed_file}, skipping...")
            continue
            
        print(f"\nProcessing {repeat_name}...")
        
        for size in window_sizes:
            print(f"  Finding densest {size // MB}Mb window...")
            
            best_window, overlap_bp = find_densest_window(
                bed_file, target_chrom, chrom_length, size
            )
            
            density_pct = (overlap_bp / size) * 100
            print(f"    Found at {best_window[0]}:{best_window[1]}-{best_window[2]} "
                  f"({density_pct:.1f}% repeat density)")
            
            # Extract the actual string and save it for the constructors
            out_name = f"{repeat_name}_{size // MB}Mb.fa"
            out_path = os.path.join(out_dir, out_name)
            
            extract_and_save_fasta(
                reference_fasta, best_window, out_path, 
                header_name=f"{repeat_name}_Densest_{size//MB}Mb"
            )
            print(f"    Saved to {out_path}")

if __name__ == "__main__":
    main()
    