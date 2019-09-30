# Project status notice
DesignSPHysics is currently under development and not ready for consumer use. It contains errors, unfinished features and is prompt to change in any moment. Take that into account when posting issues or contributing to the project.

This document was updated at 31 of July, 2018. It is probable that the project has been modified since then and this document does not contain correct information.

# How to contribute
There's 2 main ways to contribute: Opening issues and contributing to the code. Below you can find information about the 2.

## Opening issues
You can open issues in [this github repository](https://github.com/DualSPHysics/DesignSPHysics) to report errors or suggest new features or how to improve them. Keep in mind that there are a lot of things left to do and probably most of the missing features are coming eventually. The most useful feedback right now is error reporting and fixing.

## Contributing to the code
To contribute to the project please check the following section (Project Structure) as it contains a brief description about how the project is structure and where to find the related code for each UI element.

To submit code please make your changes onto the `develop` branch and open a pull request. The current maintainer of the code will check it as soon as possible to merge the change onto the branch.

# Project structure
## Branches
There are currently 2 branches on the repository:
- `master`: This is the branch with "stable" code. It represents the product that should be tested and to where each stable state of the development should merge. Please **do not** use this as the main developing branch as it will always be behind the `develop` branch.
- `develop`: This is the main developing branch. It contains unstable, up-to-date code and it may not even work correctly. Use this branch to start any development (both in this branch or another one rooting from here).

## File structure
This is a brief description on how the project files are structure and what each one contains. It only contains the most relevant files as most of them are brief and self-explanatory.
- `DesignSPHysics.FCMacro`: Macro file designed to use with FreeCAD. It only includes the DesignSPHysics FreeCAD module installed on the system, if there is any.
- `DesignSPHysics.py`: Main code file. From here all the data structures and GUI elements are created. 
- `build-release.*`: Scripts to automate installer creation for release.
- `mod`: DesignSPHysics modules. It contains all the code used by `DesignSPHysics.py`.
    - `lang`: Language files and translations.
    - `templates`: Template files used in DesignSPHysics to create batch files, represent information on screen etc.
    - `widgets.py`: Contains classes extending visual components to use in the interface.
    - `execution_parameters.py`: Contains data classes to structure execution parameters for DualSPHysics
    - `dataobjects.py`: Contains data classes to structure different DualSPHysics properties, parameters and configurations
    - `enums.py`: Contains enums to manage property data with names.
    - `utils.py`: Contains helper functions for all of the DesignSPHysics utilities.
    - `guiutils.py`: Similar to `utils.py` but containing only utilities related with user interface operations.
    - `xmlimporter.py`: Code related with importing existing DualSPHysics cases to DesignSPHysics (uses lib `xmltodict.py`)
- `images`: Images and icons used in the user interface
- `dualsphysics/bin`: DualSPHysics executables.
- `installer`: Installer code.
    - `installer.py`: Main installer file. Defines the installer window and its behaviour
    - `resource`: Resources used by the installer. Mainly images.
    
Each one of the files contains plenty of comments in the code and tries to be easily readable and auto documented. For any doubt about what the code does you can open an issue in the GitHub repository.
    
## Code structure
All the main GUI elements, global data structure and monitor thread are created in the file `DesignSPHysics.py`. Once its execution is finished, all the code is execute as a reaction to a UI component signal.
For example, when the "Load Case" button is pressed, the function binded to it gets executed and, from there, the related code inside it.

To implement a new UI component with a feature just create, for example, a button and a function to execute when pressed.

The main data structure is a Python Dictionary with different data attached to its keys. To see a reference to the structure, check the `get_default_data()` function in `mod.utils`.

# Need more help?
If you need help on how to contribute please contact one of the following people
- Lorena Docasar Vázquez - docasarlorena@gmail.com
- Orlando García Feal - orlando@uvigo.es
- José Manuel Domínguez Alonso - jmdalonso@gmail.com
- Alejandro Jacobo Cabrera Crespo - alexbexe@uvigo.es
