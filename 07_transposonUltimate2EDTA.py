#!/usr/bin/env python

"""
Takes the output file of TransposonUltimate command e.g.:

    transposon_classifier_RFSB -mode classify -fastaFile ../08_necat_assembly_ARKS.fasta.mod.EDTA.TElib.fa \
    -outputPredictionFile acacia_EDTA_transposons_classified_with_transposonUltimate.txt

    head acacia_EDTA_transposons_classified_with_transposonUltimate.txt
    >TE_00000000#DNA/DTM
    Gypsy,LTR,Retrotransposon 1/1/2  0.7 1.0 0.1 0.5 0.1 0.0 0.4 0.0 0.6 0.2 0.0 0.4 0.0 0.1 0.0 0.0 0.8 0.0
    >TE_00000001#DNA/DTC
    Gypsy,LTR,Retrotransposon 1/1/2  0.4 1.0 0.1 0.7 0.0 0.0 0.5 0.0 0.4 0.3 0.0 0.2 0.0 0.0 0.0 0.0 0.6 0.0
    >TE_00000002#DNA/DTC
    Gypsy,LTR,Retrotransposon 1/1/2  0.6 1.0 0.1 0.5 0.1 0.0 0.6 0.1 0.4 0.4 0.1 0.1 0.1 0.1 0.0 0.0 0.3 0.0
    >TE_00000003#DNA/DTC
    Gypsy,LTR,Retrotransposon 1/1/2  0.6 1.0 0.1 0.3 0.0 0.0 0.3 0.0 0.2 0.4 0.0 0.0 0.1 0.0 0.0 0.1 0.3 0.0
    >TE_00000004#DNA/DTA
    Gypsy,LTR,Retrotransposon 1/1/2  0.6 0.9 0.0 0.3 0.0 0.0 0.3 0.0 0.3 0.1 0.0 0.1 0.2 0.1 0.4 0.1 0.8 0.0

...and the TE library fasta file from EDTA, and transfers the annotations from TransposonUltimate to the EDTA
sequences in a format recognised by RepeatMasker e.g. :

    >TE_00008273#DNATransposon/Helitron
    CACTACTACAGAAAACACTTTTAACGTCTGTTTTTAAGACTCTTAG...
    >TE_00008274#Retrotransposon/LTR/Gypsy
    GGTCCCGTTTGGTACAAGGAACTCATAAGAGTTCCTGGGAACATAA...

    etc

"""

import logging
import sys
import argparse
import os
import socket
import fnmatch
from Bio import SeqIO
from scipy.stats import entropy
import collections
import re
from collections import defaultdict

# f-strings will produce a 'SyntaxError: invalid syntax' error if not supported by Python version:
f'Must be using Python 3.6 or higher.'


########################################################################################################################
########################################################################################################################

# Get current working directory and host name:
cwd = os.getcwd()
host = socket.gethostname()


