FROM fedora:latest

RUN dnf install -y \
        binutils \
        createrepo_c \
        curl \
        gh \
        git \
        gnupg2 \
        rpm-build \
        rpm-sign \
        tar \
        xz \
    && dnf clean all \
    && rm -rf /var/cache/dnf
