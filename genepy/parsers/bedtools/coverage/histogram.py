import re

# Line regular expressions.
regexes = list()

# Generate the regex for line 0
regexes.append(
  re.compile('^{regex}$'.format(
    regex=r'\t'.join([
      r'(?P<grp>[^\t]+)',                 # Group field.
      r'(?P<cov>\d+)',                    # Coverage field.
      r'(?P<cnt>\d+)',                    # Count field.
      r'(?P<tot>\d+)',                    # Total field.
      r'(?P<pct>\d\.\d+(?:e[\+-]\d+)?)',  # Percentage field.
    ]),
    )
  )
) # regexes.append regex line 0

def parse(ifs,**kwargs):
  '''
  Coverage histogram file parser.

  Line format:
    <grp>\\t<cov>\\t<cnt>\\t<tot>\\t<pct>\\n

  Parameters:
    ifs - sequence of coverage lines

  Yields:
    dict - dict of parsed line elements
      cov : str
      cov : int
      cnt : int
      tot : int
      pct : float
  '''
  # Parse this file as if it is a coverage file.
  for i,line in enumerate(ifs):

    # Sanity check line format.
    match = regexes[i%len(regexes)].match(line)
    if not match: raise ValueError('line %d malformed' % i)

    # Yield the matched fields.
    yield match.groupdict()
