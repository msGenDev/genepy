import re

# Line regular expressions.
regexes = list()

# Generate the regex for line 0
regexes.append(
  re.compile('^{regex1} + {regex2}.*$'.format(
    regex1=r'(?P<pass>\d+)',
    regex2=r'(?P<fail>\d+)',
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
    yield match.groupdict({'default':match.group(0)})
