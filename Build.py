import os
import shutil
import zipapp

# Build Variables
Version = "Dev 55"
AppName = "PyFifth"
VersionedAppName = AppName + " " + Version

CodeFiles = ["Build.py", "PyFifth.py", "__main__.py"]
AssetFiles = ["Assets"]

ExecutableZipName = AppName + ".pyzw"
Interpreter = "python3"


def Build():
    # Additional Build Variables
    BuildFolder = "BUILD - " + VersionedAppName

    # Build Functions
    def CopyFilesToBuildFolder(CopiedFiles):
        IgnoredFiles = [File for File in os.listdir(".") if File not in CopiedFiles]
        shutil.copytree(".", BuildFolder, ignore=lambda Source, Contents: IgnoredFiles)

    def CleanUp():
        shutil.rmtree(BuildFolder)
        print("Build files cleaned up.")

    # Copy Code to Build Folder
    CopyFilesToBuildFolder(CodeFiles)
    print("Code files copied to build folder.")

    # Create Executable Archive
    zipapp.create_archive(BuildFolder, ExecutableZipName, Interpreter)
    print("Executable archive created.")

    # Delete Build Folder
    shutil.rmtree(BuildFolder)
    print("Build folder deleted.")

    # Copy Assets to Build Folder and Move Executable Zip
    CopyFilesToBuildFolder(AssetFiles)
    print("Assets copied to build folder.")
    shutil.move(ExecutableZipName, BuildFolder)
    print("Executable archive moved to build folder.")

    # Zip Build
    shutil.make_archive(VersionedAppName, "zip", BuildFolder)
    print("Build zipped.")

    # Clean Up
    CleanUp()


if __name__ == "__main__":
    Build()
