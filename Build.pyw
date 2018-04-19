from PyInstaller import __main__ as PyInstall
from zipfile import ZipFile
import shutil
import os

# TODO:  Fix zipped file going too deep
# TODO:  Move release files to proper directory
# TODO:  Clean up build files

def Build():
    # Build Variables
    Version = "Dev 42"
    ExecutableScript = "PyFifth " + Version + ".pyw"
    ExecutableZip = "Executables/Final/" + ExecutableScript[:-4] + ".zip"
    InstallerScript = "PyFifth " + Version + " Installer.pyw"

    # Build Executable
    PyInstall.run(pyi_args=[ExecutableScript, "--clean", "--windowed", "--name=PyFifth " + Version, "--icon=PyFifthIcon.ico", "--add-data=PyFifthIcon.ico;.", "--workpath=./Executables/Build", "--distpath=./Executables/Final"])

    # Zip Executable
    with ZipFile(ExecutableZip, mode="w") as ZippedApp:
        # Zip Executable
        for Root, Dirs, Files in os.walk("Executables/Final/PyFifth " + Version):
            for File in Files:
                ZippedApp.write(os.path.join(Root, File))

    # Build Installer
    PyInstall.run(pyi_args=[InstallerScript, "--clean", "--windowed", "--onefile", "--name=PyFifth " + Version + " Installer", "--icon=PyFifthIcon.ico", "--add-data=PyFifthIcon.ico;.", "--add-binary=./" + ExecutableZip + ";./Executables/Final", "--workpath=./Installer/Build", "--distpath=./Installer/Final"])

if __name__ == "__main__":
    Build()