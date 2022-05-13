#!/usr/bin/env bash
########################################################################################################################
#######################################   Comparative genomics analyses   ##############################################
########################################################################################################################

########################################################################################################################
# Generating a chronogram. Analysis performed with PhyloBayes version 4.1b:
########################################################################################################################

# Fixed topology provided in file `SpeciesTree_rooted.txt`:
 (((((((Pop_tri:5,((((Cha_fas:1,Sen_tor:1)1:0.5,(Aca_pyc:1,Pro_alb:1)1:0.5) \
 1:0.5,(Gly_max:1,Lup_ang:1)1:1)1:1,Cer_can:3)1:1)1:1,Ara_tha:6)1:1,Vit_vin:7)1:1,\
 (Dau_car:1,Mim_gut:1)1:7)1:1,Aqu_coe:9)1:1,Mus_acu:10)1:1,Amb_tri:11);

# Calibrations used in file `calibrations.txt`:
7
Aca_pyc Pro_alb 61      24
Lup_ang Gly_max 69      64
Cer_can Pro_alb 77      59
Vit_vin Pro_alb 109     97
Dau_car Aqu_coe 124     110
Mus_acu Aqu_coe 173     148
Amb_tri Mus_acu 194 168

# Commands to start chains:
pb -d single_copy_orthologs_85.phy -T SpeciesTree_rooted.txt -cal calibrations.txt -dgam 4 -cat -gtr -ugam chain_1
pb -d single_copy_orthologs_85.phy -T SpeciesTree_rooted.txt -cal calibrations.txt -dgam 4 -cat -gtr -ugam chain_2

# Commands to check running chains:
readdiv chain_1
readdiv chain_2

# Command to compare run stats between chain_1 and chain_2:
tracecomp chain_1 chain_2

# Command to generate chronogram:
readdiv -x 7500 chain_1





########################################################################################################################
# Gene family expansions and contractions within the Leguminosae  using CAFE version 5.0:
########################################################################################################################

# CAFE commands:

/shared/CAFE/bin/cafexp \
--infile large_cafe_input_filtered.tsv \
--tree chain_1_sample_fabales.chronogram \
--fixed_lambda 0.0065630518393034 \
--output large_results_k2_run_1 2>&1 | tee large_run_report1.log


########################################################################################################################
# GO enrichments analyses using GOATOOLS:
########################################################################################################################

#Whole genome background first using script 44_go_whole_genome_background.py


#Then:

(goatools) cjackson@volvox_12:05:02_/media/disk2_12TB/cjackson/37_GO_enrichment$find_enrichment.py \
--pval=0.05 \
CAFE_acacia_significant_increase_go_one-gene-per-line_names_only.txt \
acacia_all_genes_with_interproscan_annotation_names.txt \
acacia_all_genes_go_list_one_gene_multi-term.txt \
--no_propagate_counts \
--outfile_detail out_detail.txt \
--outfile CAFE_sig_increase_GOATOOLS_no_propagate_sections.tsv \
--sections=goatools.test_data.sections.data2018_07_find_enrichment 2>&1 | tee run.log




(goatools) cjackson@volvox_14:48:39_/media/disk2_12TB/cjackson/37_GO_enrichment$find_enrichment.py \
--pval=0.05 \
PFAM_acacia_significant_positive_wego_input_file_names_only.txt \
acacia_all_genes_with_interproscan_annotation_names.txt \
acacia_all_genes_go_list_one_gene_multi-term.txt \
--no_propagate_counts \
--outfile PFAM_acacia_significant_positive_GOATOOLS_no_propagate.tsv \
2>&1 | tee PFAM_acacia_significant_positive_wego_GOATOOLS_no_propagate.log

find_enrichment.py \
--pval=0.05 \
CAFE_acacia_significant_AND_non_significant_increase_wego_input_file_names_only.txt \
acacia_all_genes_with_interproscan_annotation_names.txt \
acacia_all_genes_go_list_one_gene_multi-term.txt \
--outfile CAFE_acacia_significant_AND_non_significant_increase_GOATOOLS_propagate.tsv \
2>&1 | tee CAFE_acacia_significant_AND_non_significant_increase_GOATOOLS_propagate.log

