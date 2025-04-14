# DS202-Project_Pan Genomic Indexing and Search using Generalized BWT

Presented by PULI SUHAS REDDY and ABHINAV RAGHUNATHAN

## Prerequisites

- Linux-based operating system
- vg toolkit (version 1.64.1 or later)
- Python 3.7+ with the following libraries:
  - pandas
  - matplotlib
  - seaborn
  - numpy
- At least 12GB RAM for processing chromosome 22

## Installation

1. Install the vg toolkit:
```
git clone https://github.com/vgteam/vg.git
cd vg
make
```

## Usage

### 1. Data Download

Run the `download.sh` script to download the necessary inputs:

```
cd new
./download.sh
```

This script will:
- Download the chromosome 22 reference sequence (GRCh37)
- Download the 1000 Genomes Project VCF file for chromosome 22
- Create symlinks for easier referencing

### 2. VG Construction and Indexing

Execute the `run.sh` script to perform VG construction, XG indexing, and GBWT indexing:

This script will:
- Construct the VG graph for chromosome 22
- Build the XG index
- Create GBWT indexes for different path counts (10, 20, and 50)
- Log performance metrics (runtime, memory usage, and file sizes)
- Save metrics to a CSV file named `performance_metrics.csv`

```
cd new
./run.sh
```

### 3. Data Visualization

Use the `plot.py` script to generate performance visualizations:
```
cd new
python plot.py
```


This script will create visualizations of memory usage, runtime, and file sizes for the different data structures.

## Results and Analysis

### Memory Usage


Memory usage (in MB) for chromosome 22 with VG, XG, and GBWT. GBWT has taken around 2.7 GB RAM. (only for 12 paths)

Our measurements show the following memory usage patterns:
- VG construction: 12,189.5 MB
- XG indexing: 4,448.27 MB
- GBWT indexing (10 paths): 2,283.1 MB
- GBWT indexing (20 paths): 2,346.55 MB
- GBWT indexing (50 paths): 2,409.86 MB

**Caution – Increasing the number of paths can dramatically increase memory usage. Do it at your own risk!**

### Runtime


Construction time (in seconds) of VG, XG, GBWT of chromosome 22. Since XG is already computed, GBWT construction time is very less.

Our runtime measurements:
- VG construction: 265.97 seconds
- XG indexing: 207.65 seconds
- GBWT indexing (10 paths): 266.65 seconds
- GBWT indexing (20 paths): 267.89 seconds
- GBWT indexing (50 paths): 280.49 seconds

### File Sizes


Output file sizes (in MB) for chromosome 22 using VG, XG, and GBWT. We can see that GBWT takes up space lower than the original variant graph.

Our file size measurements:
- VG graph: 102 MB
- XG index: 680 MB
- GBWT index (10 paths): 52 MB
- GBWT index (20 paths): 52 MB
- GBWT index (50 paths): 53 MB

The XG index is significantly larger than both the VG graph and the GBWT index. The GBWT index remains remarkably compact even as the number of paths increases from 10 to 50.

### Path Count Comparison

Our analysis included a comparison of GBWT performance with different numbers of paths (10, 20, and 50):

| Paths | Memory (MB) | Runtime (s) | File Size (MB) |
|-------|-------------|-------------|----------------|
| 10    | 2,283.1     | 266.65      | 52             |
| 20    | 2,346.55    | 267.89      | 52             |
| 50    | 2,409.86    | 280.49      | 53             |

This shows a modest increase in memory usage and runtime as the number of paths increases, with minimal impact on file size. The GBWT index demonstrates excellent scalability in terms of storage requirements.

## Conclusion

The performance metrics demonstrate that:

1. **Memory efficiency**: While VG construction is the most memory-intensive operation (12,189.5 MB), the resulting GBWT index is quite space-efficient in memory.

2. **Storage optimization**: The GBWT index provides a compact representation of haplotype information, requiring less storage space (52-53 MB) than the original VG graph (102 MB).

3. **Scalability considerations**: Increasing the number of paths in GBWT construction from 10 to 50 shows only a modest increase in memory usage (from 2,283.1 MB to 2,409.86 MB), suggesting good scalability for larger datasets.

4. **XG index characteristics**: The XG index has the largest file size (680 MB) but provides efficient random access to the graph structure, which is essential for subsequent operations.

These findings highlight the trade-offs between memory usage, runtime, and storage requirements when working with variation graphs for genomic data. The GBWT index in particular shows excellent storage efficiency, making it suitable for representing haplotype information in large-scale genomic analyses.
