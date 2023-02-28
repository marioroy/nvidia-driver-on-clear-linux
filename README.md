# nvidia-driver-on-clear-linux

An automation **how-to** for installing the NVIDIA proprietary driver on Clear Linux OS.

## Clear Linux OS installation and updates

*Starting fresh? Obtain a recent Clear Linux image, 38300 or later, from the [release archive](https://cdn.download.clearlinux.org/releases/). Currently running < 38270 and updating the OS >= 38270? Please refer to the [community article](https://community.clearlinux.org/t/cl-38270-good-news-the-bad-news-and-solution-for-nvidia-graphics/8466) on getting NVIDIA graphics working again.*

*Using a NVIDIA Optimus laptop? Select the lts kernel in 'Advanced options' and later install the 520 driver. See also, [tip by leiniercs](https://community.clearlinux.org/t/the-nvidia-driver-automation-transitions-to-wayland-era/8499/3).*

Depending on the CL release, the open-source nouveau driver may not work with recent NVIDIA graphics (3000 series or later). The solution is to install the OS in text mode. Press the letter `e` on the boot screen and prepend `nomodeset 3` with a space to the list of kernel arguments. The OS will boot into multi-user mode and prevent the nouveau driver from loading. Press enter to boot the OS. Instructions are provided on the screen for running the installer.

During setup, remember to enter `[A]` Advanced options. Select "Kernel Command Line" and enter `nomodeset 3` to "Add Extra Arguments". Optionally, go back to the prior screen and choose the `lts` (recommended) or `native` kernel under "Kernel Selection". Also disable automatic OS updates if desired.

Before the NVIDIA installation, install OS updates. 

```bash
sudo swupd update
sudo reboot
```

Purge old kernel files, if any. This is something I run after an OS update, but requires the reboot cycle in the prior step or nothing will purge.

```bash
sudo clr-boot-manager update
```

## NVIDIA driver installation

```bash
git clone https://github.com/marioroy/nvidia-driver-on-clear-linux
cd nvidia-driver-on-clear-linux
```

First, run the pre-installer script and reboot the OS. The `update` argument is needed on prior Clear Linux installations to refresh the associated configuration files under `/etc/`. Run the pre-installer script subsequently, without an argument, to switch the boot target to text mode.

```bash
$ bash ./pre-install-driver help
Usage: pre-install-driver [ update ]

$ git pull
$ bash ./pre-install-driver update
$ bash ./pre-install-driver
$ reboot
```

Next, run the driver installer script. Running the LTS kernel? Choose any driver in the list. Planning on running the native kernel or GeForce RTX 4000 series? Specify `525` minimally or latest. Or provide the location of the `NVIDIA-Linux-x86_64-*` run-file. Do not forget to run the `check-kernel-dkms` script. That will check each kernel and involve `dkms` to auto-install the NVIDIA modules, if needed.

| Driver |  Version    |
|--------|-------------|
| latest | 525.89.02   |
|  525   | 525.89.02   |
|  520   | 520.61.05   |
|  515   | 515.86.01   |
|  510   | 510.108.03  |

```bash
$ bash ./install-driver help
Usage: install-driver latest |525|520|515|510| <valid_pathname>

$ bash ./install-driver 525
$ bash ./check-kernel-dkms
$ reboot
```

## NVIDIA CUDA Toolkit installation

Installing the CUDA Toolkit is optional. The "auto" argument is preferred and will install the version suitable for the display driver. If the display driver is not in the table then will fetch the latest CUDA run-file.

| Driver | CUDA Toolkit |
|--------|--------------|
|  525   |    12.0.1    |
|  520   |    11.8.0    |
|  515   |    11.7.1    |
|  510   |    11.6.2    |

```bash
$ bash ./install-cuda help
Usage: install-cuda latest | auto | <valid_pathname>

$ bash ./install-cuda auto    # or path to run file
$ bash ./install-cuda ~/Downloads/cuda_12.0.1_525.85.12_linux.run
```

**Q)** Why specify the auto argument to `install-cuda`?

**A)** This is the preferred choice. Otherwise, using a mismatched CUDA Toolkit installation not suited for the display driver may cause some CUDA programs to emit an error, "the provided PTX was compiled with an unsupported toolchain".

**Q)** What are my options if the `install-cuda` script is no longer current?

**A)** Notifying the author is one option. The other option is to visit the CUDA archive URL, provided at the bottom of the page. Determine the display driver version from the filename. Then visit the driver archive and scroll to the bottom of the page. Click on the latest matching the base version.  Install the driver and CUDA Toolkit by providing the path to `install-driver` and `install-cuda` respectively.

## Enable hardware acceleration

