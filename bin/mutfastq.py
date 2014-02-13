#!/usr/bin/env python
import os
import sys
import gzip
import time
import logging
import argparse

from genepy.util import mutseq

def main(args):
  # Set up logging.
  logging.basicConfig(
    level     = args.loglevel,
    filename  = args.logfile,
    format    = '%(asctime)s %(name)-6s %(levelname)-4s %(message)s',)
  logging.info('Starting %s @ %s' % (__file__,os.getcwd()))
  logging.info('args : %s' % str(args))

  # If FASTQ specified, open it.
  if args.fastq:
    if args.gzipped: ifs = gzip.open(args.fastq)
    else: ifs = open(args.fastq)
  # Otherwise, use standard input.
  else: ifs = sys.stdin

  # Generate a mut function.
  mut = mutseq.setup(rate=args.rate,vocab=args.vocab)

  # Mutate each sequence line at the given mutation rate.
  for i,line in enumerate(ifs):
    line = line.strip()
    if not i%4-1: line = mut(line)
    print line

  # Fin.
  return

if __name__ == '__main__':
  # Determine default logfile name.
  root = __file__.rsplit(os.sep,1)[0]
  name = __file__.rsplit(os.sep,1)[-1].rsplit('.',1)[0]
  date = time.strftime('%Y%m%d')
  logf = '{name}.{date}.log'.format(name=name,date=date)

  # Set up argument parser.
  parser = argparse.ArgumentParser(description='FASTQ Random Mutation Generator')

  # Optional Arguments
  parser.add_argument('--debug',dest='loglevel',action='store_const',
                      const=logging.DEBUG,default=logging.INFO,
                      help='Set logging level to debug.')
  parser.add_argument('--logfile',type=str,default=logf,
                      help='File for which to redirected log output.')
  parser.add_argument('--fastq',type=str,
                      help='FASTQ file to mutate.')
  parser.add_argument('--gzipped',action='store_const',
                      const=True,default=False,
                      help='FASTQ file is gzipped.')
  parser.add_argument('--rate',type=float,default=0.0,
                      help='Mutation rate (0.0-1.0).')
  parser.add_argument('--vocab',type=str,default='ACTGN',
                      help='Covabulary to use. [\'ACTGN\']')

  # Parse argumensts and being execution.
  main(parser.parse_args())
