%define	name	wifi-radar
%define	version	1.9.8
%define	release	%mkrel 4

Summary:	Utility for managing WiFi profiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://wifi-radar.systemimager.org/pub/%{name}-%{version}.tar.bz2
Source1:	16x%{name}.png
Source2:	32x%{name}.png
Source3:	48x%{name}.png
License:	GPL
Group:		Networking/Other
Url:		http://wifi-radar.systemimager.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	pygtk2.0
Requires:	dhcpcd
Requires:	usermode-consoleonly
BuildArch:	noarch

%description
WiFi Radar is a Python/PyGTK2  utility for managing WiFi profiles.
It enables you to scan for available networks and create profiles for
your preferred networks. At boot time, running WiFi Radar will
automatically scan for an available preferred network and connect to
it. You can drag and drop your preferred networks to arrange the
profile priority.

%prep
%setup -q
perl -pi -e 's!^CONF_FILE\s*=.*!CONF_FILE = "%{_sysconfdir}/%{name}.conf"!' %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT

install -D -m 755 %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}/
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 600 %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 %{name}.1 $RPM_BUILD_ROOT/%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
install -m 644 %{name}.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5

install -m 644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m 644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=WIFI radar
Comment=Simple wireless network manager
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/%{name} <<EOF
USER=root
PROGRAM=%{_sbindir}/%{name}
SESSION=true
EOF

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name} <<EOF
#%PAM-1.0
auth       sufficient   pam_rootok.so
auth       sufficient   pam_timestamp.so
auth       include      system-auth
session    required     pam_permit.so
session    optional     pam_xauth.so
session    optional     pam_timestamp.so
account    required     pam_permit.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc CHANGE.LOG README README.WPA-Mini-HOWTO.txt TODO
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}.conf.5*

