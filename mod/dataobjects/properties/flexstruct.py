from mod.enums import ConstModel


class FlexStruct:

    def __init__(self,mkbound:int,mkclamp:int,density:float=1000,young_mod:float=3.5e6,poisson_ratio:float=0.49,
                 const_model:ConstModel=ConstModel.PLANESTRAIN,hg_factor:float=0.1):
        self.enabled:bool=False
        self.mkbound=mkbound
        self.mkclamp=mkclamp
        self.density=density
        self.young_mod=young_mod
        self.poisson_ratio=poisson_ratio
        self.const_model=const_model
        self.hg_factor=hg_factor
