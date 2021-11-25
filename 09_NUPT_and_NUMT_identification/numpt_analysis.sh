#numpt analysis, T. Allnutt, 2021

#make blast db of necat assembly Blast v2.9.0+
makeblastdb -in 08_necat_assembly_ARKS_rename.fasta -input_type fasta -title necat -dbtype nucl -out ~/db/acacia/necat

#plastid blast
blastn -task dc-megablast -evalue 1e-5 -perc_identity 85 -db ~/db/acacia/necat -num_threads 48 -max_target_seqs 999 -query assembly_unicycler.fasta -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore' -out necat-nupt.blast

#filter nested blast hits 1=contig name column 7=hit start column 8=hit end column
blast-nest-filter.py necat-nupt.blast cp_nestfilt.blast 1 7 8

#get the list of nupt contigs
cut -f1 cp_nestfilt.blast > cp_contigs.list

#get the nupt contigs from assembly
get-seqs-from-file.py cp_contigs.list 08_necat_assembly_ARKS_rename.fasta nupt_contigs.fasta " "

#Repeat above for mtDNA

#mtDNA blast
blastn -task dc-megablast -evalue 1e-5 -perc_identity 85 -db ~/db/acacia/necat -num_threads 48 -max_target_seqs 999 -query mt_unicycler.fasta -outfmt '6 qseqid sseqid pident length slen qstart qend sstart send evalue bitscore' -out necat-numt.blast

#filter nested blast hits 1=contig name column 7=hit start column 8=hit end column
blast-nest-filter.py necat-numt.blast mt_nestfilt.blast 1 7 8

#get the list of numt contigs
cut -f1 cp_nestfilt.blast > mt_contigs.list

#get the numt contigs from assembly
get-seqs-from-file.py mt_contigs.list 08_necat_assembly_ARKS_rename.fasta numt_contigs.fasta " "

#combine cp and mt blasts
cat cp_nestfilt.blast mt_nestfilt.blast > combined.blast

#concatenate tandem numpts that are within 300 bp of each other
concat_numpts.py combined.blast comb_cat.blast 300 1 6 7

#get the combined contigs
cut -f1 comb_cat.blast >comb_numpt_contigs.list

get-seqs-from-file.py comb_numpt_contigs.list 08_necat_assembly_ARKS_rename.fasta numpt_contigs.fasta " "

#map illumna reads to numpt containing contigs using bbmap v38.90
bbmap.sh ref=numpt_contigs.fasta in=illumina_filtered_R1_paired.fastq.gz in2=illumina_filtered_R2_paired.fastq.gz unpigz=t perfectmode=t t=48 outm=illumina_numpt.sam

#remove unmapped reads from sam using bbmap reformat.sh
reformat.sh in=illumina_numpt.sam mappedonly=t out=illumina_mapped.sam

#manually made gff3 format file of numpt loci from comb_cat.blast


#make sam file of reads that overlap numpts and produce summary file numpt_summary.tab of numpt, contig, overlap reads, non-overlap reads.
numpt_overlap_sam.py illumina_mapped.sam comb_cat.gff3 comb_overlaps.sam 20














#concatenate tandem numpts 



