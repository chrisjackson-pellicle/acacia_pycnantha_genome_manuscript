#!/usr/bin/env bash
########################################################################################################################
############################   Structural gene prediction and functional annotation   ##################################
########################################################################################################################



In total 57,483 genes were predicted by BRAKER2; additional filtering for putative TEs removed 1,067 genes, leaving 56,416 predicted genes.


########################################################################################################################
# Filtering via support using script 47_filter_genes_via_support.py:

# Arguments supplied:
full.txt \
any.txt \
no.txt \
braker_seqs_no_te_pfam_nostops.fasta.tsv \
braker_seqs_no_te_pfam_withInterproResults.fasta \
ORTHOFINDER_acacia-only_orthogroup_InterProScan_table.tsv \
ORTHOFINDER_acacia_unassigned_sequences_InterProScan_table.tsv \
Aca_pyc_output_domain_table \
one-to-one-query_seqs.fa.emapper.annotations.tsv \
all_user_ko.txt

# Stage 1:

# Get stats on genes with full, some and no evidence from BRAKER hints.gtf output
    # (https://github.com/Gaius-Augustus/BRAKER/issues/319.):

# The script is called selectSupportedSubsets.py and it's located here
# https://github.com/Gaius-Augustus/BRAKER/tree/report/scripts/predictionAnalysis. To run it, you will need to have
# the predictionAnalysis.py file saved in the same folder.

cjackson@volvox_11:54:59_/media/disk2_12TB/cjackson/16_braker/17_target100_AND_1kp_no_alt_transcripts_30Sep2020/results/01_braker/braker/03_filtering_genes_on_evidence$



# Parameters used for eggNOG functional annotation using online portal as http://eggnog-mapper.embl.de/:
Minimum hit e-value 0.001
Minimum hit bit-score 60
Percentage identity 40
Minimum % of query coverage 20
Minimum % of subject coverage 20
Orthology restrictions: Transfer annotations from one-to-one orthology only
Gene Ontology evidence: Transfer non-electronic annotations

# Command used for functional annotation with InterProScan version 5.50-84.0:
interproscan.sh -cpu 20 -i ${acacia_predicted_proteins}.fasta --goterms --iprlookup --output-dir 01_acacia_interproscan


# Annotation counts:

/Users/chrisjackson/Desktop/Research/01_GAP/01_acacia/000_reanalysis_post_single_isoform_and_no-support_genes_removed/27_annotation_count_from_databases/01_annotated_gene_lists % cat genes_with_eggnog_annotation.txt genes_with_interproscan_annotation_no_mobi.txt genes_with_kegg_annotation.txt genes_with_pfam_annotation.txt | sort | uniq | wc -l
   44889

wc -l ./*
   42999 ./genes_with_eggnog_annotation.txt
   44315 ./genes_with_interproscan_annotation.txt
   43026 ./genes_with_interproscan_annotation_no_mobi.txt
   14414 ./genes_with_kegg_annotation.txt
   33555 ./genes_with_pfam_annotation.txt