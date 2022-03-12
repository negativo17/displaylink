%global debug_package %{nil}

%ifarch x86_64
%global ub_folder x64-ubuntu-1604
%endif

%ifarch %{ix86}
%global ub_folder x86-ubuntu-1604
%endif

%ifarch armv7hl
%global ub_folder arm-linux-gnueabihf
%endif

%ifarch aarch64
%global ub_folder aarch64-linux-gnu
%endif

%global evdi_version 1.10.1

# systemd 248+
%if 0%{?rhel} == 7 || 0%{?rhel} == 8
%global _systemd_util_dir %{_prefix}/lib/systemd
%endif

Name:       displaylink
Version:    5.5.0
Release:    3%{?dist}
Summary:    DisplayLink VGA/HDMI driver for DL-6xxx, DL-5xxx, DL-41xx and DL-3xxx adapters
License:    DisplayLink Software License Agreement

Source0:    %{name}-%{version}.tar.xz
Source1:    %{name}-generate-tarball.sh

Source10:   99-%{name}.rules
Source11:   %{name}.service
# Extracted from displaylink-installer.sh:
Source12:   %{name}
Source13:   95-%{name}.preset
Source14:   20-%{name}.conf
Source15:   %{name}.logrotate

ExclusiveArch:  %{ix86} x86_64 armv7hl aarch64

BuildRequires:  chrpath
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:   evdi-kmod >= %{evdi_version}
Requires:   libevdi >= %{evdi_version}
Requires:   logrotate
Requires:   xorg-x11-server-Xorg

Provides:   evdi-kmod-common == %{evdi_version}

%description
This adds support for HDMI/VGA adapters built upon the DisplayLink DL-6xxx,
DL-5xxx, DL-41xx and DL-3xxx series of chipsets. This includes numerous docking
stations, USB monitors, and USB adapters.

%prep
%autosetup

chmod -x LICENSE

chrpath -d %{ub_folder}/DisplayLinkManager

%build
# Nothing to build.

%install
mkdir -p \
    %{buildroot}%{_libexecdir}/%{name}/ \
    %{buildroot}%{_udevrulesdir}/ \
    %{buildroot}%{_unitdir}/ \
    %{buildroot}%{_presetdir}/ \
    %{buildroot}%{_systemd_util_dir}/system-sleep/ \
    %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/ \
    %{buildroot}%{_sysconfdir}/logrotate.d/ \
    %{buildroot}%{_localstatedir}/log/%{name}/

# Main binary and firmware
install -p -m755 %{ub_folder}/DisplayLinkManager %{buildroot}%{_libexecdir}/%{name}/
install -p -m644 ella-dock-release.spkg firefly-monitor-release.spkg ridge-dock-release.spkg %{buildroot}%{_libexecdir}/%{name}/

# udev rules
cp -a %{SOURCE10} %{buildroot}%{_udevrulesdir}/

# systemd stuff
install -p -m644 %{SOURCE11} %{buildroot}%{_unitdir}/
install -p -m755 %{SOURCE12} %{buildroot}%{_systemd_util_dir}/system-sleep/%{name}
install -p -m644 %{SOURCE13} %{buildroot}%{_presetdir}/

# X.org stuff
cp -a %{SOURCE14} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/

# logrotate
cp -a %{SOURCE15} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE 3rd_party_licences.txt
%doc DisplayLink*.txt
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/displaylink.service
%{_presetdir}/95-%{name}.preset
%{_systemd_util_dir}/system-sleep/%{name}
%{_udevrulesdir}/99-%{name}.rules
%{_sysconfdir}/X11/xorg.conf.d/20-%{name}.conf
%{_libexecdir}/%{name}
%dir %{_localstatedir}/log/%{name}/

%changelog
* Sat Mar 12 2022 Simone Caronni <negativo17@gmail.com> - 5.5.0-3
- Add missing aarch64 to allowed architectures.
- Fix building on RHEL/CentOS 7.

* Fri Mar 04 2022 Simone Caronni <negativo17@gmail.com> - 5.5.0-2
- Update evdi provider version.

* Fri Jan 21 2022 Simone Caronni <negativo17@gmail.com> - 5.5.0-1
- Update to 5.5 beta.
- Add aarch64 and CentOS/RHEL 8+ build.

* Fri Nov 05 2021 Simone Caronni <negativo17@gmail.com> - 5.4.1-3
- Do not use hard requirement on libusb, let RPM pick it up.

* Fri Sep 24 2021 Simone Caronni <negativo17@gmail.com> - 5.4.1-2
- Remove Runpath.

* Sat Sep 11 2021 Simone Caronni <negativo17@gmail.com> - 5.4.1-1
- Update to 5.4.1.

* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 5.4-1
- First build.
