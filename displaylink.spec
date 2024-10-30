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

# systemd 248+
%if 0%{?rhel} == 7 || 0%{?rhel} == 8
%global _systemd_util_dir %{_prefix}/lib/systemd
%endif

Name:       displaylink
Version:    6.1.0
Release:    1%{?dist}
Summary:    DisplayLink VGA/HDMI driver for DL-6xxx, DL-5xxx, DL-41xx and DL-3xxx adapters
License:    DisplayLink Software License Agreement

Source0:    %{name}-%{version}.tar.xz
Source1:    %{name}-generate-tarball.sh

Source10:   99-%{name}.rules
Source11:   %{name}.service
# Extracted from service-installer.sh:
Source12:   %{name}
Source13:   95-%{name}.preset
Source14:   20-%{name}.conf
Source15:   %{name}.logrotate

ExclusiveArch:  %{ix86} x86_64 armv7hl aarch64

BuildRequires:  chrpath
BuildRequires:  systemd-rpm-macros

Requires:   evdi-kmod >= 1.14.1
Requires:   libevdi >= 1.14.1
Requires:   logrotate
Requires:   xorg-x11-server-Xorg

Provides:   evdi-kmod-common >= 1.14.1

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
install -p -m644 *.spkg %{buildroot}%{_libexecdir}/%{name}/

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
* Wed Oct 30 2024 Simone Caronni <negativo17@gmail.com> - 6.1.0-1
- Update to 6.1.0.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 6.0.0-2
- Re-enable start/stop service based on USB insertions/removals (#2).

* Sat May 04 2024 Simone Caronni <negativo17@gmail.com> - 6.0.0-1
- Update to 6.0.0.

* Wed Sep 06 2023 Simone Caronni <negativo17@gmail.com> - 5.8.0-2
- Fix evdi requirements.
- Drop leftover build requirements.

* Wed Aug 23 2023 Simone Caronni <negativo17@gmail.com> - 5.8.0-1
- Update to 5.8.0.

* Thu Apr 20 2023 Simone Caronni <negativo17@gmail.com> - 5.7.1-1
- Update to 5.7.0.

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 5.6.1-1
- Update to 5.6.1.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 5.6.0-2
- Add Install section to systemd unit to allow using it as a normal unit and not
  on hotplug events.

* Tue May 24 2022 Simone Caronni <negativo17@gmail.com> - 5.6.0-1
- Update to 5.6.0.

* Mon May 02 2022 Simone Caronni <negativo17@gmail.com> - 5.5.0-5
- Allow upgrading open source components separately.

* Mon Mar 14 2022 Simone Caronni <negativo17@gmail.com> - 5.5.0-4
- Update to final 5.5.0 release.

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