Hardware acceleration requires installing NVDEC/VDPAU back-end VA-API drivers. See the [HWAccel](HWAccel) folder. It provides instructions for building the VA drivers, a configuration file for Firefox, and launch-desktop files for Brave, Chromium-Freeworld, Google Chrome, Microsoft Edge, and Vivaldi.

## Updating the NVIDIA driver

First, ensure you have the latest by running `git pull` followed by `pre-install-driver` with the `update` argument. You may stop here if all you want to do is refresh the NVIDIA-related configuration files from any upstream updates.

```bash
$ git pull
$ bash ./pre-install-driver update
```

The output will be much smaller for `pre-install-driver` without an argument since it will skip completed sections. Run the pre-installer script regardless to switch the boot target to text mode.

Run `install-driver latest` or acquire the run-file from NVIDIA and save it locally. Note: Choosing [latest](https://download.nvidia.com/XFree86/Linux-x86_64/latest.txt) may not always be the latest release.

```bash
$ bash ./pre-install-driver
$ reboot

$ bash ./install-driver latest    # or path to run file
$ bash ./install-driver ~/Downloads/NVIDIA-Linux-x86_64-525.89.02.run
$ reboot
```

Update the CUDA Toolkit, if installed, to install the version suitable for the display driver.

```bash
[ -d /opt/cuda ] && bash ./install-cuda auto
```

## Uninstallation

The NVIDIA software can be uninstalled and nouveau driver restored. Reinstall the NVIDIA driver if the nouveau driver is failing for your graphics (e.g. NVIDIA 3000+ series).

```bash
$ bash ./uninstall-cuda
$ bash ./uninstall-driver
$ reboot
```

## Troubleshooting

Running 6.x kernel? There's an [issue](https://forums.developer.nvidia.com/t/objtool-naked-return-found-in-rethunk-build-when-build-dkms-525-53-in-kernel-6-0-x-gcc12-2-0/234403) installing the NVIDIA driver while running the `native` kernel. Ignore the errors in `/var/log/nvidia-installer.log` if the installation succeeds. Otherwise, you will need to run the `lts` kernel before installation.

Installing a kernel manually or have multiple kernels (LTS and native)? Run `check-kernel-dkms` manually. The script installs missing dkms bundles and runs `dkms autoinstall` per each kernel on the system.

```bash
bash ./check-kernel-dkms
reboot
```

Running a NVIDIA Optimus laptop? See `CONFIGURATION STEPS` or search for `dbus` in `/usr/share/doc/NVIDIA_GLX-1.0/README.txt`. Undo the steps if `nvidia-powerd` reports no matching GPU found. Refer to: [Failure with the nvidia-powerd service](https://www.reddit.com/r/Fedora/comments/sobsgb/anyone_experiencing_failure_with_nvidiapowerd/) and [Video decode does not work after exiting sleep](https://github.com/elFarto/nvidia-vaapi-driver/issues/42).

Experiencing stutter or tearing when moving windows? Lanuch NVIDIA Settings and enable "Force Full Composition Pipeline". See also, [Difference between Force Full Composition Pipeline and Force Composition Pipeline](https://forums.developer.nvidia.com/t/can-someone-really-explain-the-difference-between-force-full-composition-pipeline-and-force-composition-pipeline/49170).

```bash
1. sudo chown $USER /etc/X11  # this is done by the install-driver script
2. Go to NVIDIA Settings > X Server Display Configuration > Advanced...
3. Enable "Force Full Composition Pipeline" per each monitor
4. Click "Apply"
5. Click "Save to X Configuration File" to persist the change
```

Using a HiDPI display? In GNOME, run `gnome-tweaks` and adjust "Scaling Factor" on the Fonts pane. For Wayland, restore `text-scaling-factor` back to 1.0 and enable an experimental feature `scale-monitor-framebuffer`. Log out for the settings to take effect. Go to GNOME settings > Displays and set the scale accordingly, for the display to 100%, 125%, 150%, ... 400%.

```bash
gsettings set org.gnome.desktop.interface text-scaling-factor 1.0
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"
```

Installing KDE? Important, remove the `desktop-autostart` bundle to not autostart GDM resulting in black screen.

```bash
sudo swupd bundle-remove desktop-autostart
sudo swupd bundle-add desktop-kde
sudo swupd bundle-add desktop-kde-apps   # optional
```

## See also

* [Announcement; tips and solutions](https://community.clearlinux.org/t/the-nvidia-driver-automation-transitions-to-wayland-era/8499)
* [CUDA Redistributable Driver Archive](https://developer.download.nvidia.com/compute/cuda/redist/nvidia_driver/linux-x86_64/)
* [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive)
* [NVIDIA Driver Archive](https://download.nvidia.com/XFree86/Linux-x86_64/)

