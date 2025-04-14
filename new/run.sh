#!/bin/bash

set -euo pipefail

FASTA="data/chr22.fa"
VCF="data/chr22.vcf.gz"
SAMPLE_NAME="chr22"
OUTDIR="vg_indexes"
LOGDIR="logs"
CSV_OUTPUT="performance_metrics.csv"

mkdir -p "$OUTDIR" "$LOGDIR"

# Initialize CSV file with headers
echo "Step,Runtime_Seconds,Memory_MB,FileSize_MB,Paths" > "$CSV_OUTPUT"

# Initialize global run log
RUN_LOG="$LOGDIR/run.log"
echo "Run started at $(date '+%Y-%m-%d %H:%M:%S')" > "$RUN_LOG"

# Function to extract memory usage from time output
extract_memory() {
  grep "Maximum resident set size" "$1" | awk '{print $6/1024}'
}

# Function to extract runtime from time output
extract_runtime() {
  grep "User time" "$1" | awk '{print $4}'
}

# Function to get file size in MB
get_filesize() {
  du -m "$1" | cut -f1
}

# 1. Construct VG graph (only once)
echo "Constructing VG graph..."
TIME_LOG="$LOGDIR/${SAMPLE_NAME}_construct_time.log"
/usr/bin/time -v vg construct \
  -r "$FASTA" -v "$VCF" -C -a -t 2 --handle-sv false \
  > "$OUTDIR/$SAMPLE_NAME.vg" \
  2> >(tee "$LOGDIR/${SAMPLE_NAME}_construct.err" > "$TIME_LOG")

# Extract and record metrics
VG_RUNTIME=$(extract_runtime "$TIME_LOG")
VG_MEMORY=$(extract_memory "$TIME_LOG")
VG_FILESIZE=$(get_filesize "$OUTDIR/$SAMPLE_NAME.vg")
echo "VG,$VG_RUNTIME,$VG_MEMORY,$VG_FILESIZE,NA" >> "$CSV_OUTPUT"
echo "VG graph constructed. Runtime: ${VG_RUNTIME}s, Memory: ${VG_MEMORY}MB, Size: ${VG_FILESIZE}MB" >> "$RUN_LOG"

# 2. XG index (only once)
echo "Building XG index..."
TIME_LOG="$LOGDIR/${SAMPLE_NAME}_xg_time.log"
/usr/bin/time -v vg index \
  -x "$OUTDIR/$SAMPLE_NAME.xg" \
  -L "$OUTDIR/$SAMPLE_NAME.vg" \
  -t 2 \
  > /dev/null \
  2> >(tee "$LOGDIR/${SAMPLE_NAME}_xg.err" > "$TIME_LOG")

# Extract and record metrics
XG_RUNTIME=$(extract_runtime "$TIME_LOG")
XG_MEMORY=$(extract_memory "$TIME_LOG")
XG_FILESIZE=$(get_filesize "$OUTDIR/$SAMPLE_NAME.xg")
echo "XG,$XG_RUNTIME,$XG_MEMORY,$XG_FILESIZE,NA" >> "$CSV_OUTPUT"
echo "XG index built. Runtime: ${XG_RUNTIME}s, Memory: ${XG_MEMORY}MB, Size: ${XG_FILESIZE}MB" >> "$RUN_LOG"

# 3. GBWT index with different path counts
for PATHS in 10 20 50; do
  # Calculate sample range based on path count (each sample has 2 haplotypes)
  SAMPLES=$((PATHS / 2))
  SAMPLE_RANGE="0-$((SAMPLES - 1))"
  
  echo "Building GBWT index with $PATHS paths (samples $SAMPLE_RANGE)..."
  TIME_LOG="$LOGDIR/${SAMPLE_NAME}_gbwt_${PATHS}_time.log"
  GBWT_FILE="$OUTDIR/${SAMPLE_NAME}_${PATHS}.gbwt"
  
  /usr/bin/time -v vg gbwt \
    -x "$OUTDIR/$SAMPLE_NAME.xg" \
    -o "$GBWT_FILE" \
    --num-threads 2 \
    -v "$VCF" \
    --buffer-size 25 \
    --batch-size 10 \
    --force-phasing \
    --discard-overlaps \
    --sample-range "$SAMPLE_RANGE" \
    > /dev/null \
    2> >(tee "$LOGDIR/${SAMPLE_NAME}_gbwt_${PATHS}.err" > "$TIME_LOG")

  # Extract and record metrics
  GBWT_RUNTIME=$(extract_runtime "$TIME_LOG")
  GBWT_MEMORY=$(extract_memory "$TIME_LOG")
  GBWT_FILESIZE=$(get_filesize "$GBWT_FILE")
  echo "GBWT-$PATHS,$GBWT_RUNTIME,$GBWT_MEMORY,$GBWT_FILESIZE,$PATHS" >> "$CSV_OUTPUT"
  echo "GBWT index with $PATHS paths built. Runtime: ${GBWT_RUNTIME}s, Memory: ${GBWT_MEMORY}MB, Size: ${GBWT_FILESIZE}MB" >> "$RUN_LOG"
done

echo "All steps completed at $(date '+%Y-%m-%d %H:%M:%S')" >> "$RUN_LOG"
echo "Performance metrics saved to $CSV_OUTPUT"