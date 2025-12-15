# ============================================================
# Stage 1: Build pulseaudio-module-xrdp
# ============================================================
FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    sudo \
    git build-essential autoconf automake libtool pkg-config \
    libpulse-dev libltdl-dev ca-certificates lsb-release \
    python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Build PulseAudio XRDP modules
RUN git clone https://github.com/neutrinolabs/pulseaudio-module-xrdp.git /src
WORKDIR /src

RUN scripts/install_pulseaudio_sources_apt.sh && \
    ./bootstrap && \
    ./configure PULSE_DIR=$HOME/pulseaudio.src && \
    make && \
    make install DESTDIR=/tmp/out


# ============================================================
# Stage 2: Runtime image with XRDP + Desktop + Audio
# ============================================================
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV XRDP_PULSE_SOURCE=1

# ------------------------------------------------------------
# Base packages
# ------------------------------------------------------------
RUN apt update && apt install -y \
    xfce4 xfce4-goodies xfce4-terminal \
    xrdp xorgxrdp \
    pulseaudio pulseaudio-utils pavucontrol \
    dbus-x11 x11-xserver-utils \
    sudo vim git wget tar locales \
    python3 python3-pip \
    ca-certificates && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Copy built PulseAudio XRDP modules
# ------------------------------------------------------------
COPY --from=builder /tmp/out /

# ------------------------------------------------------------
# PulseAudio XRDP configuration (CORRECT WAY)
# ------------------------------------------------------------
RUN install -d /etc/pulse && \
    echo "load-module module-xrdp-sink" > /etc/pulse/xrdp.pa && \
    echo "load-module module-xrdp-source" >> /etc/pulse/xrdp.pa

# Autostart PulseAudio for XRDP sessions
RUN mkdir -p /etc/xdg/autostart && \
    printf "[Desktop Entry]\nType=Application\nName=PulseAudio XRDP\nExec=pulseaudio --start --exit-idle-time=-1\nOnlyShowIn=XFCE;\n" \
    > /etc/xdg/autostart/pulseaudio-xrdp.desktop

# ------------------------------------------------------------
# Install Google Chrome
# ------------------------------------------------------------
# ------------------------------------------------------------
# Install Google Chrome (correct dependency handling)
# ------------------------------------------------------------
RUN apt update && apt install -y \
    ca-certificates \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    gnupg && \
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor \
        > /usr/share/keyrings/google-linux.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] \
        http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list && \
    apt update && \
    apt install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Create non-root user for XRDP
# ------------------------------------------------------------
RUN useradd -m -s /bin/bash ubuntu && \
    echo "ubuntu:ubuntu" | chpasswd && \
    usermod -aG sudo ubuntu

# Allow sudo without password (optional)
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# ------------------------------------------------------------
# XRDP configuration
# ------------------------------------------------------------
RUN sed -i 's/^port=3389/port=3389/' /etc/xrdp/xrdp.ini && \
    sed -i 's/^max_bpp=.*/max_bpp=32/' /etc/xrdp/xrdp.ini

# ------------------------------------------------------------
# Application files
# ------------------------------------------------------------
WORKDIR /container

COPY requirements.txt .
COPY script.py .
COPY logger_config.py .

RUN pip3 install -r requirements.txt

# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------
COPY entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh

EXPOSE 3389

ENTRYPOINT ["/usr/bin/entrypoint.sh"]