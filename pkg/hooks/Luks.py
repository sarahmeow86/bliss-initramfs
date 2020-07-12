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

from pkg.hooks.Hook import Hook


class Luks(Hook):
    @classmethod
    def IsKeyfileEnabled(cls):
        """Returns if we should embed the keyfile into the initramfs."""
        return cls._use_keyfile

    @classmethod
    def GetKeyfilePath(cls):
        """Returns the Keyfile Path."""
        return cls._keyfile_path

    @classmethod
    def IsDetachedHeaderEnabled(cls):
        """Returns if we should embed the LUKS header into the initramfs."""
        return cls._use_detached_header

    @classmethod
    def GetDetachedHeaderPath(cls):
        """Return the LUKS header path."""
        return cls._detached_header_path
