@echo off
echo "------- Autoexported by DesignSPHysics -------"
echo "This script executes GenCase for the case saved, that generates output files in the *_out dir. Then, executes a simulation on CPU of the case. Last, it exports all the geometry generated in VTK files for viewing with ParaView."
pause
"C:/DualSPHysics/EXECS/GenCase4_win64.exe" C:/Users/ndrs/AppData/Roaming/FreeCAD/Macro/test-examples/float_example/float_example_Def C:/Users/ndrs/AppData/Roaming/FreeCAD/Macro/test-examples/float_example/float_example_out/float_example -save:+all
"C:/DualSPHysics/EXECS/DualSPHysics4_win64.exe" C:/Users/ndrs/AppData/Roaming/FreeCAD/Macro/test-examples/float_example/float_example_out/float_example C:/Users/ndrs/AppData/Roaming/FreeCAD/Macro/test-examples/float_example/float_example_out -svres -cpu
"C:/DualSPHysics/EXECS/PartVTK4_win64.exe" -dirin C:/Users/ndrs/AppData/Roaming/FreeCAD/Macro/test-examples/float_example/float_example_out -savevtk C:/Users/ndrs/AppData/Roaming/FreeCAD/Macro/test-examples/float_example/float_example_out/PartAll
echo "------- Execution complete. If results were not the exepected ones check for errors. Make sure your case has a correct DP specification. -------"
pause
