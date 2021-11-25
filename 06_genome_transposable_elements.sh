#!/usr/bin/env bash
########################################################################################################################
######################   Identification, filtering and masking of Transposable elements (TEs)   ########################
########################################################################################################################


########################################################################################################################
# Generate TE library from final genome assembly using the EDTA pipeline version 1.8.4:
########################################################################################################################
EDTA.pl --genome ${assembly} --cds GCF_004799145.1_ASM479914v1_rna.fna --anno 1 --overwrite 0 --threads 40


########################################################################################################################
# Classify TEs using the Transposon Classifier "RFSB" tool from TransposonUltimate version 1.0:
########################################################################################################################
transposon_classifier_RFSB \
-mode classify \
-fastaFile ${EDTA_TE_library}  \
-outputPredictionFile acacia_EDTA_transposons_classified_with_transposonUltimate.txt


########################################################################################################################
# Filter TransposonUltimate classifications where the classification probability of a sequence to either Class I
# (retrotransposons) or Class II (DNA transposons) was less than 0.5; such sequences are labelled as ‘unclassified’.
# See Python script 07_transposonUltimate2EDTA.py
########################################################################################################################


########################################################################################################################
# Soft-mask the genome assembly with RepeatMasker version 4.1.0, using the re-labelled TE library:
########################################################################################################################
RepeatMasker \
-norna \
-nolow \
-xsmall \
-pa 30 \
-cutoff 250 \
-lib ${te_library} \
${assembly}

########################################################################################################################
# Produce TE  RepeatMasker version 4.1.0, using the re-labelled TE library:
########################################################################################################################
RepeatMasker/util/buildSummary.pl ${assembly}.out > transposon_ultimate_filtered_table.tsv