# PyFifth
PyFifth is a suite of apps for playing and running 5E D&D, written in Python 3.12 with PyQT5.  It includes a character sheet, NPC sheet, encounter sheet, hoard sheet, and coin calculator modes.  The character and NPC sheet modes also include a dice roller with the ability to store preset rolls and display messages based on the results of rolls.

## Installation
Because PyFifth is written in 64-bit Python and packaged as an executable zip, a 64-bit Python 3 installation is required to run it.  It was written and tested in Python 3.12, though it may or may not run in other versions of Python 3.

### Windows
On Windows, an appropriate Python installation is included with the release, and does not need to be installed or downloaded separately.

Simply download the .zip file of the latest Windows release from this repository, unzip it wherever you like, and double-click on the `Create Shortcut.bat` file within the app folder.  This will create a shortcut in your Start menu that allows you to run the app.

It is recommended you place the shortcut in `\AppData\Roaming\Microsoft\Windows\Start Menu\Programs` for convenience.  This will cause the shortcut to appear in the Start menu with the correct icon.  More shortcuts can always be made by double-clicking on `Create Shortcut.bat`.

### Linux
On Linux, PyFifth has only been built and tested for Kubuntu 24.04.  It probably runs just fine on many other distros, but you're on your own as far as resolving any problems or differences.

It is generally assumed that you already have 64-bit Python 3 installed as part of your distro.  If your distro has 3.12, you should be fine; otherwise, you may or may not need to install 3.12.

First, download the .zip file of the latest Linux release from this repository, and unzip it wherever you like (probably easiest somewhere in your Home).  To run the app, open a terminal in the app's directory and use the following command:

```
python3 PyFifth.pyzw
```

Alternatively, you can use the included Python interpreter (after giving `Python Interpreter - Linux/bin/python3` executable permissions, if needed):

```
"Python Interpreter - Linux/bin/python3" PyFifth.pyzw
```

However, for convenience, consider running `python3 CreateLinuxDesktopFile.py` or `python3 CreateLinuxDesktopFileForIncludedInterpreter.py` (also in the app's directory; they will not work properly with any other working directory).  This will generate a .desktop file, which will then be moved to `~/.local/share/applications/`.  Now PyFifth should show up along with your other apps in your desktop menus.

If you prefer not to use the included interpreter, consider deleting the `Python Interpreter - Linux` folder to save space.

If PyFifth does not run at first, you probably need to resolve some dependencies.  First, try `sudo apt install libxcb-xinerama0`.  If that doesn't resolve the issue, try installing PyQT5 with `sudo apt install python3-pyqt5`; if this does resolve the issue, you might even be able to (partially) uninstall it with `sudo apt remove python3-pyqt5` and still run PyFifth, as long as you don't autoremove the additional packages that were installed with it.  If installing PyQT5 through APT doesn't work, try installing it through pip; if you don't have pip already, use `sudo apt install python3-pip`, then run `pip3 install pyqt5`.  Other issues have not yet been encountered and will require you to do some research and troubleshooting to resolve on your system.

## Keybindings
Note that, after the first startup of any mode with keyboard shortcuts, there will be a corresponding `Keybindings.cfg` file in the `Configs` folder of the installation directory (for example, `PCKeybindings.cfg`).  This file can be used to alter the keybindings for various actions in the mode.  This is not intended as a feature for regular users, but rather as a workaround in case of conflicts with the user's operating system, so it is not documented thoroughly and there is no user interface provided.  If you want to alter your keybindings, you'll need to know how to format the shortcut string properly in the config file, which you can work out by looking at the existing shortcut strings.  If you format the shortcut improperly, the mode will still run but the action will have no keybinding assigned.

## Gzip Mode
PyFifth saves its files as plain-text JSON by default, but is also capable of using Python's built-in `gzip` module to save and load compressed files.  There is a toggle to enable or disable this mode in the File menu of any mode that can save and open files, and the gzip mode persists between uses of the app and different modes.  When enabled, the save and open dialogs will look for compressed files instead of the default uncompressed files.  The gzip mode is mostly useful if you have a portrait on a player character or NPC with a large file size.  To store images as plain text in JSON, PyFifth converts them to base64, which creates significant storage space overhead, though the gzip compression can offset this quite a lot, and even overcome it entirely.

To save an existing uncompressed file as a compressed file, just open it, turn on gzip mode, and save it.  To save a compressed file as an uncompressed file, just do the reverse, turning gzip mode off.  Gzipped files can also be uncompressed with any archive program that handles `.gz` files, and the resulting file will be a perfectly functional uncompressed file.

It can take noticeably longer to save and open larger files in gzip mode, due to the compression.

## Updates
Updating PyFifth is as simple as deleting all files wherever you installed it *except* the `Configs` folder, and then extracting the contents of the latest release to the installation folder.  Any shortcuts in place should resolve without issue to the updated version.  If you are using the included interpreter, you may have to give it executable permissions after updating.

The `Configs` folder should be left in place as it stores settings and contexts between uses of the app.

## Uninstallation
Uninstalling PyFifth itself only requires deleting the directory you extracted it to, along with any shortcuts you created.

If you need to uninstall Python 3.12 or, on Linux, PyQT5, consult their documentation.

## Licensing
All D&D 5E content referenced in PyFifth is licensed under the OGL Version 1.0a and [Wizards of the Coast's Fan Content Policy](https://company.wizards.com/en/legal/fancontentpolicy).  All other content is covered by the MIT license.
