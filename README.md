## Bliss Initramfs 9.5.0
#### Jonathan Vasquez (fearedbliss)
#### Designed for Gentoo Linux

## Status

This is an actively maintained fork of the original bliss-initramfs project, now with support for:

- Python 3.11+
- Modern subprocess calls
- NVMe module support
- Various improvements and bug fixes

Maintained by [sarahmeow86](https://github.com/sarahmeow86).

The original project by Jonathan Vasquez can be found at [Codeberg](https://codeberg.org/fearedbliss/bliss-initramfs).

## Description

Generates an initramfs image with all files needed to boot your Gentoo Linux
system installed on Encrypted/OpenZFS. This program was designed as a simple
alternative to genkernel for this use case.

## Usage

All you need to do is run the application and pass it the kernel you want
to build the initramfs for. That's it!

`$ ./mkinitrd.py -k $(uname -r)`

## License

Released under the **[Simplified BSD License](LICENSE)**.

## Dependencies

Please have the following installed:

### Required Dependencies

- dev-lang/python 3.11+ (Python 3.11 or newer required)
- sys-apps/busybox (Core utilities)
- app-arch/cpio (For creating the initramfs)
- app-shells/bash (Shell support)
- sys-apps/kmod (`lzma` support required to read compressed kernel modules)
- sys-apps/grep (Text processing)
- app-arch/gzip (Compression)
- sys-fs/zfs (ZFS filesystem support)
- sys-fs/zfs-kmod (ZFS kernel modules)
- sys-fs/udev OR sys-fs/eudev OR sys-apps/systemd (UUIDs, Labels, etc)
- sys-apps/kbd (Keymap support)

### Optional Dependencies

- sys-block/nvme-cli (If using NVMe drives)

### Development Dependencies

- dev-python/poetry (For managing Python dependencies)
- dev-python/black (Code formatting)
- dev-python/beautysh (Shell script formatting)

For more information/instructions check the `USAGE` file.

## Contributions

### Poetry (Virtual Environments & Dependency Management)

You can easily install Poetry on your machine and then run
`poetry install` from the root of this repository to have
poetry automatically create a virtual environment and install
any Python based dependencies for the project (Including all
development dependencies like `black` and `beautysh`).

### Black (Code Formatting - Python)

If making changes to any Python code, make sure to run `black`
on the code. The correct `black` version should have been installed
after having ran `poetry install`.

### Beautysh (Code Formatting - Bash)

If making changes to any bash files (i.e files/init), please run
`beautysh` on that file and re-test your changes. If it still works,
you can submit your PR.
