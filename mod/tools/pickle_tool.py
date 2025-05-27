import sys
import pickle
class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        import mod.dataobjects.properties.bound_normals_property as props
        import mod.dataobjects.properties.initials_property as iniprop
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
        import mod.dataobjects.configuration.execution_parameters as execparam
        import mod.dataobjects.configuration.domain_fixed_parameter as dfixedparam
        import mod.dataobjects.properties.simulation_object as sobject
        import mod.dataobjects.properties.mk_based_properties as mkprop
        import mod.dataobjects.motion.awas as awas
        import mod.dataobjects.motion.awas_correction as awascorr
        import mod.dataobjects.properties.float_property as floatprop
        import mod.dataobjects.configuration.periodicity as peri
        import mod.dataobjects.configuration.periodicity_info as perinfo
        import mod.dataobjects.configuration.simulation_domain as sdomain
        import mod.dataobjects.configuration.sd_position_property as sdposprop
        import mod.dataobjects.configuration.executable_paths as execpath
        import mod.dataobjects.configuration.application_settings as appset
        import mod.dataobjects.configuration.constants as ctes
        import mod.dataobjects.acceleration_input.acceleration_input as accein
        import mod.dataobjects.acceleration_input.acceleration_input_data as acceindata
        import mod.dataobjects.properties.faces_property as facespro

        # For Modules
        # MODULE_REDIRECTS = {
        #     # Old module → New module
        #     'mod.dataobjects.constants': 'mod.constants',  
        #     # Add more module redirects if needed
        # }

        # For Classes
        RENAMES = {
            # Old (module, class) → New class
            # properties.bound_normals_property
            ("mod.dataobjects.bound_initials_property", "BoundInitialsProperty"): props.BoundNormals,
            ("mod.dataobjects.initials_property", "InitialsProperty"): iniprop.InitialsProperty,
            ("mod.dataobjects.properties.bound_initials_property", "BoundInitialsProperty"): props.BoundNormals,
            ("mod.dataobjects.properties.initials_property", "InitialsProperty"): iniprop.InitialsProperty,
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
            ("mod.dataobjects.execution_parameters", "ExecutionParameters"): execparam.ExecutionParameters,
            ("mod.dataobjects.domain_fixed_parameter", "DomainFixedParameter"): dfixedparam.DomainFixedParameter,
            ("mod.dataobjects.simulation_object", "SimulationObject"): sobject.SimulationObject,
            ("mod.dataobjects.mk_based_properties", "MKBasedProperties"): mkprop.MKBasedProperties,
            ("mod.dataobjects.awas", "AWAS"): awas.AWAS,
            ("mod.dataobjects.awas_correction", "AWASCorrection"): awascorr.AWASCorrection,
            ("mod.dataobjects.float_property", "FloatProperty"): floatprop.FloatProperty,
            ("mod.dataobjects.periodicity", "Periodicity"): peri.Periodicity,
            ("mod.dataobjects.periodicity_info", "PeriodicityInfo"): perinfo.PeriodicityInfo,
            ("mod.dataobjects.simulation_domain", "SimulationDomain"): sdomain.SimulationDomain,
            ("mod.dataobjects.sd_position_property", "SDPositionProperty"): sdposprop.SDPositionProperty,
            ("mod.dataobjects.application_settings", "ApplicationSettings"): appset.ApplicationSettings,
            ("mod.dataobjects.constants", "Constants"): ctes.Constants,
            ("mod.dataobjects.executable_paths", "ExecutablePaths"): execpath.ExecutablePaths,
            ("mod.dataobjects.acceleration_input", "AccelerationInput"): accein.AccelerationInput,
            ("mod.dataobjects.acceleration_input_data", "AccelerationInputData"): acceindata.AccelerationInputData,
            ("mod.dataobjects.faces_property", "FacesProperty"): facespro.FacesProperty,
            # Add more mappings if needed
        }

        # # First check if the module needs redirecting
        # if module in MODULE_REDIRECTS:
        #     module = MODULE_REDIRECTS[module]

        # Check if this class needs renaming
        if (module, name) in RENAMES:
            return RENAMES[(module, name)]  # Return the new class directly
        
        # Fallback for other classes
        try:
            return super().find_class(module, name)
        except (ModuleNotFoundError, AttributeError) as e:
            raise pickle.UnpicklingError(f"Failed to load {module}.{name}: {str(e)}")        
