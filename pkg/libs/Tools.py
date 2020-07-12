# Copyright (C) 2012-2020 Jonathan Vasquez <jon@xyinn.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import json
import argparse

import pkg.libs.Variables as var

from subprocess import call
from subprocess import check_output


class Tools:
    """Contains various tools/utilities that are used throughout the app."""

    # Available Features
    _features = {1: "ZFS", 2: "LUKS", 3: "Basic"}

    # Checks parameters and running user
    @classmethod
    def ProcessArguments(cls, Modules):
        user = Tools.Run("whoami")[0]

        if user != "root":
            cls.Fail("This program must be ran as root")

        parser = argparse.ArgumentParser(
            description="Builds an initramfs for booting from OpenZFS."
        )
        parser.add_argument(
            "-c",
            "--config",
            help="Path to the settings.json. (i.e: /home/jon/settings.json)",
        )
        parser.add_argument(
            "-f",
            "--features",
            help="Comma delimited list of features you want [Available: zfs, luks, basic]. (i.e: zfs,luks)",
        )
        parser.add_argument(
            "-k",
            "--kernel",
            help="The name of the kernel you are building the initramfs for. (i.e: 4.14.170-FC.01)",
        )

        args = parser.parse_args()

        if args.config:
            var.settingsPath = args.config

        if args.kernel:
            var.kernel = args.kernel

        if args.features:
            var.features = args.features

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
    def PrintFeatures(cls):
        """Prints the available options."""
        cls.NewLine()

        for feature in cls._features:
            cls.Option(str(feature) + ". " + cls._features[feature])

        cls.NewLine()

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
            shutil.rmtree(var.temp)

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
    def Copy(cls, vFile, **optionalArgs):
        """ Intelligently copies the file into the initramfs

            Optional Args:
               directoryPrefix = Prefix that we should add when constructing the file path
               dontFail = If the file wasn't able to be copied, do not fail.
        """
        # NOTE: shutil.copy will dereference all symlinks before copying.

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
                shutil.copy(targetFile, path)
        else:
            if os.path.isfile(targetFile):
                # Make sure that the directory that this file wants to be in
                # exists, if not then create it.
                if os.path.isdir(os.path.dirname(path)):
                    shutil.copy(targetFile, path)
                else:
                    os.makedirs(os.path.dirname(path))
                    shutil.copy(targetFile, path)
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
            shutil.copy(sourceFile, targetFile)

            if not os.path.isfile(targetFile):
                Tools.Fail('Error creating the "' + sourceFileName + '" file. Exiting.')
        else:
            Tools.Fail("The source file doesn't exist: " + sourceFile)

    @classmethod
    def CopyConfigOrWarn(cls, targetConfig):
        """Copies and verifies that a configuration file exists, and if not,
           warns the user that the default settings will be used.
        """
        if os.path.isfile(targetConfig):
            Tools.Flag("Copying " + targetConfig + " from the current system...")
            Tools.Copy(targetConfig)
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
                "An error occured while processing the following command: " + command
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
            Tools.Fail(settingsFile + " doesn't exist.")

        with open(settingsFile) as settings:
            return json.load(settings)

    ####### Message Functions #######

    @classmethod
    def Colorize(cls, vColor, vMessage):
        """Returns the string with a color to be used in bash."""
        if vColor == "red":
            coloredMessage = "\e[1;31m" + vMessage + "\e[0;m"
        elif vColor == "yellow":
            coloredMessage = "\e[1;33m" + vMessage + "\e[0;m"
        elif vColor == "green":
            coloredMessage = "\e[1;32m" + vMessage + "\e[0;m"
        elif vColor == "cyan":
            coloredMessage = "\e[1;36m" + vMessage + "\e[0;m"
        elif vColor == "purple":
            coloredMessage = "\e[1;34m" + vMessage + "\e[0;m"
        elif vColor == "white":
            coloredMessage = "\e[1;37m" + vMessage + "\e[0;m"
        elif vColor == "pink":
            coloredMessage = "\e[1;35m" + vMessage + "\e[0;m"
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
        """Used for flags (aka using zfs, luks, etc)."""
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
