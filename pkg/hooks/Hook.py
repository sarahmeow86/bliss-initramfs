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
