#!/usr/bin/env bash

########################################################################################################################
# Generating a chronogram. Analysis performed with PhyloBayes version 4.1b
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





