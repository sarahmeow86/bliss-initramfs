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

from pkg.libs.Tools import Tools


class Hook:
    _use = 0
    _use_man = 0
    _files = []
    _optional_files = []
    _directories = []
    _man = []

    @classmethod
    def Enable(cls):
        """Enables this hook."""
        cls._use = 1

    @classmethod
    def Disable(cls):
        """Disables this hook."""
        cls._use = 0

    @classmethod
    def EnableMan(cls):
        """Enables copying the man pages."""
        cls._use_man = 1

    @classmethod
    def DisableMan(cls):
        """Disables copying the man pages."""
        cls._use_man = 0

    @classmethod
    def IsEnabled(cls):
        """Returns whether this hook is activated."""
        return cls._use

    @classmethod
    def IsManEnabled(cls):
        """Returns whether man pages will be copied."""
        return cls._use_man

    @classmethod
    def AddFile(cls, vFile):
        """Adds a required file to the hook to be copied into the initramfs."""
        cls._files.append(vFile)

    @classmethod
    def RemoveFile(cls, vFile):
        """Deletes a required file from the hook."""
        try:
            cls._files.remove(vFile)
        except ValueError:
            Tools.Fail('The file "' + vFile + '" was not found on the list!')

    @classmethod
    def PrintFiles(cls):
        """Prints the required files in this hook."""
        for file in cls.GetFiles():
            print("File: " + file)

    @classmethod
    def GetFiles(cls):
        """Returns the list of required files."""
        return cls._files

    @classmethod
    def GetOptionalFiles(cls):
        """Returns the list of optional files."""
        return cls._optional_files

    @classmethod
    def GetDirectories(cls):
        """Returns the list of required directories."""
        return cls._directories

    @classmethod
    def GetManPages(cls):
        """Returns the list of man page files for this hook."""
        return cls._man
