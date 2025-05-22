# Release Notes
The release notes for the DesignSPHysics.

-------------------
## DesignSPHysics v0.8.0 (16-05-2025) 
* Update DualSPHysics binaries from v5.4
* Implementation of the novelties on DualSPHysics
* VRes: support for Variable Resolution feature
* FlexStruc: Support for Flexible structures
* Gauges system
* Particle Output Filters
* mDBC normals from geometry
* Advanced Drawing Mode
* Motion from path file
* Helper object to show position size and orientation of Inlet zones, Variable Resolution Zones, Gauges,Particle Filters and FlowTool Boxes
* Script generation for Windows and Linux
* Importing of .vtm and .vtu files
* Compatibility with DesignSPHysics v0.7.0

-------------------
## DesignSPHysics v0.7.0 (15-09-2023) 
* Update DualSPHysics binaries from v5.2
* GEO: Keep temporal geometries in FreeCad when it is added to DSPH simulation to avoid duplicated names
* MoorDynPlus: Add a new option to define the time step for MoorDynPlus
* Show warning when clicking on gencase without previously saving
* WaveGen: Add new files for focused wave generation
* Save: Check the path to save the case and give an error when spaces or special characters are found
* Chrono: Disable the Multi-Core execution using Chrono since it is deprecated in the DualSPHysics-Chrono coupling
* GEO: Store the imported geometry in the case without adding it to the DSPH simulation automatically
