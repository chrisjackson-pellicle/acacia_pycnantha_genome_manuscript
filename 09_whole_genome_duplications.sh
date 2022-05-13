#!/usr/bin/env bash
########################################################################################################################
####################################   Whole Genome Duplication analyses   #############################################
########################################################################################################################

cjackson@volvox_09:14:47_/media/disk2_12TB/cjackson/36_WholeGenomeDuplication$perl /shared/TransDecoder-TransDecoder-v5.5.0/util/gff3_file_to_proteins.pl


bokeh serve &

wgd \
viz -i \
-ks acacia-vs-prosopis_one-to-one.tsv,\
acacia-vs-senna_one-to-one.tsv,\
acacia-vs-cercis_one-to-one.tsv,\
acacia-vs-lupinus_one-to-one.tsv \
--labels acacia/prosopis,\
acacia/senna,\
acacia/cercis,\
acacia/lupinus


wgd \
viz -i \
-ks acacia_anchors.tsv,\
prosopis_anchors.tsv,\
senna_anchors.tsv,\
cercis_anchors.tsv,\
lupinus_anchors.tsv \
--labels acacia_anchor_pairs,\
prosopis_anchor_pairs,\
senna_anchor_pairs,\
cercis_anchor_pairs,\
lupinus_anchor_pairs


wgd viz -i \
-ks acacia.ks.tsv,\
prosopis.ks.tsv,\
senna.ks.tsv,\
cercis.ks.tsv,\
lupinus.ks.tsv \
--labels acacia_whole_paranome_Ks,\
prosopis_whole_paranome_Ks,\
senna_whole_paranome_Ks,\
cercis_whole_paranome_Ks,\
lupinus_whole_paranome_Ks


wgd viz -i \
-ks acacia_anchors.tsv,\
prosopis_anchors.tsv,\
senna_anchors.tsv,\
cercis_anchors.tsv,\
lupinus_anchors.tsv,\
acacia-vs-prosopis_one-to-one.tsv,\
acacia-vs-senna_one-to-one.tsv,\
acacia-vs-cercis_one-to-one.tsv,\
acacia-vs-lupinus_one-to-one.tsv \
--labels acacia_anchor_pairs,\
prosopis_anchor_pairs,\
senna_anchor_pairs,\
cercis_anchor_pairs,\
lupinus_anchor_pairs,\
acacia/prosopis,\
acacia/senna,\
acacia/cercis,\
acacia/lupinus