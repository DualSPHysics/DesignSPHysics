# Release Notes
The release notes for the DesignSPHysics.

-------------------
## DesignSPHysics v0.7.0 (15-09-2023) 
-Update DualSPHysics binaries from v5.2

-GEO: Keep temporal geometries in FreeCad when it is added to DSPH simulation to avoid duplicated names

-MoorDyn+: Add a new option to define the time step for MoorDyn+

-Show warning when clicking on gencase without previously saving

-WaveGen: Add new files for focused wave generation

-Save: Check the path to save the case and give an error when spaces or special characters are found

-Chrono: Disable the Multi-Core execution using Chrono since it is deprecated in the DualSPHysics-Chrono coupling

-GEO: Store the imported geometry in the case without adding it to the DSPH simulation automatically