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

%global evdi_version 1.9.1
%global release_date 2021-09

# systemd 248+
%if 0%{?rhel} == 8
%global _systemd_util_dir %{_prefix}/lib/systemd
%endif

Name:       displaylink
Version:    5.4.1
Release:    1%{?dist}
Summary:    DisplayLink VGA/HDMI driver for DL-6xxx, DL-5xxx, DL-41xx and DL-3xxx adapters
License:    DisplayLink Software License Agreement

# https://www.synaptics.com/products/displaylink-graphics/downloads/ubuntu
Source0:    https://www.synaptics.com/sites/default/files/exe_files/%{release_date}/DisplayLink USB Graphics Software for Ubuntu%{version}-EXE.zip#/%{name}-%{version}.zip
Source1:    https://www.synaptics.com/sites/default/files/release_notes/%{release_date}/DisplayLink USB Graphics Software for Ubuntu%{version}-Release Notes.txt#/%{name}-%{version}.txt

Source10:   99-%{name}.rules
Source11:   %{name}.service
# Extracted from displaylink-installer.sh:
Source12:   %{name}
Source13:   95-%{name}.preset
Source14:   20-%{name}.conf
Source15:   %{name}.logrotate

ExclusiveArch:  %{ix86} x86_64 armv7hl

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:   evdi-kmod >= %{evdi_version}
Requires:   libevdi >= %{evdi_version}
Requires:   libusbx%{?_isa}
Requires:   logrotate
Requires:   xorg-x11-server-Xorg

Provides:   evdi-kmod-common == %{evdi_version}

%description
This adds support for HDMI/VGA adapters built upon the DisplayLink DL-6xxx,
DL-5xxx, DL-41xx and DL-3xxx series of chipsets. This includes numerous docking
stations, USB monitors, and USB adapters.

%prep
%autosetup -c %{name}-%{version}

chmod +x displaylink-driver-%{version}*.run
./displaylink-driver-%{version}*.run --noexec --keep --target .
rm -f evdi.tar.gz *.run
find . -name "libusb*.so*" -delete

chmod -x LICENSE

cp %{SOURCE1} .

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
%doc %{name}-%{version}.txt
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/displaylink.service
%{_presetdir}/95-%{name}.preset
%{_systemd_util_dir}/system-sleep/%{name}
%{_udevrulesdir}/99-%{name}.rules
%{_sysconfdir}/X11/xorg.conf.d/20-%{name}.conf
%{_libexecdir}/%{name}
%dir %{_localstatedir}/log/%{name}/

%changelog
* Sat Sep 11 2021 Simone Caronni <negativo17@gmail.com> - 5.4.1-1
- Update to 5.4.1.

* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 5.4-1
- First build.
