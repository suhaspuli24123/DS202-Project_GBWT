#!/bin/bash

set -euo pipefail

mkdir -p data
cd data

# Download GRCh37 reference for chromosome 22
echo "Downloading GRCh37 reference FASTA..."
wget -nc ftp://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.dna.chromosome.22.fa.gz
gunzip -c Homo_sapiens.GRCh37.dna.chromosome.22.fa.gz > Homo_sapiens.GRCh37.dna.chromosome.22.fa

# Index FASTA
echo "Indexing FASTA..."
samtools faidx Homo_sapiens.GRCh37.dna.chromosome.22.fa

# Download VCF (1000 Genomes chr22, phase 3, v5b - already GRCh37)
echo "Downloading VCF..."
wget -nc ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz
wget -nc ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz.tbi

# Create symlinks for easier referencing
ln -sf Homo_sapiens.GRCh37.dna.chromosome.22.fa chr22.fa
ln -sf ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz chr22.vcf.gz
ln -sf ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz.tbi chr22.vcf.gz.tbi

echo "Downloads complete: $(pwd)"