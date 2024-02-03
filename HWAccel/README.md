# hardware-acceleration-using-nvidia-graphics

## NVIDIA backend VA-API driver installation

The build script installs minimum dependencies, builds, and installs the driver to `/usr/lib64/dri/`. Run the build and clean scripts as a normal user.

```bash
cd HWAccel
bash ./build-all  # Builds and installs the NVIDIA VA-API driver.
bash ./clean-all

# rpmbuild/RPMS   # Folder preserved, clean manually if desired.
```

## Firefox configuration and settings

Copy the configuration file to your home directory. For NVIDIA graphics, hardware acceleration is handled by the NVIDIA VA-API driver, supporting AV1, VP9 and h264.

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

Optional, disables AV1 content; ensure false if your GPU lacks AV1 support.
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

