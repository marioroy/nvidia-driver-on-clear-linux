# hardware-acceleration-using-nvidia-graphics

## Install the "codecs-cuda" bundle from Clear Fraction

[Clear Fraction](https://clearfraction.cf) introduced the `codecs-cuda` bundle in August 2022. It provides ffmpeg and gstreamer-libav with dependencies, supporting AMD (vaapi, vdpau), Intel (qsv, vaapi), and NVIDIA (nvdec, vaapi, vdpau). It also includes the (nvdec, vdpau) backend vaapi drivers. Note: The vdpau backend VA-API driver no longer works since Chrome 110.

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

Next, run the `pre-install-driver` script. The `update` argument refreshes various configuration files without switching the boot target mode and includes making symbolic links in `/usr/lib64/dri` for the (nvdec, vdpau) backend VA-API drivers.

```bash
cd nvidia-driver-on-clear-linux
git pull   # important
bash ./pre-install-driver update
```

## Firefox configuration and settings

Copy the configuration file to your home directory. For NVIDIA graphics, hardware acceleration is handled by the NVDEC VA driver, supporting AV1, VP9, and h264.

```bash
cp firefox/firefox.conf ~/.config/.
```

Open Firefox and review settings via the about:config page. Re-launch Firefox when completed.

```text
Required, enables hardware acceleration using VA-API.
media.ffmpeg.vaapi.enabled                     true

Required, enables hardware VA-API decoding support for WebRTC (e.g. Google Meet).
media.navigator.mediadatadecoder_vpx_enabled   true

Required, for HW acceleration to work using NVIDIA driver 470 (or newer series).
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

