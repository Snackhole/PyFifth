import os

from Core.Base64Converters import GetBase64StringFromFilePath


if __name__ == "__main__":
    Files = [os.path.join("Assets", File) for File in os.listdir("Assets") if File.endswith(".png") and os.path.basename(File) != "PyFifth Icon.png"]

    Files.sort()

    IconBase64Strings = ""

    for File in Files:
        Base64String = GetBase64StringFromFilePath(File)
        FileLine = f"{os.path.basename(File)}:\n    {Base64String}\n\n"
        IconBase64Strings += FileLine

    IconBase64Strings = IconBase64Strings.rstrip()

    with open("Assets/Icon Base64 Strings.txt", "w") as IconBase64StringsFile:
        IconBase64StringsFile.write(IconBase64Strings)
