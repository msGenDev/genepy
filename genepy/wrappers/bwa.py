import simplewrapper

class BWA(simplewrapper.SimpleWrapper):
  def __init__(self,exe='bwa',*args,**kwargs):
    super(BWA,self).__init__(exe,*args,**kwargs)
