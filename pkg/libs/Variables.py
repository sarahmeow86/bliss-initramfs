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
import subprocess
import sys
import random

"""Defines various variables that are used internally for the application.

   Variables that are meant to be exposed to the user are in settings.json.
"""

# Application Info
name = "Bliss Initramfs"
author = "Jonathan Vasquez"
email = "jon@xyinn.org"
contact = author + " <" + email + ">"
version = "9.4.0"
license = "Simplified BSD License"

# Locations
home = os.getcwd()

# Kernel and Menu Choice
kernel = ""
features = ""
settingsPath = ""
modules = ""
lmodules = ""
initrd = ""

rstring = str(random.randint(100000000, 999999999))

# Temporary directory will now be in 'home' rather than
# in /tmp since people may have executed their /tmp with 'noexec'
# which would cause bliss-initramfs to fail to execute any binaries
# in the temp dir.
temp = home + "/bi-" + rstring

# Directory of Program
phome = os.path.dirname(os.path.realpath(sys.argv[0]))

# Files Directory
filesDirectory = phome + "/files"

# CPU Architecture
arch = subprocess.check_output(["uname", "-m"], universal_newlines=True).strip()

# Layout of the initramfs
baselayout = [
    temp + "/etc",
    temp + "/etc/bash",
    temp + "/etc/zfs",
    temp + "/dev",
    temp + "/proc",
    temp + "/sys",
    temp + "/mnt",
    temp + "/mnt/root",
    temp + "/mnt/key",
    temp + "/lib",
    temp + "/lib/modules",
    temp + "/lib64",
    temp + "/bin",
    temp + "/sbin",
    temp + "/usr",
    temp + "/root",
    temp + "/run",
]

# Temporary Directories (Dynamically Retrieved) since we need
# to first load all of our variables from our settings.json
def GetTempBinDir():
    return temp + bin


def GetTempSbinDir():
    return temp + sbin


def GetTempLibDir():
    return temp + lib


def GetTempLib64Dir():
    return temp + lib64


def GetTempEtcDir():
    return temp + etc
