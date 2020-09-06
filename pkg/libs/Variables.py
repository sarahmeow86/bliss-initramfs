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
version = "9.3.0"
license = "Apache License 2.0"

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
