from PySide2 import QtWidgets
from mod.constants import MKFLUID_LIMIT
from mod.dataobjects.case import Case
from mod.dataobjects.properties.flexstruct import FlexStruct
from mod.dataobjects.motion.base_motion import BaseMotion
from mod.dataobjects.motion.movement import Movement
from mod.enums import ConstModel, ObjectType, MotionType
from mod.tools.translation_tools import __
from mod.widgets.custom_widgets.mk_select_input_with_names import MkSelectInputWithNames
from mod.widgets.custom_widgets.value_input import ValueInput



class FlexStructDialog(QtWidgets.QDialog):
    '''Dialog for flexible structures'''
    def __init__(self, mkbound:int,dataobj:FlexStruct, parent=None):
        super().__init__(parent)
        self.mkbound=mkbound
        if dataobj == None:
            dataobj=FlexStruct(mkbound=mkbound,mkclamp=Case.the().get_first_mk_not_used(object_type=ObjectType.BOUND)-1)
        self.dataobj=dataobj
        self.setWindowTitle("Flexible Structure Configuration")
        self.main_layout=QtWidgets.QVBoxLayout()
        self.flexstruct_mkbound_label=QtWidgets.QLabel(__(f"MkBound : {self.mkbound}"))
        self.flexstruct_enable_checkbox = QtWidgets.QCheckBox(__("Enabled"))


        self.flexstruct_mkclamp_layout = QtWidgets.QHBoxLayout()
        self.flexstruct_mkclamp_label = QtWidgets.QLabel(__("MkClamp"))
        self.flexstruct_mkclamp_input = MkSelectInputWithNames(obj_type=ObjectType.BOUND)
        self.flexstruct_mkclamp_layout.addWidget(self.flexstruct_mkclamp_label)
        self.flexstruct_mkclamp_layout.addWidget(self.flexstruct_mkclamp_input)

        self.flexstruct_density_layout=QtWidgets.QHBoxLayout()
        self.flexstruct_density_label=QtWidgets.QLabel(__("Density"))
        self.flexstruct_density_input = ValueInput()
        self.flexstruct_density_layout.addWidget(self.flexstruct_density_label)
        self.flexstruct_density_layout.addWidget(self.flexstruct_density_input)

        self.flexstruct_young_mod_layout = QtWidgets.QHBoxLayout()
        self.flexstruct_young_mod_label = QtWidgets.QLabel(__("Young's Modulus"))
        self.flexstruct_young_mod_input = ValueInput()
        self.flexstruct_young_mod_layout.addWidget(self.flexstruct_young_mod_label)
        self.flexstruct_young_mod_layout.addWidget(self.flexstruct_young_mod_input)

        self.flexstruct_poisson_ratio_layout = QtWidgets.QHBoxLayout()
        self.flexstruct_poisson_ratio_label = QtWidgets.QLabel(__("Poisson ratio"))
        self.flexstruct_poisson_ratio_input = ValueInput()
        self.flexstruct_poisson_ratio_layout.addWidget(self.flexstruct_poisson_ratio_label)
        self.flexstruct_poisson_ratio_layout.addWidget(self.flexstruct_poisson_ratio_input)

        self.flexstruct_const_model_layout = QtWidgets.QHBoxLayout()
        self.flexstruct_const_model_label = QtWidgets.QLabel(__("Constitutive Model"))
        self.flexstruct_const_model_combo = QtWidgets.QComboBox()
        self.flexstruct_const_model_combo.addItem(ConstModel.PLANESTRAIN.name.lower())
        self.flexstruct_const_model_combo.addItem(ConstModel.PLANESTRESS.name.lower())
        self.flexstruct_const_model_combo.addItem(ConstModel.STVENANTKIRCHOFF.name.lower())
        self.flexstruct_const_model_layout.addWidget(self.flexstruct_const_model_label)
        self.flexstruct_const_model_layout.addWidget(self.flexstruct_const_model_combo)

        self.flexstruct_hg_factor_layout = QtWidgets.QHBoxLayout()
        self.flexstruct_hg_factor_label = QtWidgets.QLabel(__("Hourglass correction factor"))
        self.flexstruct_hg_factor_input = ValueInput()
        self.flexstruct_hg_factor_layout.addWidget(self.flexstruct_hg_factor_label)
        self.flexstruct_hg_factor_layout.addWidget(self.flexstruct_hg_factor_input)

        self.flexstruct_buttons_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton(__("Save"))
        self.cancel_button = QtWidgets.QPushButton(__("Cancel"))
        self.flexstruct_buttons_layout.addWidget(self.ok_button)
        self.flexstruct_buttons_layout.addWidget(self.cancel_button)

        self.main_layout.addWidget(self.flexstruct_mkbound_label)
        self.main_layout.addWidget(self.flexstruct_enable_checkbox)
        self.main_layout.addLayout(self.flexstruct_mkclamp_layout)
        self.main_layout.addLayout(self.flexstruct_density_layout)
        self.main_layout.addLayout(self.flexstruct_young_mod_layout)
        self.main_layout.addLayout(self.flexstruct_poisson_ratio_layout)
        self.main_layout.addLayout(self.flexstruct_const_model_layout)
        self.main_layout.addLayout(self.flexstruct_hg_factor_layout)
        self.main_layout.addLayout(self.flexstruct_buttons_layout)

        self.cancel_button.clicked.connect(self.on_cancel)
        self.ok_button.clicked.connect(self.on_ok)

        self.setLayout(self.main_layout)

        self.fill_values(self.dataobj)

    def on_cancel(self):
        """ Closes the window with a rejection when cancel is pressed. """
        self.reject()

    def on_ok(self):
        const_model:ConstModel=ConstModel.PLANESTRAIN
        if self.flexstruct_const_model_combo.currentIndex()==0:
            const_model=ConstModel.PLANESTRAIN.value
        elif self.flexstruct_const_model_combo.currentIndex()==1:
            const_model=ConstModel.PLANESTRESS.value
        elif self.flexstruct_const_model_combo.currentIndex()==2:
            const_model=ConstModel.STVENANTKIRCHOFF.value

        self.dataobj.density=self.flexstruct_density_input.value()
        self.dataobj.young_mod = self.flexstruct_young_mod_input.value()
        self.dataobj.poisson_ratio = self.flexstruct_poisson_ratio_input.value()
        self.dataobj.const_model=const_model
        self.dataobj.hg_factor = self.flexstruct_hg_factor_input.value()
        self.dataobj.mkclamp=self.flexstruct_mkclamp_input.get_mk_value()

        self.dataobj.enabled=self.flexstruct_enable_checkbox.isChecked()

        #CREATE NULL MOVEMENT FOR MK
        self.mkbasedproperties = Case.the().get_mk_based_properties(self.mkbound + MKFLUID_LIMIT)
        if not self.mkbasedproperties.movements:
            new_movement=Movement("Null movement")
            new_movement.type=MotionType.MOVEMENT
            new_movement.add_motion(BaseMotion())
            self.mkbasedproperties.movements.append(Movement()) #TODO TEST
        self.accept()


    def fill_values(self,dataobj):
        if dataobj.const_model==ConstModel.PLANESTRAIN.value:
            const_model_index=0
        elif dataobj.const_model==ConstModel.PLANESTRESS.value:
            const_model_index = 1
        else:#if dataobj.const_model==ConstModel.STVENANTKIRCHOFF:
            const_model_index = 2
        self.flexstruct_density_input.setValue(dataobj.density)
        self.flexstruct_young_mod_input.setValue(dataobj.young_mod)
        self.flexstruct_poisson_ratio_input.setValue(dataobj.poisson_ratio)
        self.flexstruct_const_model_combo.setCurrentIndex(const_model_index)
        self.flexstruct_hg_factor_input.setValue(dataobj.hg_factor)
        self.flexstruct_mkclamp_input.set_mk_index(dataobj.mkclamp)
        self.flexstruct_enable_checkbox.setChecked(dataobj.enabled)





