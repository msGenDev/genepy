import re

# Line regular expressions.
regexes = list()

# Generate the regex for line 0.
regexes.append(
  re.compile(r'^@{regex1} {regex2}$'.format(
    regex1=r':'.join([
      r'(?P<name>[^:]+)',         # Machine name.
      r'(?P<run>\d+)',            # Run number.
      r'(?P<flow>[^:]+)',         # Flowcell name.
      r'(?P<lane>\d+)',           # Flowcell lane.
      r'(?P<tile>\d+)',           # Tile number.
      r'(?P<xpos>\d+)',           # X coordinate of cluster.
      r'(?P<ypos>\d+)',           # Y coordinate of cluster.
    ]),
    regex2=r':'.join([
      r'(?P<pair>\d)',            # Pair for paired end.
      r'(?P<pass>[YN])',          # Passed filter.
      r'(?P<cntl>\d+)',           # Control bits.
      r'(?P<index>[ACTGactg]+)',  # Index sequence.
    ]),
    )
  )
) # regexes.append regex line 0

# Generate the regex for line 1.
regexes.append(
  re.compile(r'^{regex}$'.format(
    regex=r'(?P<seq>\w+)',  # Sequence.
    )
  )
) # regexes.append regex line 1

# Generate the regex for line 2.
regexes.append(
  re.compile(r'^\+(?:{regex1} {regex2})?$'.format(
    regex1=r':'.join([
      r'(?P<name>[^:]+)',         # Machine name.
      r'(?P<run>\d+)',            # Run number.
      r'(?P<flow>[^:]+)',         # Flowcell name.
      r'(?P<lane>\d+)',           # Flowcell lane.
      r'(?P<tile>\d+)',           # Tile number.
      r'(?P<xpos>\d+)',           # X coordinate of cluster.
      r'(?P<ypos>\d+)',           # Y coordinate of cluster.
    ]),
    regex2=r':'.join([
      r'(?P<pair>\d)',            # Pair for paired end.
      r'(?P<pass>[YN])',          # Passed filter.
      r'(?P<cntl>\d+)',           # Control bits.
      r'(?P<index>[ACTGactg]+)',  # Index sequence.
    ]),
    )
  )
) # regexes.append regex line 2

# Generate the regex for line 3.
regexes.append(
  re.compile(r'^{regex}$'.format(
    regex=r'(?P<qual>.+)',  # Qualities.
    )
  )
) # regexes.append regex line 3

def parse(ifs):
  '''
  FASTQ Casava 1.8 format file parser.

  Parameters:
    ifs - sequence of FASTQ Casava 1.8 format lines

  Yields:
    dict - dict of parsed line elements based on current line
  '''
  # Parse this file as if it is a FASTQ Casava 1.8 format file.
  for i,line in enumerate(ifs):

    # Sanity check line format.
    match = regexes[i%len(regexes)].match(line)
    if not match: raise ValueError('line %d malformed' % i)

    # Yield the matched fields.
    yield match.groupdict()
