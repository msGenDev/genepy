import re

# Generate the regular expression for this file type.
fields = [
  r'(?P<grp>[^\t]+)',             # Group field.
  r'(?P<cov>\d+)',                # Coverage field.
  r'(?P<cnt>\d+)',                # Count field.
  r'(?P<tot>\d+)',                # Total field.
  r'(?P<pct>\d\.\d+(?:e[\+-]\d+)?)', # Percentage field.
]
line_re = re.compile('^{regex}$'.format(regex=r'\t'.join(fields)))

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
    match = line_re.match(line)
    if not match: raise ValueError('line %d malformed' % i)

    # Yield the matched fields.
    yield match.groupdict()
