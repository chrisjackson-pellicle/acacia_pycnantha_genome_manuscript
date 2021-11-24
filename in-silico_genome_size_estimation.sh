########################################################################################################################
# In-silico genome size estimation
########################################################################################################################


# Using JellyFish version 2.3.0:
jellyfish count -C -m 21 -s 128000000000 -t 48 filt_illumina/*.fastq -o reads.jf
jellyfish histo -t 24 reads.jf > reads.histo

# Using GenomeScope Rscript `genomescope.R` from https://github.com/schatzlab/genomescope/blob/master/genomescope.R:
Rscript genomescope.R reads.histo 21 150 genomescope/