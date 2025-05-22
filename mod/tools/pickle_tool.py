import pickle
import mod.dataobjects.properties.bound_normals_property as props
import mod.dataobjects.moorings.moordynplus.moordynplus_body as moorbody
import mod.dataobjects.moorings.moordynplus.moordynplus_configuration as moorconf
import mod.dataobjects.moorings.moordynplus.moordynplus_connect as moorconn
import mod.dataobjects.moorings.moordynplus.moordynplus_connect_connection as moorconnc
import mod.dataobjects.moorings.moordynplus.moordynplus_fix_connection as moorfix
import mod.dataobjects.moorings.moordynplus.moordynplus_line as moorline
import mod.dataobjects.moorings.moordynplus.moordynplus_line_default_configuration as moorlinedef
import mod.dataobjects.moorings.moordynplus.moordynplus_output_configuration as moorout
import mod.dataobjects.moorings.moordynplus.moordynplus_solver_options as moorsolv
import mod.dataobjects.moorings.moordynplus.moordynplus_vessel_connection as moorvess

RENAMES = {
    # Old (module, class) → New class
    # properties.bound_normals_property
    ("mod.dataobjects.properties.bound_initials_property", "BoundInitialsProperty"): props.BoundNormals,
    # moorings.moordynplus
    ("mod.dataobjects.moorings.moordyn.moordyn_body", "MoorDynBody"): moorbody.MoorDynPlusBody,
    ("mod.dataobjects.moorings.moordyn.moordyn_configuration", "MoorDynConfiguration"): moorconf.MoorDynPlusConfiguration,
    ("mod.dataobjects.moorings.moordyn.moordyn_connect", "MoorDynConnect"): moorconn.MoorDynPlusConnect,
    ("mod.dataobjects.moorings.moordyn.moordyn_connect_connection", "MoorDynConnectConnection"): moorconnc.MoorDynPlusConnectConnection,
    ("mod.dataobjects.moorings.moordyn.moordyn_fix_connection", "MoorDynFixConnection"): moorfix.MoorDynPlusFixConnection,
    ("mod.dataobjects.moorings.moordyn.moordyn_line", "MoorDynLine"): moorline.MoorDynPlusLine,
    ("mod.dataobjects.moorings.moordyn.moordyn_line_default_configuration", "MoorDynLineDefaultConfiguration"): moorlinedef.MoorDynPlusLineDefaultConfiguration,
    ("mod.dataobjects.moorings.moordyn.moordyn_output_configuration", "MoorDynOutputConfiguration"): moorout.MoorDynPlusOutputConfiguration,
    ("mod.dataobjects.moorings.moordyn.moordyn_solver_options", "MoorDynSolverOptions"): moorsolv.MoorDynPlusSolverOptions,
    ("mod.dataobjects.moorings.moordyn.moordyn_vessel_connection", "MoorDynVesselConnection"): moorvess.MoorDynPlusVesselConnection,
    # Add more mappings if needed
}

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Check if this class needs renaming
        if (module, name) in RENAMES:
            return RENAMES[(module, name)]  # Return the new class directly
        
        # Fallback for other classes
        try:
            return super().find_class(module, name)
        except (ModuleNotFoundError, AttributeError) as e:
            raise pickle.UnpicklingError(f"Failed to load {module}.{name}: {str(e)}")        

