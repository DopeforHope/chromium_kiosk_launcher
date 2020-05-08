# Chromium Kiosk Launcher and Survivor
Simple script so launch chromium in kiosk mode on all avaible monitors (GNOME/Ubuntu18.04/X11)

## Use-Case

You have a machine which shall run on several monitors a website in kiosk mode. Meaning full-screen without any interruptions and from boot on automatically. While there is no easy way specifying the display for an applications (because everything gets merges as DISPLAY :0), you need to parse `xrandr` output and take the offset as start positions for your chromium windows. And then you need to create temporary profile directories and so on.
This script also covers the case that a monitor gets disconnected and later reconnected. It's a small pain in the ass which is thr reason I shared it. It's not perfect as I haven't found a way of just starting mutliple new windows on different screen but it's better than nothing.
