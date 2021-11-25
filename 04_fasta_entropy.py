#!/usr/bin/env python

import sys
import collections
from Bio import SeqIO
from scipy.stats import entropy
import math


def estimate_shannon_entropy(dna_sequence):
    bases = collections.Counter([tmp_base for tmp_base in dna_sequence])
    # define distribution
    dist = [x / sum(bases.values()) for x in bases.values()]

    # use scipy to calculate entropy
    entropy_value = entropy(dist, base=2)
    # norm_ent = entropy_value/math.log(len(dna_sequence),2)
    return entropy_value


f = open(sys.argv[1], 'r')
g = open(sys.argv[2], 'w')
samplesize = int(sys.argv[3])

c = 0
for i in SeqIO.parse(f, 'fasta'):  # fastq.. whaeva
    c = c + 1
    print("calculating..", c)

    if c <= samplesize:
        shannon = estimate_shannon_entropy(str(i.seq))

        g.write(str(i.id) + "\t" + str(len(i.seq)) + "\t" + str(shannon) + "\n")



