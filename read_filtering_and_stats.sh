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
#TODO Longranger commands


#####################################
# Illumina genomic shotgun data
#####################################

# Illumina read filtering performed using BBduk version 38.61:
bbduk.sh -Xmx51200m \
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

#TODO RNAseq filtering commands