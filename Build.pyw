from PyInstaller import __main__ as PyInstall
import shutil
import os

def Build():
    # Version String
    Version = "Dev 47"

    # Build Variables
    ExecutableScript = "PyFifth " + Version + ".pyw"
    ExecutableZip = "Executables/Final/" + ExecutableScript[:-4] + ".zip"
    InstallerScript = "PyFifth " + Version + " Installer.pyw"

    # Build Executable
    PyInstall.run(pyi_args=[ExecutableScript, "--clean", "--windowed", "--name=PyFifth", "--icon=PyFifthIcon.ico", "--add-data=PyFifthIcon.ico;.", "--workpath=./Executables/Build", "--distpath=./Executables/Final"])

    # Zip Executable
    shutil.make_archive(ExecutableZip[:-4], "zip", "Executables/Final/PyFifth")

    # Build Installer
    PyInstall.run(pyi_args=[InstallerScript, "--clean", "--windowed", "--onefile", "--name=PyFifth " + Version + " Installer", "--icon=PyFifthIcon.ico", "--add-data=PyFifthIcon.ico;.",
                            "--add-binary=./" + ExecutableZip + ";./Executables/Final", "--workpath=./Installer/Build", "--distpath=./Installer/Final"])

    # Move Files to Versions Folder
    VersionsSubFolder = os.path.dirname("Versions/PyFifth " + Version + "/")
    if not os.path.exists(VersionsSubFolder):
        os.makedirs(VersionsSubFolder)
    shutil.copy(ExecutableScript, VersionsSubFolder)
    shutil.copy(ExecutableZip, VersionsSubFolder)
    shutil.copy("Installer/Final/PyFifth " + Version + " Installer.exe", VersionsSubFolder)

    # Delete Build Files
    for Folder in ["Executables/", "Installer/"]:
        shutil.rmtree(Folder, True)
    for File in os.listdir("."):
        if File.endswith(".spec"):
            os.unlink(File)

    # Mark Source Files as Built
    os.rename(ExecutableScript, "BUILT " + ExecutableScript)
    os.rename(InstallerScript, "BUILT " + InstallerScript)


if __name__ == "__main__":
    Build()
