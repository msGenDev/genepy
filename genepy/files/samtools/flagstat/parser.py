import re

# Line regular expressions.
regexes = list()

# Generate the regex for line 0
regexes.append(
  re.compile('^{regex1} + {regex2} in total \(QC-passed reads \+ QC-failed reads\)$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
  ))
)

# Generate the regex for line 1
regexes.append(
  re.compile('^{regex1} + {regex2} duplicates$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
  ))
)

# Generate the regex for line 2
regexes.append(
  re.compile('^{regex1} + {regex2} mapped \({regex3}%\)$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
    regex3=r'(?P<pct>\d+\.\d+)',
  ))
)

# Generate the regex for line 3
regexes.append(
  re.compile('^{regex1} + {regex2} paired in sequencing$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
    regex3=r'paired in sequencing',
  ))
)

# Generate the regex for line 4
regexes.append(
  re.compile('^{regex1} + {regex2} read1$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
  ))
)

# Generate the regex for line 5
regexes.append(
  re.compile('^{regex1} + {regex2} read2$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
  ))
)

# Generate the regex for line 6
regexes.append(
  re.compile('^{regex1} + {regex2} properly paired \({regex3}NaV\)$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
    regex3=r'(?P<nav>\d+\.\d+)',
  ))
)

# Generate the regex for line 7
regexes.append(
  re.compile('^{regex1} + {regex2} with itself and mate mapped$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
  ))
)

# Generate the regex for line 8
regexes.append(
  re.compile('^{regex1} + {regex2} singletons \({regex3}NaV\)$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
    regex3=r'(?P<pct>\d+\.\d+)',
  ))
)

# Generate the regex for line 9
regexes.append(
  re.compile('^{regex1} + {regex2} with mate mapped to a different chr$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
  ))
)

# Generate the regex for line 10
regexes.append(
  re.compile('^{regex1} + {regex2} with mate mapped to a different chr \(mapQ\>\={regex3}\)$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
    regex3=r'(?P<qual>\d+)',
  ))
)

def parse(ifs,**kwargs):
  '''
  SAMTools flagstat format file parser.

  Parameters:
    ifs - sequence of coverage lines

  Yields:
    dict - dict of parsed line elements
  '''
  # Parse this file as if it is a coverage file.
  for i,line in enumerate(ifs):

    # Sanity check line format.
    match = regexes[i%len(regexes)].match(line)
    if not match: raise ValueError('line %d malformed' % i)

    # Yield the matched fields.
    yield match.groupdict()
