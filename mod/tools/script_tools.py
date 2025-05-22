import os
import stat

from mod.dataobjects.case import Case
from mod.dataobjects.configuration.application_settings import ApplicationSettings
from mod.tools.dialog_tools import warning_dialog, info_dialog
from mod.tools.stdout_tools import debug
from mod.tools.template_tools import get_template_text

LINUX_FOLDER = "/templates/scripts/linux/"
WINDOWS_FOLDER = "/templates/scripts/windows/"


def generate_ext_script(toolname, arguments, sufix):
    if not Case.the().path:
        warning_dialog("Case is not saved. You need to save your case first")
        return
    if not ApplicationSettings.the().execs_path:
        warning_dialog(
            "You have not set up a binary folder for external execution. Please set it up in the 'Setup plugin' section")
        return
    lin = ApplicationSettings.the().linux_os
    dir = ApplicationSettings.the().execs_path
    custom_lines = ApplicationSettings.the().custom_script_text
    if sufix:
        sufix = "_" + sufix
    if lin:
        outfile = f"x_{toolname}{sufix}.sh"
        template = f"{toolname}.sh"
        COMMON_SCRIPT_TEMPLATE = LINUX_FOLDER + "common.sh"
        GENCASE_SCRIPT_TEMPLATE = LINUX_FOLDER + template
    else:
        outfile = f"w_{toolname}{sufix}.bat"
        template = f"{toolname}.bat"
        COMMON_SCRIPT_TEMPLATE = WINDOWS_FOLDER + "common.bat"
        GENCASE_SCRIPT_TEMPLATE = WINDOWS_FOLDER + template
    common = get_template_text(COMMON_SCRIPT_TEMPLATE).format(**{"dir": dir,
                                                                 "custom_text": custom_lines})
    script = get_template_text(GENCASE_SCRIPT_TEMPLATE).format(**{"common": common,
                                                                  "args": " ".join(arguments),
                                                                  })
    save_to_disk(f"{Case.the().path}{os.sep}{outfile}", script)
    if lin:
        os.chmod(f"{Case.the().path}/{outfile}", os.stat(f"{Case.the().path}/{outfile}").st_mode | stat.S_IXUSR)
    info_dialog(f"{toolname} script generated successfully")


def save_to_disk(path, text) -> None:
    """ Creates a file on disk with the contents of text """
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
