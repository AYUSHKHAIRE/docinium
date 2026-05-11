#!/usr/bin/env bash
set +e

# ------------------------------------------------------------
# Create runtime directories required by dbus
# ------------------------------------------------------------
mkdir -p /run/dbus
chmod 755 /run/dbus

# ------------------------------------------------------------
# Create user if missing (safe on rebuild)
# ------------------------------------------------------------
if ! id docinium >/dev/null 2>&1; then
    groupadd -g 1020 docinium || true
    useradd \
        -u 1020 \
        -g 1020 \
        -G sudo \
        -m \
        -s /bin/bash docinium
    echo "docinium:docinium" | chpasswd
fi

# ------------------------------------------------------------
# Clean stale XRDP PID files
# ------------------------------------------------------------
rm -f /var/run/xrdp/xrdp*.pid /run/xrdp/xrdp*.pid 2>/dev/null || true

# ------------------------------------------------------------
# Start DBUS (system bus)
# ------------------------------------------------------------
if ! pgrep -x dbus-daemon >/dev/null; then
    /usr/bin/dbus-daemon --system --fork
fi

# ------------------------------------------------------------
# Force XRDP default resolution by patching xrdp.ini
# ------------------------------------------------------------
XRDP_CONF="/etc/xrdp/xrdp.ini"

if ! grep -q "width=1920" "$XRDP_CONF"; then
    cat >> "$XRDP_CONF" <<EOF

[xrdp1]
name=sesman-Xvnc
lib=libvnc.so
username=ask
password=ask
ip=127.0.0.1
port=-1
width=1920
height=1080
EOF
fi

# ------------------------------------------------------------
# Ensure XFCE session is 1920x1080
# ------------------------------------------------------------
STARTWM="/etc/xrdp/startwm.sh"
if ! grep -q "xrandr --fb 1920x1080" "$STARTWM"; then
    sed -i "1i xrandr --fb 1920x1080" "$STARTWM"
fi

# ------------------------------------------------------------
# Create autostart for Selenium script
# ------------------------------------------------------------
mkdir -p /home/docinium/.config/autostart
cat > /home/docinium/.config/autostart/selenium.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Selenium Script
Exec=bash -c 'sleep 3; export $(grep -v "^#" /container/runtime.env | xargs); sleep 3; python3 /container/script.py'
X-GNOME-Autostart-enabled=true
EOF
chown -R docinium:docinium /home/docinium/.config

env | grep DOCINIUM > /container/runtime.env

echo "[entrypoint] starting xrdp services"
# run XRDP in background
/usr/sbin/xrdp-sesman &
/usr/sbin/xrdp &

echo "[entrypoint] container ready, blocking PID 1"
/bin/bash -c "tail -f /dev/null"