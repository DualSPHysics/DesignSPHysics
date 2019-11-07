# Contributing
First of all, thank you for contributing to the project! This is becoming a huge project to maintain and improve by only one person, and every bit of help is appreciated.

# Project status notice
DesignSPHysics is currently under development and not ready for consumer use. It contains errors, unfinished features and is prompt to change in any moment. Take that into account when posting issues or contributing to the project.

This document was updated at 07 of November, 2019. It is probable that the project has been modified since then and this document does not contain correct information.

# How to contribute
There's 2 main ways to contribute: Opening issues and contributing to the code. Below you can find information about the 2.

## Opening issues
You can open issues in [this github repository](https://github.com/DualSPHysics/DesignSPHysics/issues) to report errors or suggest new features or how to improve them.

## Contributing to the code
To contribute to the project please check the following section (Project Structure) as it contains a brief description about how the project is structure and where to find the related code for each UI element.

To submit code please make your changes onto the `develop` branch and open a pull request. The current maintainer of the code will check it as soon as possible to merge the change onto the branch.

## Code style and architecture
The repository files include a `pylintrc` file meant to be used with the linter *pylint*. It is advised to follow the gidelines of this linter and try to fix any errors, warnings and suggestions it gives. 

The focus of the code is to be as autodocumented as possible, and easily readable and undesrtandable. Please **do not** include overly abbreviated variables and do not try to skimp in line length. writing a `super_long_variable_but_easy_to_understand` is fine, `ts_crmp` (too_short_and_cramped) variables are definitely not easy to understand. Avoid that.

Also, the codebase is built around an object/class model, trying to avoid single module functions whenever as possible. For now a few of those remain but in the future all of those files should be integrated on static classes. This way, the code is easy to traverse and jump from one structure to another on editors and IDEs.

# Project structure
## Branches
There are currently 2 branches on the repository:
- `master`: This is the branch with "stable" code. It represents the product that should be tested and to where each stable state of the development should merge. Please **do not** use this as the main developing branch as it will always be behind the `develop` branch.
- `develop`: This is the main developing branch. It contains unstable, up-to-date code and it may not even work correctly. Use this branch to start any development (both in this branch or another one rooting from here).

## File structure
This is a brief description on how the project files are structure and what each one contains. It only contains the most relevant files as most of them are brief and self-explanatory.
- `DesignSPHysics.FCMacro`: Macro file designed to use with FreeCAD. It bootstraps the DesignSPHysics application.
- `./mod/main.py`: Main project file. From here all the data structures and GUI elements are created. 
- `mod`: DesignSPHysics modules. It contains all the code used by `DesignSPHysics.py`.
    - `dataobjects`: Contains dataclasses representing the structure of a DesignSPHysics / DualSPHysics case.
    - `lang`: Language files and translations.
    - `templates`: Template files used in DesignSPHysics to create files on disk, create the DualSPHysics XML, represent information on screen etc.
    - `widgets`: Contains Qt classes with the widgets that compose the GUI
    - `xml`: Contains the XML generator files, with its renderers.
    - `constants.py`: Contains useful constants for the application.
    - `enums.py`: Contains the enums used on the application.
    - `*_tools.py`: These files contains little tools related to their name.
- `images`: Images and icons used in the user interface
- `dualsphysics/bin`: DualSPHysics executables.
    
Each one of the files contains plenty of comments in the code and tries to be easily readable and auto documented. For any doubt about what the code does you can open an issue in the GitHub repository.
    
## Code structure
All the main GUI elements, global data structure etc are created in the file `main.py`. Once its execution is finished, all the code is execute as a reaction to a UI component signal.
For example, when the "Load Case" button is pressed, the function binded to it gets executed and, from there, the related code inside it.

To implement a new UI component with a feature just create, for example, a button and a function to execute when pressed.

The main data structure is a singleton data object named `Case`. It can be accessed like `Case.the()` and only one of them can be in memory at a time.

# Need more help?
If you need help on how to contribute please contact one of the following people
- Andrés Vieira Vázquez - anvieiravazquez@gmail.com
- Lorena Docasar Vázquez - docasarlorena@gmail.com
- Orlando García Feal - orlando@uvigo.es
- José Manuel Domínguez Alonso - jmdalonso@gmail.com
- Alejandro Jacobo Cabrera Crespo - alexbexe@uvigo.es
