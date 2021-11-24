#!/usr/bin/env bash

########################################################################################################################
# Read filtering and statistics for Nanopore and Illumina data
########################################################################################################################


#####################################
# Nanopore data
#####################################

# Nanopore read statistics generated using NanoPlot version 1.24.0:
NanoPlot \
-t 20 \
--fastq all_nano_raw.fastq.gz

# Nanopore read filtering performed using NanoFilt version 2.3.0:
gunzip -c all_nano_raw.fastq.gz | NanoFilt --quality 10 --length 1000 > nanopore_filtered.fastq.gz

# Filtered Nanopore read correction using Canu branch v1.9 +321 changes (r9531):
canu_1_9 \
-correct \
-genomeSize \1000m \
-nanopore-raw \
nanopore_filtered.fastq.gz \
useGrid=False \
maxMemory=250 \
maxThreads=50


#####################################
# Illumina genomic 10X data
#####################################

# Basic read and barcode processing including read trimming, barcode error correction, barcode whitelisting, and
# attaching barcodes to reads performed using LongRanger version 2.2.2.
# Output is barcode-attached reads either in FASTQ:
longranger \
basic \
--id=acacia_v1 \
--fastqs /media/disk2_12TB/01_GAP_data/01_Acacia/03_TenX/bpa-gap-genomics-10x-79638/fastq/HFLC3DRXX/SI-GA-C7/ \
--sample=79638 \
--localcores=10 \
--localmem=10


#####################################
# Illumina genomic shotgun data
#####################################

# Adapters used for trimming, provided in file `TruSeq_Adapters.fa`:
>PrefixPE/1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PrefixPE/2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
>PE1
TACACTCTTTCCCTACACGACGCTCTTCCGATCT
>PE1_rc
AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA
>PE2
GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT
>PE2_rc
AGATCGGAAGAGCACACGTCTGAACTCCAGTCA

# Illumina read filtering performed using BBduk version 38.61:
bbduk.sh \
-Xmx51200m \
in1=bpa_R1.fq.gz \
in2=bpa_R2.fq.gz \
out1=illumina_filtered_forward_paired.fq.gz \
out2=illumina_filtered_reverse_paired.fq.gz \
minlen=50 \
k=25 \
mink=8 \
ktrim=r \
ref=TruSeq_Adapters.fa \
hdist=1 \
overwrite=f \
qtrim=rl \
trimq=30 \
t=50 \
bhist=illumina_bhist.txt \
qhist=illumina_qhist.txt \
gchist=illumina_gchist.txt \
aqhist=illumina_aqhist.txt \
lhist=illumina_lhist.txt


#####################################
# Illumina RNAseq shotgun data
#####################################

# Illumina input files:
79638_LibID81994_HNMVTDRXX_AATCCGGA-CTACAGTT_S1_L001_R1.fastq.gz
79638_LibID81994_HNMVTDRXX_AATCCGGA-CTACAGTT_S1_L001_R2.fastq.gz
79638_LibID81995_HNMVTDRXX_TAATACAG-ATATTCAC_S2_L001_R1.fastq.gz
79638_LibID81995_HNMVTDRXX_TAATACAG-ATATTCAC_S2_L001_R2.fastq.gz
79638_LibID81996_HNMVTDRXX_CGGCGTGA-GCGCCTGT_S3_L001_R1.fastq.gz
79638_LibID81996_HNMVTDRXX_CGGCGTGA-GCGCCTGT_S3_L001_R2.fastq.gz


# Illumina read filtering performed using Trimmomatic version 0.39:
R1=${reads_R1}
R2=${reads_R2}
sampleID=${R1%_R[1,2].fastq.gz}
output_forward_paired=${R1%.fastq.gz}_forward_paired.fq.gz
output_reverse_paired=${R2%.fastq.gz}_reverse_paired.fq.gz
output_forward_unpaired=${R1%.fastq.gz}_forward_unpaired.fq.gz
output_reverse_unpaired=${R2%.fastq.gz}_reverse_unpaired.fq.gz
output_both_unpaired=${sampleID}_both_unpaired.fq.gz

java -jar /shared/bin/trimmomatic-0.39.jar \
PE \
-phred33 \
-threads 20 \
${reads_R1} ${reads_R2} \
${output_forward_paired} ${output_forward_unpaired} \
${output_reverse_paired} ${output_reverse_unpaired} \
ILLUMINACLIP:TruSeq3-PE-2.fa:2:30:10:1:true \
LEADING:3 \
TRAILING:3 \
SLIDINGWINDOW:4:20 \
MINLEN:36 \
2>&1 | tee ${sampleID}.log
cat ${output_forward_unpaired} ${output_reverse_unpaired} > ${output_both_unpaired}


# Illumina filtered read normalisation performed using BBNorm version 38.44:
bbnorm.sh \
-Xmx900g \
threads=20 \
in=acacia_RNAseq_R1_all.fastq \
in2=acacia_RNAseq_R2_all.fastq \
out=acacia_RNAseq_R1_all.fastq_target100.fq.gz \
out2=acacia_RNAseq_R2_all.fastq_target100.fq.gz \
mindepth=5 \
target=100
