## Creating the initramfs

Run the script by running: `./mkinitrd -k $(uname -r)`

* It must be run as root since root is the only user that can run `depmod`.

* If the script doesn't run and gives you a permission denied message,
  give it execution permission: `chmod +x mkinitrd` and then try again.

After that the required files will be gathered and packed into an initramfs
and you will find the initramfs in the directory that you are currently in.

Copy that file to your boot directory and name it whatever you want.

You can modify the `settings.json` file to change paths of binaries, add modules
that you want to include in the initramfs, or change other settings.


## Setting up the bootloader configuration (GRUB 2)

If the following information is true:

* Kernel     = `vmlinuz-3.9.9-FB.02`
* Initramfs  = `initrd-3.9.9-FB.02`
* Partition Layout is `GPT`
* /boot = `/dev/sda1` (ext2)

Add a new entry to `/boot/grub/grub.cfg`

### Normal ZFS

```
menuentry "Gentoo - 3.9.9-FB.02" {
    linux /vmlinuz-3.9.9-FB.02 root=tank/gentoo/os by=id elevator=noop quiet logo.nologo
    initrd /initrd-3.9.9-FB.02
}
```

### Encrypted ZFS (Passphrase)

```
menuentry "Gentoo - 3.9.9-FB.02" {
    linux /vmlinuz-3.9.9-FB.02 root=tank/gentoo/os encrypted by=id elevator=noop quiet logo.nologo
    initrd /initrd-3.9.9-FB.02
}
```


### Summary

This would load the `vmlinuz-3.9.9-FB.02` kernel and try to mount the
`tank/gentoo/os` dataset as the / of the filesystem. It will then chroot
into it and load your system. If you are using encrypted zfs, then you
will also be asked for your pool's passphrase.


## Kernel Options

### GENERAL

- `root` - Location to rootfs dataset
	+ Example: `linux <kernel> root=tank/gentoo/root`

- `options` - Mount options for the datasets (rootfs and /usr)
	- Example: `linux <kernel> root=tank/gentoo/root options="noatime"`

- `usr` - Location of separate /usr
	- Example: `linux <kernel> root=tank/gentoo/root usr=tank/gentoo/usr`

    - If you use this option, you need to make sure that /usr is on the same type of style as your /. Meaning that if you have / in a zfs dataset, then /usr should be on a zfs dataset as well.

- `recover` - Use this if you want the initrd to throw you into a rescue shell.
      Useful for recovery and debugging purposes.
	- Example: `linux <kernel> recover`

- `su` - Single User Mode. This is a really crappy implementation of a single user,
     mode. But at least it will help you if you forgot to change your password,
     after installation.
	- Example: `linux <kernel> root=tank/gentoo/root su`

- `init` - Specifies the init system to use. If the init system isn't located in /sbin/init,
       you can specific it explicitly:
	- Example: `linux <kernel> root=tank/gentoo/root init=/path/to/init`

### ZFS

- `by` - Specifies what directory you want to use when looking for your zpool so that we can import it.

	Supported Options

     - dev
     - id
     - uuid
     - partuuid
     - label
     - partlabel
     - \* (Wild card will just set the 'by' variable to whatever you specified.)



	Example

	- `by=label` -> /dev/disk/by-label
	- `by=uuid`  -> /dev/disk/by-uuid
	- `by=dev`   -> /dev
	- `by=/mystical/ninja` -> /mystical/ninja

- `refresh` - Ignores the zpool.cache in the rootfs, creates a new one
          inside the initramfs at import, and then copies it into the rootfs.

	- Example: `linux <kernel> root=tank/gentoo/root refresh`

- `encrypted` - Tells the initramfs that you are using encryption. This will ask you for your pool's passphrase.
	+ Example: `linux <kernel> root=tank/gentoo/root encrypted`

## Modules Support

If you have compiled some critical stuff as modules rather than them being
built into the kernel, you can now write which modules you need in the
modules -> files section in `settings.json`. The initramfs will gather the
module and it's dependencies and put them in the initramfs for you. Then the
initramfs will automatically load all those modules for you at boot.

- Example:
    `"files": ["i915", "zfs", "ahci", "ext2", "ext3", "ext4",
              "ohci-hcd", "ehci-hcd", "xhci-hcd", "usb-storage"]`

That example basically loads the intel i915 gfx driver, zfs, ahci, ext2-4
filesystem hdd drivers, ohci/ehci/xhci usb 1.1,2.0,3.0 drivers and the
usb-storage driver. All the dependencies are automatically gathered and
compressed by the initramfs, and automatically loaded at boot in that order.

## Firmware Support

If you want to include firmware in your initramfs, open up your `settings.json`,
and enable the hook by changing the "use" to 1 in the "firmware" section.

You can then add the specific firmware name/path to the files list.

If you want to copy all firmware that's included in a particular directory
under the "/lib/firmware" folder (Or whatever "firmwareDirectory" is set to),
then you can add the names of each directory you want included in the
"directories" variable. Do not add any slashes in the beginning or ending
of this, only the directory name that's in the root directory of the firmware
folder is needed. (Example: `"directories": ["intel", "i915", "ath10k"]`).

If you don't want to specify a specific firmware files/folders, but would
rather copy all the firmware that's on your system, you can toggle the
"copyAll" setting by changing it to 1. The firmware files will be copied
from your system's /lib/firmware directory (Which can be modified in the
"firmwareDirectory" setting). The firmware that you add to the "files"
list should be relative to this directory.

## Excluding Udev Files

bliss-initramfs copies all of the files in both of your udev configuration
directories (i.e `/lib/udev` and `/etc/udev`), however, sometimes there are
files in there that can cause delays if they exist during early boot.
For example, on my machine if I have laptop-mode-tools installed, the
`lmt-udev auto` udev related files would kick in and cause a delay of over
2 minutes. For these files, we can add the file path relative to the
corresponding directory in the appropriate section in settings.json.

If I wanted to exclude the `/lib/udev/rules.d/78-sound-card.rules`, I would add
`rules.d/78-sound-card.rules` to the `udev -> lib -> excludedFiles` section.
