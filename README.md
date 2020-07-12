## Bliss Initramfs 8.1.0
#### Jonathan Vasquez (fearedbliss)
#### Designed for Gentoo Linux

## Description

An utility that generates an initramfs image with all files and dependencies
needed to boot your Gentoo Linux system installed on OpenZFS. This program was
designed as a simple alternative to genkernel for this use case.

## Usage

All you need to do is run the utility, select the options you want "a-la-carte",
and then tell the initramfs via your bootloader parameters in what order you
want those features to be trigered in. Check the USAGE file for examples.

## License

Released under the Apache License 2.0

## Dependencies

Please have the following installed:

### Required Dependencies
- dev-lang/python 3.6+
- app-arch/cpio
- app-shells/bash
- sys-apps/kmod
- sys-apps/grep
- app-arch/gzip (initramfs compression)
- sys-fs/zfs (ZFS support)
- sys-fs/udev OR sys-fs/eudev OR sys-apps/systemd (UUIDs, Labels, etc)
- sys-apps/kbd (Keymap support)

### Only required if you need encryption
- sys-fs/cryptsetup (LUKS support)
- app-crypt/gnupg (GPG Encrypted Keyfile used for LUKS)

For more information/instructions check the USAGE file.

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

## Beautysh (Code Formatting - Bash)

If making changes to any bash files (i.e files/init), please run
`beautysh` on that file and re-test your changes. If it still works,
you can submit your PR.
