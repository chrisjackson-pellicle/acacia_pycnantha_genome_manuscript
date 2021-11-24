#!/usr/bin/env bash
########################################################################################################################
#######################   Genome assembly using NECAT and downstream polishing and processing   ########################
########################################################################################################################


########################################################################################################################
# Genome assembly performed using NECAT:
########################################################################################################################

# With the following files in the working directory:
#  - `read_list.txt` (specifying the location of the raw nanopore reads)
#  - `acacia_config.txt` (specifying config settings, see Supplementary File S1)

necat.pl correct acacia_config.txt
necat.pl assembly acacia_config.txt
necat.pl bridge acacia_config.txt


########################################################################################################################
# Genome polishing performed using Canu-corrected nanopore reads and Racon version 1.3.3:
########################################################################################################################

# Map Canu-corrected long reads to the NECAT genome assembly:
output_filename=${assembly}
minimap2 \
-ax map-ont \
-N 0 \
-t 30 \
${assembly} \
${corrected_reads} > \
${output_filename%.fasta}_MMr1.sam

# Run Racon:
output_filename=${assembly}
racon \
--include-unpolished \
-t 20 \
${corrected_reads} \
${assembly_sam} \
${assembly} > \
${output_filename%.fasta}_raconLRr1.fasta


########################################################################################################################
# Genome polishing performed using Medaka version v0.11.5:
########################################################################################################################
medaka_consensus \
-i ${corrected_reads} \
-d ${assembly} \
-o medaka_r1 \
-t 20 \
-m r941_prom_high_g303 \

# Subsequently performed a second round of polishing with Medaka

########################################################################################################################
# Genome polishing performed using filtered R1 Illumina reads and Racon version 1.3.3:
########################################################################################################################

# Map filtered R1 Illumina reads to the long-read polished genome avssembly:
output_filename=${assembly}
minimap2 \
-ax sr \
-N 0 \
-t 30 \
${assembly} \
${reads_R1} > \
${output_filename%.fasta}_MMr1.sam

# Run Racon:
output_filename=${assembly}
racon \
--include-unpolished \
-t 20 \
${reads_R1} \
${assembly_sam} \
${assembly} > \
${output_filename%.fasta}_raconSRr1.fasta


########################################################################################################################
# Identify and split potentially misassembled contigs with Tigmint version 1.1.2, using Illumina 10X linked-read data
# output from LongRanger basic:
########################################################################################################################

# Run Tigmint
tigmint-make tigmint draft=wtdbg2_polished_r2 reads=barcoded t=20


########################################################################################################################
# Remove haplotigs and heterozygous contig overlaps with purge_dupes version 0.0.3, using forward and reverse filtered
# Illumina shotgun reads and filtered, corrected nanopore reads:
########################################################################################################################

# With the following files in the working directory:
#  - `config.json` (specifying config settings, see Supplementary File S1)

# Run the Python provided script:
run_purge_dups.py --platform bash config.json /shared/purge_dups/bin acacia


########################################################################################################################
# Scaffold contigs with RAILS v 1.5.1 /Cobbler v0.6.1, using filtered, corrected nanopore reads:
########################################################################################################################

# Run the provided bash script runRAILSminimap.sh:
runRAILSminimap.sh \
consensus_r2_MMr1_raconSRr1.purged.fa \
canu_assembly.correctedReads.fasta \
1000 \
0.90 \
250bp \
1 \
ont \
/usr/local/miniconda3/bin/samtools


########################################################################################################################
# Genome polishing performed on scaffolded, gap-filled assembly performed with Racon version 1.3.3 (2 rounds with
# filtered, corrected nanopore reads, followed by 2 rounds with filtered R1 Illumina reads; commands as described above.
########################################################################################################################


########################################################################################################################
# Split any potentially erroneous contig joins introduced by RAILS with Tigmint using Illumina 10X
# linked-read data output from LongRanger basic; commands as described above.
########################################################################################################################


########################################################################################################################
# Final scaffold of assembly with ARCS version 1.1.0 using Illumina 10X linked-read data output from LongRanger basic:
########################################################################################################################
arcs-make arks draft=${assembly) reads=barcoded t=20 time=1
