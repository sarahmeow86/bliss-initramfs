# Copyright © 2012-2022 Jonathan Vasquez <jon@xyinn.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import os
import json
import argparse

import pkg.libs.Variables as var

from subprocess import call
from subprocess import check_output


class Tools:
    """Contains various tools/utilities that are used throughout the app."""

    # Checks parameters and running user
    @classmethod
    def ProcessArguments(cls, Modules):
        user = Tools.Run("whoami")[0]

        if user != "root":
            cls.Fail("This program must be ran as root")

        parser = argparse.ArgumentParser(
            description="Builds an initramfs for booting from Encrypted/OpenZFS."
        )
        parser.add_argument(
            "-c",
            "--config",
            help="Path to the settings.json. (i.e: /home/jon/settings.json)",
        )
        parser.add_argument(
            "-k",
            "--kernel",
            required=True,
            help="The name of the kernel you are building the initramfs for. (i.e: 4.14.170-FC.01)",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s {}".format(var.version),
            help="Displays the version of this application.",
        )

        args = parser.parse_args()

        if args.config:
            var.settingsPath = args.config

        if args.kernel:
            var.kernel = args.kernel

    @classmethod
    def PrintHeader(cls):
        """Prints the header of the application."""
        print("-" * 30)
        Tools.Print(
            Tools.Colorize("yellow", var.name)
            + " - "
            + Tools.Colorize("pink", "v" + var.version)
        )
        Tools.Print(var.contact)
        Tools.Print(var.license)
        print("-" * 30 + "\n")

    @classmethod
    def GetProgramPath(cls, vProg):
        """Finds the path to a program on the system."""
        cmd = "whereis " + vProg + ' | cut -d " " -f 2'
        results = check_output(cmd, shell=True, universal_newlines=True).strip()

        if results:
            return results
        else:
            cls.Fail("The " + vProg + " program could not be found!")

    @classmethod
    def Clean(cls):
        """Check to see if the temporary directory exists, if it does,
           delete it for a fresh start.
        """
        # Go back to the original working directory so that we are
        # completely sure that there will be no inteference cleaning up.
        os.chdir(var.home)

        # Removes the temporary directory
        if os.path.exists(var.temp):
            Tools.RemoveTree(var.temp)

            if os.path.exists(var.temp):
                cls.Warn("Failed to delete the " + var.temp + " directory. Exiting.")
                quit(1)

    @classmethod
    def CleanAndExit(cls, vInitrd):
        """Clean up and exit after a successful build."""
        cls.Clean()
        cls.Info('Please copy "' + vInitrd + '" to your ' + "/boot directory")
        quit()

    @classmethod
    def Into(cls, vFile, **optionalArgs):
        """ Intelligently copies the file _into_ the initramfs

            Optional Args:
               directoryPrefix = Prefix that we should add when constructing the file path
               dontFail = If the file wasn't able to be copied, do not fail.
        """
        # If a prefix was passed into the function as an optional argument
        # it will be used below.
        directoryPrefix = optionalArgs.get("directoryPrefix", None)

        # Check to see if a file with this name exists before copying,
        # if it exists, delete it, then copy. If a directory, create the directory
        # before copying.
        if directoryPrefix:
            path = var.temp + "/" + directoryPrefix + "/" + vFile
            targetFile = directoryPrefix + "/" + vFile
        else:
            path = var.temp + "/" + vFile
            targetFile = vFile

        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
                Tools.Copy(targetFile, path)
        else:
            if os.path.isfile(targetFile):
                # Make sure that the directory that this file wants to be in
                # exists, if not then create it.
                if os.path.isdir(os.path.dirname(path)):
                    Tools.Copy(targetFile, path)
                else:
                    os.makedirs(os.path.dirname(path))
                    Tools.Copy(targetFile, path)
            elif os.path.isdir(targetFile):
                os.makedirs(path)

        # Finally lets make sure that the file was copied to its destination (unless declared otherwise)
        if not os.path.isfile(path):
            message = "Unable to copy " + targetFile

            if optionalArgs.get("dontFail", False):
                cls.Warn(message)
            else:
                cls.Fail(message)

    @classmethod
    def SafeCopy(cls, sourceFile, targetDest, *desiredName):
        """Copies a file to a target path and checks to see that it exists."""
        if len(desiredName) == 0:
            splitResults = sourceFile.split("/")
            lastPosition = len(splitResults)
            sourceFileName = splitResults[lastPosition - 1]
        else:
            sourceFileName = desiredName[0]

        targetFile = targetDest + "/" + sourceFileName

        if os.path.exists(sourceFile):
            Tools.Copy(sourceFile, targetFile)

            if not os.path.isfile(targetFile):
                Tools.Fail('Error creating the "' + sourceFileName + '" file. Exiting.')
        else:
            Tools.Fail("The source file doesn't exist: " + sourceFile)

    @classmethod
    def Copy(cls, source, target, recursive=False):
        # https://github.com/fearedbliss/bliss-initramfs/issues/32
        # Using 'shutil.[copytree,copy and possibly rmtree] causes
        # issues in Bedrock Linux where it seems they are using FUSE
        # in interesting ways to separate different "stratas". Regardless,
        # shutil seems to be behaving weird in these cases and throwing
        # exceptions. Switching these implementations to the regular
        # UNIX shell commands that can work in these environments and maintain
        # expected UNIX behavior.
        if not os.path.exists(source):
            Tools.Fail(
                "Copy: The following file/directory doesn't exist: {}".format(source)
            )

        cmd = "cp "

        if recursive:
            cmd += "-r "

        # Try and account for spaces
        cmd += '"' + source + '" "' + target + '"'
        result = call(cmd, shell=True)
        if result != 0:
            Tools.Fail(
                "An error occurred while copying {} to {}. Debug: recursive = {}".format(
                    source, target, recursive
                )
            )

    @classmethod
    def Remove(cls, target, recursive=False):
        if not os.path.exists(target):
            Tools.Fail(
                "Remove: The following file/directory doesn't exist: {}".format(target)
            )

        cmd = "rm "

        if recursive:
            cmd += "-r "

        # Try and account for spaces
        cmd += '"' + target + '"'
        result = call(cmd, shell=True)

        if result != 0:
            Tools.Fail(
                "An error occurred while removing {}. Debug: recursive = {}".format(
                    target, recursive
                )
            )

    @classmethod
    def RemoveTree(cls, target):
        Tools.Remove(target, True)

    @classmethod
    def CopyTree(cls, source, target):
        Tools.Copy(source, target, True)

    @classmethod
    def CopyConfigOrWarn(cls, targetConfig):
        """Copies and verifies that a configuration file exists, and if not,
           warns the user that the default settings will be used.
        """
        if os.path.isfile(targetConfig):
            Tools.Flag("Copying " + targetConfig + " from the current system...")
            Tools.Into(targetConfig)
        else:
            Tools.Warn(
                targetConfig
                + " was not detected on this system. The default settings will be used."
            )

    @classmethod
    def Run(cls, command):
        """Runs a shell command and returns its output."""
        try:
            return (
                check_output(command, universal_newlines=True, shell=True)
                .strip()
                .split("\n")
            )
        except:
            Tools.Fail(
                "An error occurred while processing the following command: " + command
            )

    @classmethod
    def LoadSettings(cls):
        """Loads the settings.json file and returns it."""
        settingsFile = (
            var.settingsPath
            if var.settingsPath
            else "/etc/bliss-initramfs/settings.json"
        )

        if not os.path.exists(settingsFile):
            fallbackSettingsFile = os.path.join(
                var.filesDirectory, "default-settings.json"
            )
            Tools.Warn("Configuration File Missing: {}".format(settingsFile))
            Tools.Warn("Defaulting To: {}\n".format(fallbackSettingsFile))
            settingsFile = fallbackSettingsFile

            if not os.path.exists(settingsFile):
                Tools.Fail(
                    "Backup Configuration File Missing: {}. Exiting.".format(
                        settingsFile
                    )
                )

        with open(settingsFile) as settings:
            return json.load(settings)

    ####### Message Functions #######

    @classmethod
    def Colorize(cls, vColor, vMessage):
        """Returns the string with a color to be used in bash."""
        if vColor == "red":
            coloredMessage = "\033[1;31m" + vMessage + "\033[0;m"
        elif vColor == "yellow":
            coloredMessage = "\033[1;33m" + vMessage + "\033[0;m"
        elif vColor == "green":
            coloredMessage = "\033[1;32m" + vMessage + "\033[0;m"
        elif vColor == "cyan":
            coloredMessage = "\033[1;36m" + vMessage + "\033[0;m"
        elif vColor == "purple":
            coloredMessage = "\033[1;34m" + vMessage + "\033[0;m"
        elif vColor == "white":
            coloredMessage = "\033[1;37m" + vMessage + "\033[0;m"
        elif vColor == "pink":
            coloredMessage = "\033[1;35m" + vMessage + "\033[0;m"
        elif vColor == "none":
            coloredMessage = vMessage

        return coloredMessage

    @classmethod
    def Print(cls, vMessage):
        """Prints a message through the shell."""
        call(["echo", "-e", vMessage])

    @classmethod
    def Info(cls, vMessage):
        """Used for displaying information."""
        call(["echo", "-e", cls.Colorize("green", "[*] ") + vMessage])

    @classmethod
    def Question(cls, vQuestion):
        """ Used for input (questions)."""
        return input(vQuestion)

    @classmethod
    def Warn(cls, vMessage):
        """Used for warnings."""
        call(["echo", "-e", cls.Colorize("yellow", "[!] ") + vMessage])

    @classmethod
    def Flag(cls, vFlag):
        """Used for flags."""
        call(["echo", "-e", cls.Colorize("purple", "[+] ") + vFlag])

    @classmethod
    def Option(cls, vOption):
        """Used for options."""
        call(["echo", "-e", cls.Colorize("cyan", "[>] ") + vOption])

    @classmethod
    def Fail(cls, vMessage):
        """Used for errors."""
        cls.Print(cls.Colorize("red", "[#] ") + vMessage)
        cls.NewLine()
        cls.Clean()
        quit(1)

    @classmethod
    def NewLine(cls):
        """Prints empty line."""
        print("")

    @classmethod
    def BinaryDoesntExist(cls, vMessage):
        """Error Function: Binary doesn't exist."""
        cls.Fail("Binary: " + vMessage + " doesn't exist. Exiting.")

    @classmethod
    def ModuleDoesntExist(cls, vMessage):
        """Error Function: Module doesn't exist."""
        cls.Fail("Module: " + vMessage + " doesn't exist. Exiting.")
