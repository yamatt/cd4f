%global __os_install_post %{nil}
%global debug_package %{nil}

Name:           claude-desktop
Version:        @VERSION@
Release:        1%{?dist}
Summary:        Claude Desktop for Linux (Unofficial RPM Repackage)
License:        Proprietary
URL:            https://claude.ai

AutoReqProv:    no
Requires:       gtk3, libnotify, nss, libXScrnSaver, libXtst, xdg-utils, at-spi2-core, libuuid, mesa-libgbm

%description
Unofficial RPM repackage of Anthropic's official Debian package for Claude Desktop.

%install
mkdir -p %{buildroot}
cp -a %{_sourcedir}/unpacked/* %{buildroot}/

%files
%defattr(-,root,root,-)
/usr/bin/claude-desktop
/usr/lib/claude-desktop
%attr(4755,root,root) /usr/lib/claude-desktop/chrome-sandbox
/usr/share/applications/claude-desktop.desktop
/usr/share/icons/hicolor/*/apps/claude-desktop.png