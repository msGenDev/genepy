#!/usr/bin/env python

import os
import sys
import time
import math
import logging
import argparse

from genepy.util import insert

def main(args):
  # Set up output.
  logging.info('Opening output stream.')
  ofs = args.out and open(args.out,args.append and 'a' or 'w') or sys.stdout

  # Gather insert sizes.
  logging.info('Gathering insert sizes.')
  lengths = map(lambda x: insert.get_sizes_mixed(x), args.files)

  # Calculate stats.
  stats = list()
  for i in lengths:
    num = sum(i.values())
    try: avg = sum(map(lambda x: x[0]*x[1],i.items()))/float(num)
    except ZeroDivisionError: avg = 0.0
    var = sum(map(lambda x: ((x[0]-avg)**2)*x[1],i.items()))
    try: std = math.sqrt(var/num)
    except ZeroDivisionError: std = 0.0
    stats.append((num,avg,std))

  # Report header if necessary.
  logging.info('Reporting stats.')
  fields = ['file','reads','avg','std',]
  ofs.write(args.header and '\t'.join(fields)+'\n' or '')

  # Report stats for each file.
  values = zip(args.files,stats)
  map(lambda x: ofs.write('\t'.join(map(str,[x[0]]+list(x[1])))+'\n'),values)

  # Fin.
  logging.info('Fin.')
  return

if __name__ == '__main__':
  # Determine default logfile name.
  root = __file__.rsplit(os.sep,1)[0]
  name = __file__.rsplit(os.sep,1)[-1].rsplit('.',1)[0]
  date = time.strftime('%Y%m%d')
  logf = '{name}.{date}.log'.format(name=name,date=date)

  # Set up argument parser.
  parser = argparse.ArgumentParser(
    description = 'Paired-End Insert Size Calculator',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter,
  )

  # Positional arguments.
  parser.add_argument('files',type=str,nargs='+',
                      help='Files from which to estimate insert sizes.')

  # Keyword arguments.
  parser.add_argument('--logfile',type=str,default=logf,
                      help='File for which to redirected log output.')
  parser.add_argument('--out',type=str,default=None,
                      help='Target output file.')

  # Flags.
  parser.add_argument('-d','--debug',dest='loglevel',action='store_const',
                      const=logging.DEBUG,default=logging.INFO,
                      help='Set logging level to debug.')
  parser.add_argument('-a','--append',action='store_const',
                      const=True,default=False,
                      help='Append output to file.')
  parser.add_argument('--header',action='store_const',
                      const=True,default=False,
                      help='Print out header.')

  # Parse command line arguments.
  args = parser.parse_args()

  # Set up logging.
  logging.basicConfig(
    level     = args.loglevel,
    filename  = args.logfile,
    format    = '%(asctime)s %(name)-6s %(levelname)-4s %(message)s',)
  logging.info('Starting %s @ %s' % (__file__,os.getcwd()))
  logging.info('args : %s' % str(args))

  # Begin execution.
  try: main(args)
  except Exception as err: logging.error(err)
