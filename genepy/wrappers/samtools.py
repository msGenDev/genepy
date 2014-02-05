import simplewrapper

class Samtools(simplewrapper.SimpleWrapper):
  def __init__(self,exe='samtools',*args,**kwargs):
    super(Samtools,self).__init__(exe,*args,**kwargs)
