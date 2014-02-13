#!/usr/bin/env python

import re
import random
random.seed()

def setup(rate=0.0,vocab='ACTGN'):
  '''
  Returns a mutseq function with the rate and vocab fixed.

  Keyword arguments:
    rate  - rate of mutations (0.0-1.0) [0.0]
    vocab - vocabulary of seq and mutations ['ACTG']

  Returns:
    func - mutseq function with fixed rate and vocab
  '''

  # Sanity checks the rate range.
  if rate < 0.0 or rate > 1.0:
    raise ValueError('rate must be in the range [0.0,1.0]')

  # Set up for sanity checking input sequences.
  vocab_re = re.compile(r'^[{vocab}]+$'.format(vocab=vocab))

  def mutseq(seq):
    '''
    Introduce random mutations into a sequence string.

    Positional arguments:
      seq - sequence string to mutate

    Returns:
      str - mutated sequence string
    '''
    # Sanity check the sequence content.
    if not vocab_re.match(seq): raise ValueError(seq)

    # Randomly mutate positions.
    seq = list(seq)
    for i,rand in enumerate([random.random() for i in xrange(len(seq))]):
      if rand < rate: seq[i] = random.sample(set(vocab)-set(seq[i]),1)[0]

    # Return the mutated sequence.
    return ''.join(seq)

  # Return the set up mutseq.
  return mutseq