# Configure logger:
def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to create one or multiple loggers.

    :param name: string used for the name of the logger object
    :param log_file: string used for the logging filename
    :param level: logger level
    :return: a logger object
    """

    # Check for existing log files and increment integer as necessary:
    existing_log_file_numbers = [int(file.split('_')[-1]) for file in os.listdir('.') if
                                 fnmatch.fnmatch(file, '*.log*')]
    if not existing_log_file_numbers:
        new_log_number = 1
    else:
        new_log_number = sorted(existing_log_file_numbers)[-1] + 1

    # Log to file:
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler = logging.FileHandler(f'{log_file}.log_{new_log_number}', mode='w')
    f_handler.setFormatter(f_format)

    # Log to Terminal (stdout):
    c_format = logging.Formatter('%(message)s')
    c_handler = logging.StreamHandler(sys.stdout)
    c_handler.setFormatter(c_format)

    # Setup logger:
    logger_object = logging.getLogger(name)
    logger_object.setLevel(level)

    # Add handlers to the logger
    logger_object.addHandler(c_handler)
    logger_object.addHandler(f_handler)

    return logger_object


# Create logger(s):
logger = setup_logger(__name__, 'parse_transposon_ultimate')


########################################################################################################################
########################################################################################################################
# Define general functions:


def splitall(path):
    """
    Splits a path into its constituent parts and returns them as a list
    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def createfolder(directory):
    """
    Attempts to create a directory named after the name provided, and provides an error message on failure
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        logger.info(f'Error: Creating directory: {directory}')


def file_exists_and_not_empty(file_name):
    """
    Check if file exists and is not empty by confirming that its size is not 0 bytes
    """
    # Check if file exist and is not empty
    return os.path.isfile(file_name) and not os.path.getsize(file_name) == 0


def grouped(iterable, n):  # CJJ
    """
    s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ...
    """
    return zip(*[iter(iterable)]*n)


def parse_transposon_ultimate_output(transposon_ultimate_output_file, edta_fasta_file, filter_unclassifed=True):
    """
    Create a dictionary from the EDTA TE library fasta file.
    Parses the output of <transposon_classifier_RFSB -mode classify>.
    Renames sequences in the EDTA TE library fasta file using TransposonUltimate classifications; for any cases where
    the confidence of TransposonUltimate classification to Class I or Class two was less than 0.5, the sequence was
    labelled as <#Unclassified>.


    :param transposon_ultimate_output_file: text file output of running TransposonUltimate in classify mode.
    :param edta_fasta_file: fasta file TE library from EDTA containing the transposable element sequences that were
    (re)classified by TransposonUltimate.
    :return:
    """

    edta_basename = os.path.basename(edta_fasta_file)
    edta_name, edta_ext = os.path.splitext(edta_basename)
    edta_renamed_fasta = f'{edta_name}.renamedTU{edta_ext}'
    print(edta_renamed_fasta)
    transposon_fasta_seqs_dict = SeqIO.to_dict(SeqIO.parse(edta_fasta_file, 'fasta'))

    total_number_of_seqs = 0
    renamed_edta_seqs = []
    number_of_unclassified_seqs = 0
    with open(transposon_ultimate_output_file, 'r') as parse_file_handle:
        lines = parse_file_handle.readlines()
        for fasta_header, classification in grouped(lines, 2):
            if fasta_header.startswith('>'):
                fasta_header = fasta_header.lstrip('>').rstrip()
                seqobject = transposon_fasta_seqs_dict[fasta_header]
                fasta_header_seqname_only = fasta_header.split('#')[0]
                if len(seqobject.seq) == 0:
                    sys.exit(f'Sequence {seqobject.name} is zero length, check this!')
                total_number_of_seqs += 1
                classification_all_levels = classification.split()[0]
                classification_probabilities = classification.split()[2:]
                class_one_probability = classification_probabilities[0]
                class_two_probability = classification_probabilities[8]

                if float(class_one_probability) < 0.5 and float(class_two_probability) < 0.5:
                    print(f'{fasta_header_seqname_only}\n{classification_all_levels}\n{classification_probabilities}\n'
                          f'{class_one_probability}\n{class_two_probability}')
                    number_of_unclassified_seqs += 1
                    seq_rename = f'{fasta_header_seqname_only}#Unclassified'
                    seqobject.name = seq_rename
                    seqobject.id = seq_rename
                    renamed_edta_seqs.append(seqobject)

                elif len(classification_all_levels.split(',')) == 3:
                    level1, level2, level3 = classification_all_levels.split(',')
                    seq_rename = f'{fasta_header_seqname_only}#{level3}/{level2}/{level1}'
                    seqobject.name = seq_rename
                    seqobject.id = seq_rename
                    renamed_edta_seqs.append(seqobject)

                elif len(classification_all_levels.split(',')) == 2:
                    level2, level3 = classification_all_levels.split(',')
                    seq_rename = f'{fasta_header_seqname_only}#{level3}/{level2}'
                    seqobject.name = seq_rename
                    seqobject.id = seq_rename
                    renamed_edta_seqs.append(seqobject)

    print(f'Total number of sequences in classification file: {total_number_of_seqs}')
    print(f'Total number of sequences in renamed file: {len(renamed_edta_seqs)}')
    print(f'Total number of sequences unclassified: {number_of_unclassified_seqs}')

    with open(edta_renamed_fasta, 'w') as renamed_edta_handle:
        SeqIO.write(renamed_edta_seqs, renamed_edta_handle, 'fasta')


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transposon_ultimate_output_file', type=str,
                        help='text output file produced by running transposonUltimate in classify mode')
    parser.add_argument('transposon_fasta_file', type=str,
                        help='fasta file containing the transposable element sequences that were classified')
    results = parser.parse_args()
    return results


########################################################################################################################
########################################################################################################################
# Run script:

def main():
    results = parse_arguments()
    logger.info(f'Running script with: {results}')

    parse_transposon_ultimate_output(
        results.transposon_ultimate_output_file,
        results.transposon_fasta_file
    )


########################################################################################################################
########################################################################################################################

if __name__ == '__main__':
    if not len(sys.argv) >= 1:
        print(__doc__)
        sys.exit()
    sys.exit(main())

########################################################################################################################
########################################################################################################################
