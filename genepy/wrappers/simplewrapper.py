import logging
import subprocess

class SimpleWrapper(object):
  '''
  Simple Wrapper object.
  '''
  def __init__(self,exe,*args,**opts):
    '''
    Initializes the wrapper.

    Positional arguments:
      exe     - Target executable string
      Additional positional arguments passed before options.

    Keyword arguments:
      stdin   - Filehandle for executable input
      stdout  - Filehandle for executable output
      stderr  - Filehandle for executable errors
      optpre  - Options prefix
      Additional keywords passed as options with optpre as option prefix.
      NOTE: These keyword arguments prevent usage as options.
            Therefore, they would need to be passed in the call.
    '''
    # Set state variables.
    self.exe    = exe
    self.args   = args
    self.opts   = opts
    self.stdin  = self.opts.pop('stdin',None)
    self.stdout = self.opts.pop('stdout',None)
    self.stderr = self.opts.pop('stderr',None)
    self.optpre = self.opts.pop('optpre','-')
    # If PIPEs are offered for stdout or stderr, log a warning.
    if self.stdout == subprocess.PIPE:
      logging.warning('stdout specified as PIPE - may cause permanent blocking')
    if self.stderr == subprocess.PIPE:
      logging.warning('stderr specified as PIPE - may cause permanent blocking')
    # Fin.
    return

  def __getitem__(self,key):
    '''
    Returns the keyword argument key.
    '''
    return self.opts[key]

  def __setitem__(self,key,val):
    '''
    Sets the keyword argument key to value val.
    '''
    self.opts[key] = val

  def __delitem__(self,key):
    '''
    Unsets the keyword argument key.
    '''
    del self.opts[key]

  def __call__(self,*args,**opts):
    '''
    Invokes the executable.
    '''
    logging.info('Executing call to %s' % self.exe)

    # Generate the call.
    call = []
    # Add the executable.
    call.append(self.exe)
    # Add the prefix arguments.
    for arg in self.args:
      call.append(str(arg))
    # Add the constructor options specified.
    for x,y in self.opts.items():
      if not y: call.append('%s%s' % (str(self.optpre),str(x),))
      else: call.extend(('%s%s' % (str(self.optpre),str(x),), str(y)))
    # Add the positional arguments specified.
    for arg in args:
      call.append(str(arg))
    # Add the options specified.
    for x,y in opts.items():
      if not y: call.append('%s%s' % (str(self.optpre),str(x),))
      else: call.extend(('%s%s' % (str(self.optpre),str(x),), str(y)))

    # Make the call.
    logging.info(call)
    return subprocess.call(
            call,
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=self.stderr,
           )
