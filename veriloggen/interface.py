import os
import sys
import collections
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import vtypes

class Interface(vtypes.VeriloggenNode):
    def __init__(self, module, prefix='', postfix='', io=False):
        self.module = module
        self.prefix = prefix
        self.postfix = postfix
        self.io = io

    def Input(self, name, width=1, length=None, signed=False, value=None):
        new_name = self.prefix + name + self.postfix
        return self.module.Input(name, width, length, signed, value)
        
    def Output(self, name, width=1, length=None, signed=False, value=None):
        new_name = self.prefix + name + self.postfix
        return self.module.Output(name, width, length, signed, value)
        
    def OutputReg(self, name, width=1, length=None, signed=False, value=None):
        new_name = self.prefix + name + self.postfix
        return self.module.OutputReg(name, width, length, signed, value)
        
    def Inout(self, name, width=1, length=None, signed=False, value=None):
        new_name = self.prefix + name + self.postfix
        return self.module.Inout(name, width, length, signed, value)
        
    def Reg(self, name, width=1, length=None, signed=False, value=None):
        new_name = self.prefix + name + self.postfix
        return self.module.Reg(name, width, length, signed, value)
        
    def Wire(self, name, width=1, length=None, signed=False, value=None):
        new_name = self.prefix + name + self.postfix
        return self.module.Wire(name, width, length, signed, value)
        
    def Parameter(self, name, value, width=None, signed=False):
        new_name = self.prefix + name + self.postfix
        return self.module.Parameter(name, value, width, signed)
        
    def Localparam(self, name, value, width=None, signed=False):
        new_name = self.prefix + name + self.postfix
        return self.module.Localparam(name, value, width, signed)
        
    def connectAllPorts(self, prefix='', postfix=''):
        inputs = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Input) ]
        outputs = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Output) ]
        inouts = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Inout) ]
        regs = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Reg) ]
        wires = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Wire) ]
        ret = collections.OrderedDict()
        for p in inputs:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        for p in outputs:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        for p in inouts:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        for p in regs:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        for p in wires:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        return ret

    def connectAllParameters(self, prefix='', postfix=''):
        parameters = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Parameter) ]
        localparams = [ s for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Localparam) ]
        ret = collections.OrderedDict()
        for p in parameters:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        for p in localparams:
            name = prefix + re.sub(r'' + self.postfix + '$', '', getattr(self, p).name.replace(self.prefix, '', 1)) + postfix
            ret[name] = getattr(self, p)
        return ret
    
    def getPorts(self):
        return ([ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Input) ] +
                [ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Output) ] +
                [ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Inout) ] +
                [ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Reg) ] +
                [ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Wire) ])
        
    def getParameters(self):
        return ([ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Parameter) ] +
                [ getattr(self, s) for s in self.__dir__() if isinstance(getattr(self, s), vtypes.Localparam) ])