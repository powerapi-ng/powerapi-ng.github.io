# How to active cgroups V1
You can enable cgroups V1 by adding `systemd.unified_cgroup_hierarchy=false` and `systemd.legagy_systemd_cgroup_controller=false` as permanent parameters of the kernel. In order to that follow these instructions:

 - Open the GRUB file:
```
sudo nano /etc/default/grub
```

 - Add to `GRUB_CMDLINE_LINUX_DEFAULT` the two parameters:

```
GRUB_CMDLINE_LINUX_DEFAULT="quit splash {==systemd.unified_cgroup_hierarchy=false systemd.legagy_systemd_cgroup_controller=false==}"

```

 - Update grub:
```
sudo update-grub
```
