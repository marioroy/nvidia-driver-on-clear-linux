# hardware-acceleration-using-nvidia-graphics

## Install the (nvdec, vdpau) backend vaapi drivers manually

The manual installation provides more recent VA-API drivers, needed for the NVIDIA v525 display driver.

The build script installs minimum dependencies, builds, and installs the drivers to `/usr/lib64/dri/`. Once installed, hardware acceleration is available to Firefox, Google Chrome, and derivatives.

Run the scripts as a normal user. The scripts call `sudo` to install bundles+packages and run `ldconfig`.

_Note: Chromium has made changes in early 2023 to use DMA-BUF, causing the VDPAU backend VA-API driver to fail. The browser launch scripts were updated to use Vulkan._

```bash
cd HWAccel
bash ./build-all  # builds+installs the vaapi drivers
bash ./clean-all

rpmbuild/RPMS     # preserved, clean manually if desired
```

## Install the "codecs-cuda" bundle on Clear Linux from Clear Fraction

[Clear Fraction](https://clearfraction.cf) introduced the `codecs-cuda` bundle in August 2022. It provides ffmpeg and gstreamer-libav with dependencies, supporting AMD (vaapi, vdpau), Intel (qsv, vaapi), and NVIDIA (nvdec, vaapi, vdpau), also includes the (nvdec, vdpau) backend vaapi drivers.

First, check as one cannot have both `codecs` and `codecs-cuda` installed. Then, proceed with the installation.

```bash
# First time? Add the Clear Fraction repository.
sudo swupd 3rd-party add clearfraction https://download.clearfraction.cf/update

# Check and remove the codecs bundle if installed.
sudo swupd 3rd-party bundle-list | grep codecs
sudo swupd 3rd-party bundle-remove codecs

# Install the codecs-cuda bundle.
sudo swupd 3rd-party bundle-add codecs-cuda
```

Next, run the `pre-install-driver` script if omitted the manual installation above. The `update` argument refreshes various configuration files without switching the boot target mode and includes making symbolic links in `/usr/lib64/dri` for the (nvdec, vdpau) backend vaapi drivers.

```bash
cd nvidia-driver-on-clear-linux
git pull   # important
bash ./pre-install-driver update
```

## Firefox configuration and settings

On Clear Linux, copy the configuration file to your home directory. For NVIDIA graphics, hardware acceleration is handled by the NVDEC VA driver, supporting AV1, VP9, and h264.

```bash
cp firefox/firefox.conf ~/.config/.
```

Or copy the run script and associated desktop file.

```bash
mkdir -p ~/bin
cp bin/run-firefox ~/bin/.
cp desktop/firefox.desktop ~/.local/share/applications/.
rm -f ~/.config/firefox.conf
```

Open Firefox and review settings via the about:config page. Re-launch Firefox when completed.

```text
Required, enables hardware acceleration using VA-API.
media.ffmpeg.vaapi.enabled                     true

Required, enables hardware VA-API decoding support for WebRTC (e.g. Google Meet).
media.navigator.mediadatadecoder_vpx_enabled   true

Required, for HW acceleration to work using NVIDIA 470 series drivers.
widget.dmabuf.force-enabled                    true

Required, leave this setting true to use the internal decoders for VP8/VP9.
media.ffvpx.enabled                            true

Optional, or false if prefer external FFmpeg including LD_LIBRARY_PATH set.
media.ffvpx.enabled                            false

Optional, disables AV1 content; ensure false if graphics lacks support.
media.av1.enabled                              false

---
The rest are defaults or not set and kept here as informative knownledge.

Enable software render if you want to render on the CPU instead of GPU.
Preferably, leave this setting false since webrender on the GPU is needed
to decode videos in hardware.
gfx.webrender.software                         false

Do not add xrender if missing or set to false or click on the trash icon.
This is a legacy setting that shouldn't be used as it disables WebRender.
gfx.xrender.enabled                            false

Ensure false so to be on a supported code path for using WebRender.
layers.acceleration.force-enabled              false

Ensure enabled, default since Firefox 97.
media.rdd-ffmpeg.enabled                       true
media.rdd-process.enabled                      true
```

## Installing Google Chrome and like browsers.

This repo provides complementary launch scripts and desktop files for several browsers. They provide initial customization for enabling hardware acceleration. There's no reason to use them if you prefer to run the browser as is without any flags. Or, copy and further customize them to your taste. The scripts run well-using GNOME on Xorg.

Copying the installer script (upd-) is optional. Simply run the updater from the repo location.

## Brave installation

You can install Brave from the [Clear Fractions](https://clearfraction.cf/) 3rd-party repository or run the provided installer script. The launch script checks the `/opt/brave.com` location, otherwise runs Brave from the 3rd-party path.

All the magic for enabling hardware acceleration is done inside the launch script.

```bash
mkdir -p ~/bin
cp bin/upd-brave-stable ~/bin/.
cp bin/run-brave-stable ~/bin/.
cp desktop/brave-browser.desktop ~/.local/share/applications/.
```

```bash
sudo swupd 3rd-party bundle-add brave  # (or)
~/bin/upd-brave-stable
```

Is the Brave icon blank? Reset the icon path in your .local desktop file. Copy and paste the code block to your terminal and press enter.

```bash
if [ -f "$HOME/.local/share/applications/brave-browser.desktop" ]; then
   if [ -d "/opt/brave.com/brave" ]; then
      sed -i 's!^Icon=.*!Icon=brave-browser!' \
         "$HOME/.local/share/applications/brave-browser.desktop"
   elif [ -d "/opt/3rd-party/bundles/clearfraction/opt/brave.com/brave" ]; then
      sed -i 's!^Icon=.*!Icon=/opt/3rd-party/bundles/clearfraction/opt/brave.com/brave/product_logo_128.png!' \
         "$HOME/.local/share/applications/brave-browser.desktop"
   fi
fi
```

Launch Brave and install the "Not, AV1" extension to disable AV1 as the backend VDPAU driver does not support AV1 content. Optionally, edit `~/bin/run-brave-stable` to adjust the window size.

## Google Chrome installation

How can one not want Google Chrome :) It is glamorously fast.

```bash
mkdir -p ~/bin
cp bin/upd-chrome-stable ~/bin/.
cp bin/run-chrome-stable ~/bin/.
cp desktop/google-chrome.desktop ~/.local/share/applications/.
```

Run the installer script for the initial installation and periodically to update. Using NVIDIA graphics? Like with Brave, install the "Not, AV1" extension to disable AV1. Using Intel graphics? Install the "enhanced-h264ify" extension to block {VP8, VP9, AV1}. Try unblocking AV1 if supported in both the hardware and the backend VA-API driver.

```bash
~/bin/upd-chrome-stable
```

## Chromium-Freeworld installation

You're in for a treat! [RPM Fusion](https://github.com/rpmfusion/chromium-freeworld) provides Chromium built with all Freeworld codecs and VA-API support. The installer script creates a symbolic link to Google's WidevineCmd folder, if installed. Although, Google Chrome is not necessary if you prefer Chromium only. Installing the "Not, AV1" extension enables Chromium to setup Widevine. Check the `~/.config/chromium/WidevineCmd` folder.

```bash
mkdir -p ~/bin
cp bin/upd-chromium-freeworld ~/bin/.
cp bin/run-chromium-freeworld ~/bin/.
cp desktop/chromium-freeworld.desktop ~/.local/share/applications/.
```

Run the installer script for the initial installation and periodically to update. Install the "Not, AV1" or the "enhanced-h264ify" extension, if needed.

```bash
~/bin/upd-chromium-freeworld
```

## Microsoft Edge installation

The [Microsoft Edge](https://www.microsoft.com/en-us/edge?r=1&form=MA13FJ) stable version is finally available on Linux, based on the open source Chromium browser.

```bash
mkdir -p ~/bin
cp bin/upd-edge-stable ~/bin/.
cp bin/run-edge-stable ~/bin/.
cp desktop/microsoft-edge.desktop ~/.local/share/applications/.
```

Run the installer script for the initial installation and periodically to update. Microsoft Edge defaults to playing `VP9` media for NVIDIA graphics.

Is right-clicking problematic or unusual? Go to Settings, Appearance, and scroll down to "Context menus". Disable "Show smart actions" and "Show mini menu when selecting text".

On YouTube, does changing the video quality from 720p to 1080p, 1440p, or 4K stall playback? I experienced this using the NVIDIA v525 display driver. No issues with v520.

## Vivaldi installation

Similar automation was done for the Vivaldi browser.

```bash
mkdir -p ~/bin
cp bin/upd-vivaldi-stable ~/bin/.
cp bin/run-vivaldi-stable ~/bin/.
cp desktop/vivaldi-stable.desktop ~/.local/share/applications/.
```

Run the installer script for the initial installation and periodically to update. Not to forget, install the "Not, AV1" or the "enhanced-h264ify" extension, if needed.

```bash
~/bin/upd-vivaldi-stable
```

### Acknowledgement

Thank you, @paulcarroty. Particularly for enlightenment on the `rpmbuild` command.

Thank you, @xtknight for the initial [VP9](https://github.com/xtknight/vdpau-va-driver-vp9) acceleration bits. Likewise and thank you, @xuanruiqi for the [VP9-update](https://github.com/xuanruiqi/vdpau-va-driver-vp9) to include additional fixes. Finally, thank you @elFarto for the [NVDEC-enabled](https://github.com/elFarto/nvidia-vaapi-driver) driver. Both drivers can co-exist with few tweaks to the installation process.

