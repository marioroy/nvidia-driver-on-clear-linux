
February 1, 2024

## ERROR: modpost: GPL-incompatible module nvidia.ko uses GPL-only symbol `__rcu_read_lock`

"linux-6.1.76, 6.6.15 and 6.7.3 have modified the non-ARCH-specific
`pfn_valid()` to use `__rcu_read_lock/unlock` that is marked GPL and
cannot be used unless use the open source variant."

[NVIDIA issue report](https://forums.developer.nvidia.com/t/linux-6-7-3-545-29-06-550-40-07-error-modpost-gpl-incompatible-module-nvidia-ko-uses-gpl-only-symbol-rcu-read-lock/280908)


## Workaround patch from Gentoo

"As a workaround, reuse the old implementation until NVIDIA makes
a fixed release (due to no longer be using `pfn_valid`, likely
with its own implementation similarly to this patch)."

[nvidia-drivers-470.223.02-gpl-pfn-valid.patch](https://github.com/gentoo/gentoo/blob/c64caf53/x11-drivers/nvidia-drivers/files/nvidia-drivers-470.223.02-gpl-pfn_valid.patch)


