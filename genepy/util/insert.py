#!/usr/bin/env python

import pysam

'''
Utilities for gathering insert-size statistics from aligned sequences.
Currently only looks at well-aligned sequences.

TODO:
Add options to gather stats based on read-group.
Add options to gather stats based on other sam/bam parameters.
'''

def get_sizes_se(sam):
  '''
  Calculates the average and standard deviation of sequence insert sizes
  given a sam/bam format file.

  Only looks for single-end reads.
  '''
  lengths = dict()
  for read in pysam.Samfile(sam):

    # Skip read if any of the following.
    if read.is_unmapped: continue # Don't want unmapped reads.
    if read.is_paired: continue # Don't want paired reads.

    # Add insert length to the running tally.
    try: lengths[read.rlen] += 1
    except KeyError: lengths[read.rlen] = 1

  # Fin.
  return lengths

def get_sizes_pe(sam):
  '''
  Calculates the average and standard deviation of sequence insert sizes
  given a sam/bam format file.

  Only looks for paired-end reads.
  '''
  lengths = dict()
  for read in pysam.Samfile(sam):

    # Skip read if any of the following.
    if not read.is_paired: continue # Technically not needed due to next line.
    if not read.is_proper_pair: continue
    if not read.is_read1: continue # TODO This doesn't seem to do anything...
    if read.is_secondary: continue
    if read.tlen < 0: continue

    # Add insert length to the running tally.
    try: lengths[read.tlen] += 1
    except KeyError: lengths[read.tlen] = 1

  # Fin.
  return lengths

def get_sizes_mixed(sam,n=None):
  '''
  Calculates the average and standard deviation of sequence insert sizes
  given a sam/bam format file.

  Looks for both single-end and paired-end reads.
  '''
  # TODO Not the most efficient, two trips through file...
  # Could change this to stand-alone function w/ rules as above?
  se_lengths = get_sizes_se(sam)
  pe_lengths = get_sizes_pe(sam)

  lengths = dict(se_lengths)
  for i in pe_lengths:
    try: lengths[i] += pe_lengths[i]
    except KeyError: lengths[i] = pe_lengths[i]

  # Fin.
  return lengths
